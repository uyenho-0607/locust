
from src.prj_info import Config, Endpoints
from src.utils.config_util import gen_password
from src.utils.logging_util import logger
import requests


class Oauth2:
    @staticmethod
    def login():
        url = f"{Config.oauth2}{Endpoints.token}"

        headers = {"app_id": Config.app_id, "device_uid": Config.device_uid}
        data = {
            "username": f"{Config.username}@{Config.domain}",
            "password": gen_password(),
            "grant_type": "password"
        }

        resp = requests.post(url=url, data=data, headers=headers)

        if resp.status_code == 200:
            access_token = resp.json()["data"].get("access_token")
            Config.headers = headers | dict(Authorization=f"Bearer {access_token}")
            logger.info(f"- Logged in user {Config.username} success !")

        else:
            raise Exception(f"Login failed! {resp.json()}")

        return resp.json()
