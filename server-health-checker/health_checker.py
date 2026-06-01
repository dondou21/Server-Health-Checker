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
        return [server.strip() for server in servers]

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
        response = urlopen(url, timeout=5)
        end_time = time.perf_counter()

        response_time_ms = round((end_time - start_time) * 1000)

        return {
            "url": url,
            "status_code": response.status,
            "response_time_ms": response_time_ms
        }

    except HTTPError as error:
        end_time = time.perf_counter()
        response_time_ms = round((end_time - start_time) * 1000)

        return {
            "url": url,
            "status_code": error.code,
            "response_time_ms": response_time_ms
        }

    except URLError:
        return {
            "url": url,
            "status_code": None,
            "response_time_ms": None
        }


servers = load_servers()
print(f"Loaded {len(servers)} servers")

result = check_server(servers[0])
print(result)