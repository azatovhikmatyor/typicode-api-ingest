import json
import os
from pathlib import Path
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from typing import Union
from collections.abc import Mapping


# XXX: ???
# 1. Is function name self explanatory or is there any better name?
# 2. Should max_retry: int = 0 option be added?
def get_data(url: str, cache: bool = False, from_local: bool = False):
    # FIXME: `cache` folder name is hardcoded and the code to get filename itself is ugly.
    # get directory name from argument and check if directory exists, if not: create
    Path('cache').mkdir(parents=True, exist_ok=True)
    file_name = url.split("/")[-1] + ".json"
    file_name = os.path.join("cache", file_name)
    if from_local:
        try:
            with open(file_name, "rb") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Failed to load from local. Fetching from API...")
            return get_data(url, from_local=False, cache=True)
        except Exception:
            print("Error during loading data from local file")
            raise

    try:
        res = urlopen(url)
    except HTTPError as err:
        print("HTTPError", err)
        raise
    except URLError as err:
        print("URLError", err)
        raise
    except Exception:
        print("Some other exception during retrieving the url", url)
        raise
    else:
        res_content = res.read()
        return json.loads(res_content)
    finally:
        if cache:
            with open(file_name, "wb") as f:
                print("Caching the response...")
                f.write(res_content)


# FIXME: Mapping | list | tuple - ugly
def is_nested(data: Union[list, Mapping]):
    if isinstance(data, Mapping):
        for val in data.values():
            if isinstance(val, Mapping | list | tuple):
                return True
        return False
    elif isinstance(data, list | tuple) and len(data) > 0:
        return is_nested(data[0])
    else:
        return False


def flatten_json_list(json_list):
    flattened_list = []

    for item in json_list:
        flattened_item = {}
        flatten_recursive(item, '', flattened_item)
        flattened_list.append(flattened_item)

    return flattened_list


def flatten_recursive(json_obj, prefix, flattened_dict):
    for key, value in json_obj.items():
        new_key = f"{prefix}{key}"

        if isinstance(value, dict):
            flatten_recursive(value, f"{new_key}__", flattened_dict)
        else:
            flattened_dict[new_key] = value