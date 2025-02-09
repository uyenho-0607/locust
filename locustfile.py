import time

from locust import events
from locust.runners import MasterRunner

from src.prj_info import Config, FileInfo, DataRuntime
from src.services.oauth2 import Oauth2
from src.utils import file_util, common_util
from src.utils.config_util import load_config
from src.utils.logging_util import setup_logger, logger
from tasks.storage import StorageTest

setup_logger()

is_spawn_complete = False
start_time = None

TOTAL_REQ = 0
PASSED_REQ = 0
RESP_TIME = []


@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--env", type=str, choices=["dev", "qa", "staging"], default="dev")
    parser.add_argument("--username", type=str, default="")
    parser.add_argument("--all_users", type=bool, default=False)
    parser.add_argument("--size", type=int, default=50)
    parser.add_argument("--file_amount", type=int, default=1)


@events.init.add_listener
def on_locust_init(environment, **kwargs):

    runtime_options = environment.parsed_options
    DataRuntime.options.all_users = runtime_options.all_users

    load_config(runtime_options.env)
    logger.info("- Config loaded !")
    if runtime_options.username:
        Config.username = runtime_options.username

    FileInfo.size = runtime_options.size
    FileInfo.amount = runtime_options.file_amount

    FileInfo.file_uid_list = file_util.get_file_uid_list(FileInfo.size, Config.username)

    # Login
    Oauth2.login()


@events.spawning_complete.add_listener
def is_spawn_complete(user_count, **kwargs):
    global start_time
    spawn_duration = time.time() - start_time
    DataRuntime.options.is_spawn_complete = True

    logger.info(f"Spawn completed after {spawn_duration:.2f} seconds")


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    global start_time
    start_time = time.time()
    if not isinstance(environment.runner, MasterRunner):
        logger.info(" Test setup")

    else:
        logger.info("Started test from Master node")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    if not isinstance(environment.runner, MasterRunner):
        logger.info("- Test stopped")
        logger.info(f"- Total: {TOTAL_REQ}, Passed: {PASSED_REQ}, Failed: {TOTAL_REQ - PASSED_REQ}")

        if RESP_TIME:
            logger.info(f"- Percentile 80th: {common_util.calculate_percentile(RESP_TIME, 80)} sec")
    else:
        logger.info("Stopped test from master")


@events.request.add_listener
def on_request(context, **kwargs):
    global TOTAL_REQ, PASSED_REQ, RESP_TIME
    resp = kwargs.get("response")
    TOTAL_REQ += 1

    if resp.ok:
        PASSED_REQ += 1
        resp_time = round(kwargs.get("response_time") * 0.001, 3)
        RESP_TIME.append(resp_time)

        if resp.status_code == 201:
            file_util.store_files(FileInfo.size, resp.json()["data"], Config.username)
    else:
        logger.info(f" Request failed with status_code: {resp.status_code}, error: {resp.reason}")


class MyUser(StorageTest):
    host = "not using"
