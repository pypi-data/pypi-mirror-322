class MlflowException(Exception):
    message: str

    def __str__(self):
        return self.message


class UnauthorizedException(MlflowException):
    message = "401 Unauthorized"


class AlreadyExistsException(MlflowException):
    message = "Resource with the provided name already exists"


class NotFoundException(MlflowException):
    message = "404 Not Found"


class MaxRetriesException(MlflowException):
    message = "Connection failed: maximum number of retries exceeded"


class UnexpectedException(MlflowException):
    message = "An unexpected error have occurred"


def process_exception(e: Exception):
    error_str = str(e)
    match error_str:
        case msg if "INTERNAL_ERROR: 401 Unauthorized" in msg:
            raise UnauthorizedException

        case msg if "RESOURCE_ALREADY_EXISTS" in msg:
            raise AlreadyExistsException

        case msg if "Version has already been taken" in msg:
            raise AlreadyExistsException

        case msg if "Not Found" in msg:
            raise NotFoundException

        case msg if "RESOURCE_DOES_NOT_EXIST" in msg:
            raise NotFoundException

        case msg if "Max retries exceeded" in msg:
            raise MaxRetriesException

    raise UnexpectedException from e
