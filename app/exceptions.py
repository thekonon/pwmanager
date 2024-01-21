class PasswordIsMissing(Exception):
    def __init__(self, msg: str, *args: object) -> None:
        super().__init__(*args)
        self.msg = msg


class PasswordError(ValueError):
    def __init__(self, msg: str) -> None:
        self.msg = msg


class PasswordToShortError(PasswordError):
    """
    Error is raised when password is too short

    Args:
        msg (string): Extra information
    """


class PasswordHasNoDigitError(PasswordError):
    """
    Error is raised when password has no digit

    Args:
        msg (string): Extra information
    """


class PasswordHasNoSpecialCharacterError(PasswordError):
    """
    Error is raised when password has no special character from string.punctation

    Args:
        msg (string): Extra information
    """


class WrongPasswordError(Exception):
    """
    This excetion is return if CryptoManager is unable to decrypt bytes string
    """

    def __init__(self, msg, *args: object) -> None:
        super().__init__(*args)
        self.msg = msg

    def __str__(self) -> str:
        return self.msg
