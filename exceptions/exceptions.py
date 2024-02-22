from fastapi import HTTPException, status


class UnknownFieldsException(HTTPException):
    code = status.HTTP_400_BAD_REQUEST
    detail = "Unknown fields in body data"

    def __init__(self):
        self.status_code = self.code


class NotFoundException(HTTPException):
    code = status.HTTP_404_NOT_FOUND

    def __init__(self):
        self.status_code = self.code


class UserNotFoundException(NotFoundException):
    detail = "User not found"


class MashupNotFoundException(NotFoundException):
    detail = "Mashup not found"


class SourceNotFoundException(NotFoundException):
    detail = "Source not found"


class AuthorNotFoundException(NotFoundException):
    detail = "Author not found"


class AlreadyExistsException(NotFoundException):
    code = status.HTTP_400_BAD_REQUEST

    def __init__(self):
        self.status_code = self.code


class UserAlreadyExistsException(AlreadyExistsException):
    detail = "This mashup is already exists"


class MashupAlreadyExistsException(AlreadyExistsException):
    detail = "This mashup is already exists"


class SourceAlreadyExistsException(AlreadyExistsException):
    detail = "This source is already exists"


class AuthorAlreadyExistsException(AlreadyExistsException):
    detail = "This author is already exists"
