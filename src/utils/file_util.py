import json
import os

from src.consts import RESOURCE
from src.utils.logging_util import setup_logger, logger

setup_logger()


def handle_file_path(file_paths):
    files = []
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as file:
            files.append(
                ("file", (file_name, file.read(), f"{file_name}"))
            )

    return files


def load_json_file(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    return data


def store_files(file_size, resp_data: list, username):
    file_name = f'{username.split("@")[0]}_file_uids.json'
    path = RESOURCE / "stored_data" / file_name

    file_uid_list = [item["uid"] for item in resp_data]

    # Check if JSON file exists, create if not
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump({}, f)  # Initialize with an empty JSON object

    data = load_json_file(path)

    # Initialize category list if not present
    if not data.get(f"f_{file_size}"):
        data[f"f_{file_size}"] = []

    # Append file_uid to the respective category list
    data[f"f_{file_size}"].extend(file_uid_list)

    # Write updated data back to the JSON file
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def get_file_uid_list(file_size, username):
    file_name = f'{username.split("@")[0]}_file_uids.json'
    path = RESOURCE / "stored_data" / file_name

    if not os.path.exists(path):
        return []

    logger.info("- Loading file uid from stored file....")
    data = load_json_file(path)
    file_uid_list = data[f"f_{file_size}"]

    return file_uid_list


def remove_file(file_size, file_uid_list, username):
    file_name = f'{username.split("@")[0]}_file_uids.json'
    path = RESOURCE / "stored_data" / file_name

    with open(path, "r") as f:
        data = json.load(f)

    file_data = data.get(f"f_{file_size}", [])

    for file_uid in file_uid_list:

        if file_uid in file_data:
            file_data.remove(file_uid)

    # Write updated data back to the JSON file
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
