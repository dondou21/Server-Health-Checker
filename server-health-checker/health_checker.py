import json
import os
import time
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


CONFIG_FILE = "config.json"


def load_servers():
    env_servers = os.getenv("SERVERS")

    if env_servers:
        servers = env_servers.split(",")
        return [server.strip() for server in servers if server.strip()]

    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
            return config["servers"]
    except FileNotFoundError:
        raise Exception("No SERVERS environment variable or config.json file found.")
    except KeyError:
        raise Exception("config.json must contain a 'servers' list.")


def check_json_status(response_body):
    try:
        data = json.loads(response_body)
        return data.get("status") == "ok"
    except json.JSONDecodeError:
        return None


def check_server(url):
    start_time = time.perf_counter()

    try:
        response = urlopen(url, timeout=5)
        response_body = response.read().decode("utf-8")
        end_time = time.perf_counter()

        response_time_ms = round((end_time - start_time) * 1000)
        status_code = response.status
        json_ok = check_json_status(response_body)

        return {
            "url": url,
            "status_code": status_code,
            "response_time_ms": response_time_ms,
            "healthy": 200 <= status_code <= 299,
            "json_ok": json_ok
        }

    except HTTPError as error:
        end_time = time.perf_counter()
        response_time_ms = round((end_time - start_time) * 1000)

        return {
            "url": url,
            "status_code": error.code,
            "response_time_ms": response_time_ms,
            "healthy": False,
            "json_ok": None
        }

    except URLError:
        return {
            "url": url,
            "status_code": None,
            "response_time_ms": None,
            "healthy": False,
            "json_ok": None
        }


servers = load_servers()
print(f"Loaded {len(servers)} servers")

result = check_server("https://httpbin.org/json")
print(result)