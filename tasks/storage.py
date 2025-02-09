import random

from locust import task, tag, FastHttpUser
from src.test_data import File
from src.consts import FILES
from src.utils.file_util import handle_file_path
from src.prj_info import Config, FileInfo, Endpoints, DataRuntime


class StorageTest(FastHttpUser):
    # host = "https://storage.k8s.flodev.net"
    host = "not using"

    @task
    @tag("upload")
    def upload(self):
        file_info = File(file_size=FileInfo.size, file_amount=FileInfo.amount)
        file_paths = [FILES[f"f_{file_info.file_size}KB"] for _ in range(file_info.file_amount)]
        
        file = handle_file_path(file_paths)

        if not DataRuntime.options.all_users or DataRuntime.options.is_spawn_complete:
            self.client.post(Endpoints.Storage.upload, data=file_info.upload(), files=file, headers=Config.headers)

    @task
    @tag("download")
    def download(self):

        file_uid = random.choice(FileInfo.file_uid_list)
        file_info = File(file_uid=file_uid)

        if not DataRuntime.options.all_users or DataRuntime.options.is_spawn_complete:
            self.client.get(Endpoints.Storage.download, params=file_info.download(), headers=Config.headers)

        