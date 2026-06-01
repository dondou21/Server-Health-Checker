import json
import os
import requests


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
    response = requests.get(url)

    return {
        "url": url,
        "status_code": response.status_code
    }


servers = load_servers()
print(f"Loaded {len(servers)} servers")

result = check_server(servers[0])
print(result)