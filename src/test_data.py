
class File:
    def __init__(
            self, channel_id=1676521, message_uid="96c42970-e6ec-11ef-830a-acde48001122", file_uid="",
            file_size=50, file_amount=1
    ) -> None:
        self.channel_id = channel_id
        self.message_uid = message_uid
        self.channel_type = 1
        self.file_size = file_size
        self.file_amount = file_amount
        self.file_uid = file_uid

    def upload(self):
        payload = dict(
            channel_id=self.channel_id, channel_type=self.channel_type, message_uid=self.message_uid,
        )
        return payload

    def download(self):
        params = dict(channel_id=self.channel_id, channel_type=self.channel_type, file_uid=self.file_uid)
        return params
