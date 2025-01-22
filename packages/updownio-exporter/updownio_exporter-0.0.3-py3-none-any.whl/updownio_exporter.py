import logging
import time
from collections import defaultdict
from datetime import datetime, timezone

import requests
from prometheus_client import Counter, Gauge, Histogram, start_http_server
from the_conf import TheConf

conf = TheConf(
    {
        "source_order": ["env", "files"],
        "config_files": [
            "/etc/updownio-exporter/updownio-exporter.json",
            "~/.config/updownio-exporter.json",
        ],
        "parameters": [
            {"name": {"default": "updownio-exporter"}},
            {"type": "list", "apikeys": {"type": str}},
            {
                "loop": [
                    {"interval": {"default": 240, "help": "seconds"}},
                    {"reset": {"default": 48, "help": "hours"}},
                ]
            },
            {
                "prometheus": [
                    {"port": {"type": "int", "default": 9100}},
                    {"namespace": {"default": "updownio"}},
                ]
            },
            {"logging": [{"level": {"default": "WARNING"}}]},
        ],
    }
)

logger = logging.getLogger("updownio-exporter")
try:
    logger.setLevel(getattr(logging, conf.logging.level.upper()))
    logger.addHandler(logging.StreamHandler())
except AttributeError as error:
    raise AttributeError(
        f"{conf.logging.level} isn't accepted, only DEBUG, INFO, WARNING, "
        "ERROR and FATAL are accepted"
    ) from error


URL = "https://updown.io/api/%s?api-key=%s"
RESPONSE_TIME_BUCKETS = [125, 250, 500, 1000, 2000, 4000, 8000, 16000, 32000]
DAEMON = Gauge("daemon", "", ["name", "section", "status"])
APDEX = Gauge(
    "apdex",
    "apdex",
    ["alias"],
    namespace=conf.prometheus.namespace,
)
TIMINGS = Gauge(
    "timings",
    "timings",
    ["alias", "step"],
    namespace=conf.prometheus.namespace,
)
REQUEST_COUNT = Counter(
    "request",
    "request",
    ["alias", "tag"],
    namespace=conf.prometheus.namespace,
)
RESPONSE_TIME = Histogram(
    "response_time",
    "Response time",
    ["alias"],
    buckets=RESPONSE_TIME_BUCKETS,
    namespace=conf.prometheus.namespace,
)
CACHE: dict = defaultdict(lambda: defaultdict(int))


def browse_request_by_response_time(metrics: dict, alias: str):
    histogram = RESPONSE_TIME.labels(alias)
    observed_sample = 0
    # filling each buckets with every non seen counter with value
    # of half distance with previous bucket
    previous_bucket = 0
    for bucket in RESPONSE_TIME_BUCKETS:
        count = metrics["requests"]["by_response_time"][f"under{bucket}"]
        for _ in range(count - CACHE[alias][bucket]):
            histogram.observe(bucket - ((bucket - previous_bucket) / 2))
            observed_sample += 1
        CACHE[alias][bucket] = count
        previous_bucket = bucket

    new_sample_cnt = metrics["requests"]["samples"] - CACHE[alias]["samples"]

    if observed_sample < new_sample_cnt:
        for _ in range(new_sample_cnt - observed_sample):
            histogram.observe(RESPONSE_TIME_BUCKETS[-1] * 2)
    CACHE[alias]["samples"] = metrics["requests"]["samples"]


def collect(api_key, from_):
    logger.debug("listing checks from %r", from_)
    response = requests.get(URL % ("checks", api_key), timeout=60)
    response.raise_for_status()
    checks = response.json()

    for check in checks:
        alias = check["alias"].lower().replace(" ", "-")
        uri = f"checks/{check['token']}/metrics"
        url = URL % (uri, api_key) + f"&from={from_.isoformat()}"
        logger.debug("querying for checks on %r", check["token"])
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        metrics = response.json()
        if "apdex" in metrics:  # accounting apdex
            APDEX.labels(alias=alias).set(metrics["apdex"])
        # filling histogram
        if "requests" in metrics:
            browse_request_by_response_time(metrics, alias)
        # counting request
        for key, value in metrics.get("requests", {}).items():
            if isinstance(value, int):
                REQUEST_COUNT.labels(alias, key).inc(value - CACHE[alias][key])
                CACHE[alias][key] = value
        for step, timing in metrics.get("timings", {}).items():
            TIMINGS.labels(alias=alias, step=step).set(timing)


def main():
    labels = {"name": conf.name, "section": "config"}
    DAEMON.labels(status="loop-period", **labels).set(conf.loop.interval)
    DAEMON.labels(status="loop-reset", **labels).set(conf.loop.reset)
    DAEMON.labels(status="item-count", **labels).set(len(conf.apikeys))

    labels["section"] = "exec"
    from_ = datetime.now(timezone.utc)
    while True:
        elapsed_time = (datetime.now(timezone.utc) - from_).total_seconds()
        # reseting
        logger.info("new loop %s seconds from beginning", elapsed_time)
        if elapsed_time >= conf.loop.reset * 60 * 60:
            logger.info(
                "resetting time period and counters after %d hours",
                conf.loop.reset,
            )
            for metric in APDEX, TIMINGS, REQUEST_COUNT, RESPONSE_TIME:
                metric.clear()
            CACHE.clear()
            from_ = datetime.now(timezone.utc)
            DAEMON.labels(status="loop-reset", **labels).inc()
        DAEMON.labels(status="items-ok", **labels).set(0)
        DAEMON.labels(status="items-ko", **labels).set(0)
        for api_key in conf.apikeys:
            try:
                collect(api_key, from_)
            except Exception:
                logger.exception("something went wrong when collecting")
                DAEMON.labels(status="items-ko", **labels).inc()
                continue
            DAEMON.labels(status="items-ok", **labels).inc()
        DAEMON.labels(status="loop-count", **labels).inc()
        time.sleep(conf.loop.interval)


if __name__ == "__main__":
    logger.info("starting updownio-exporter")
    start_http_server(conf.prometheus.port)
    main()
