import json
import os
import time
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


CONFIG_FILE = "config.json"
SLOW_LIMIT_MS = 500
REQUEST_TIMEOUT = 10


def load_servers():
    env_servers = os.getenv("SERVERS")

    if env_servers:
        return [server.strip() for server in env_servers.split(",")]

    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
            return config["servers"]

    except FileNotFoundError:
        raise Exception(
            "No SERVERS environment variable or config.json file found."
        )

    except KeyError:
        raise Exception(
            "config.json must contain a 'servers' list."
        )


def check_server(url):
    start_time = time.perf_counter()

    try:
        response = urlopen(url, timeout=REQUEST_TIMEOUT)

        end_time = time.perf_counter()

        response_time_ms = round(
            (end_time - start_time) * 1000
        )

        return {
            "url": url,
            "status_code": response.status,
            "response_time_ms": response_time_ms,
            "slow": response_time_ms > SLOW_LIMIT_MS
        }

    except HTTPError as error:
        end_time = time.perf_counter()

        response_time_ms = round(
            (end_time - start_time) * 1000
        )

        return {
            "url": url,
            "status_code": error.code,
            "response_time_ms": response_time_ms,
            "slow": response_time_ms > SLOW_LIMIT_MS
        }

    except Exception:
        return {
            "url": url,
            "status_code": None,
            "response_time_ms": None,
            "slow": False
        }


servers = load_servers()

print(f"Loaded {len(servers)} servers")

result = check_server("https://httpbin.org/delay/2")

if result["slow"]:
    print(
        f"slow response — {result['response_time_ms']}ms"
    )
else:
    print(result)