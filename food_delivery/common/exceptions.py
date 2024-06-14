from rest_framework.exceptions import APIException
from rest_framework import status
from django.http import JsonResponse


class BadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Bad Request'


class GenericException(JsonResponse):
    """
    Generic Exceptions will return status code of 500 and given error message
    """

    def __init__(self, message=None,
                 data=None,
                 code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                 *args,
                 **kwargs):

        if message is None:
            self.message = "There is some internal issue, Please try again later."
        else:
            self.message = message

        self.code = code

        if data is None:
            self.response_data = []

        self.data = {
            "data": self.response_data,
            "status": {
                "code": self.code,
                "message": self.message
            }
        }

        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        super().__init__(*args, **kwargs, data=self.data)


class CustomBadRequest(GenericException):
    def __init__(self, message=None, data=None, code=400, *args, **kwargs):
        super().__init__(message, data, code, *args, **kwargs)

        self.code = 400

        if message is None:
            self.message = "Bad Request"

        self.status_code = 400

