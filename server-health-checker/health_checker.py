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
        return [server.strip() for server in env_servers.split(",") if server.strip()]

    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
            return config["servers"]
    except FileNotFoundError:
        raise Exception("No SERVERS environment variable or config.json file found.")
    except KeyError:
        raise Exception("config.json must contain a 'servers' list.")


def check_server(url):
    start_time = time.perf_counter()

    try:
        response = urlopen(url, timeout=REQUEST_TIMEOUT)
        end_time = time.perf_counter()

        response_time_ms = round((end_time - start_time) * 1000)
        status_code = response.status

        return {
            "url": url,
            "status_code": status_code,
            "response_time_ms": response_time_ms,
            "healthy": 200 <= status_code <= 299,
            "slow": response_time_ms > SLOW_LIMIT_MS,
            "error": None
        }

    except HTTPError as error:
        end_time = time.perf_counter()
        response_time_ms = round((end_time - start_time) * 1000)

        return {
            "url": url,
            "status_code": error.code,
            "response_time_ms": response_time_ms,
            "healthy": False,
            "slow": response_time_ms > SLOW_LIMIT_MS,
            "error": None
        }

    except (URLError, TimeoutError):
        return {
            "url": url,
            "status_code": None,
            "response_time_ms": None,
            "healthy": False,
            "slow": False,
            "error": "TIMEOUT"
        }


def format_result(result):
    url = result["url"]

    if result["healthy"]:
        line = f"{url} — OK ({result['status_code']}) — {result['response_time_ms']}ms"

        if result["slow"]:
            line += " [slow]"

        return line

    if result["error"] == "TIMEOUT":
        return f"{url} — TIMEOUT"

    return f"{url} — DOWN ({result['status_code']})"


servers = load_servers()

for server in servers:
    result = check_server(server)
    print(format_result(result))