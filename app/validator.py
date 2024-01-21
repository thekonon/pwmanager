from .exceptions import (
    PasswordToShortError,
    PasswordHasNoDigitError,
    PasswordHasNoSpecialCharacterError,
)
import string


def validate_raw_password(password: str) -> None:
    """Check if password meet all critteria, returns True
    otherwise one of exception is rissen

    Args:
        password (str): _description_

    Raises:
        PasswordToShortError: is thrown if password has less than 4 chars
        PasswordHasNoDigitError
        PasswordHasNoSpecialCharacterError

    Returns:
        bool: True if password is ok
    """
    min_password_lengt = 4
    if len(password) < min_password_lengt:
        raise PasswordToShortError(
            f"Password must be at least {min_password_lengt} characters"
        )
    if not any(c.isdigit() for c in password):
        raise PasswordHasNoDigitError("Password must contain at least 1 digit")
    if not any(c in string.punctuation for c in password):
        raise PasswordHasNoSpecialCharacterError(
            "Pasword must contain at least special character"
        )
