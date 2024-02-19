from fastapi import HTTPException, status


class UnknownFieldsExeption(HTTPException):
    code = status.HTTP_400_BAD_REQUEST
    detail = "Unknown fields in body data"

    def __init__(self):
        self.status_code = self.code


class NotFoundExeption(HTTPException):
    code = status.HTTP_404_NOT_FOUND

    def __init__(self):
        self.status_code = self.code


class UserNotFoundExeption(NotFoundExeption):
    detail = "User not found"


class MashupNotFoundExeption(NotFoundExeption):
    detail = "Mashup not found"


class SourceNotFoundExeption(NotFoundExeption):
    detail = "Source not found"


class AuthorNotFoundExeption(NotFoundExeption):
    detail = "Author not found"


class AlreadyExistsExeption(NotFoundExeption):
    code = status.HTTP_400_BAD_REQUEST

    def __init__(self):
        self.status_code = self.code


class UserAlreadyExistsExeption(AlreadyExistsExeption):
    detail = "This mashup is already exists"


class MashupAlreadyExistsExeption(AlreadyExistsExeption):
    detail = "This mashup is already exists"


class SourceAlreadyExistsExeption(AlreadyExistsExeption):
    detail = "This source is already exists"


class AuthorAlreadyExistsExeption(AlreadyExistsExeption):
    detail = "This author is already exists"
