from rest_framework.response import Response


class GenericSuccessResponse(Response):

    def __init__(self, data=None, message=None, status=200):
        super().__init__()

        if data is None:
            self.response_data = []
        else:
            self.response_data = data

        self.data = {
            "data": self.response_data,
            "status": {
                "code": status,
                "message": message
            }
        }
        self.status_code = status
