import Exception


class DataError(Exception):
    def __init__(self, status, message):
        self.status = status
        self.message = message

    def msg(self):
        return dict(status=self.status, message=self.message)
