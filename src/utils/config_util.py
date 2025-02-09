from contextlib import suppress

import yaml
from yaml import FullLoader

from src.consts import CONFIG_DIR, PEM_DIR
from src.prj_info import Config
from src.utils import common_util, DotDict


def load_config(env):
    config_path = CONFIG_DIR / f"config_{env}.yaml"
    with open(config_path, "r") as file:
        data = yaml.load(file, Loader=FullLoader)

    # load config into class for more convenient
    for key, value in data.items():
        setattr(Config, key, value)

    return DotDict(data)


def gen_password():
    path = PEM_DIR / "pkey.pem"

    with suppress(FileNotFoundError):
        with path.open("r+") as _r:
            public_key = _r.readline()

    public_key = common_util.decode_base64(public_key)
    password = Config.password
    result = common_util.encrypt_rsa_base64(password, public_key)

    return result
