class UserBaseError(Exception):
    status_code = 500
    detail = "Internal error"

    def __init__(self):
        super().__init__(self.detail)


class InvalidPasswordError(UserBaseError):
    status_code = 400
    detail = "Invalid password"


class UserExpired(UserBaseError):
    status_code = 403
    detail = "User expired"


class UserLocked(UserBaseError):
    status_code = 403
    detail = "User locked"


class UserNotFound(UserBaseError):
    status_code = 404
    detail = "User not found"


class UserExists(UserBaseError):
    status_code = 409
    detail = "User already exists"
