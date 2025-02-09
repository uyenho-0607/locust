from src.utils import DotDict


class Config:
    username: str
    domain: str
    password: str
    oauth2: str
    headers: dict
    app_id: str
    device_uid: str


class Endpoints:
    token = "/token"

    class Storage:
        upload = "/upload/chat-attachment"
        download = "/download/chat-attachment"


class FileInfo:
    size: int
    amount: int
    file_uid_list: list = []
    stored_data: list = []


class DataRuntime:
    options = DotDict(is_spawn_complete=False, all_users=False)
