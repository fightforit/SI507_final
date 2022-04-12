import json
import os


def write_json(filename, data) -> None:
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)


def read_json(filename) -> dict:
    with open(filename, 'r') as f:
        return json.load(f)


def clear_cache() -> None:
    os.system("rm -rf cache/*")


def get_cache(filename) -> dict:
    try:
        return read_json(f"cache/{filename}")
    except:
        return {}
