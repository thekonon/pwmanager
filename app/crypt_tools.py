from typing import Optional, Protocol
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64

from .exceptions import WrongPasswordError


# TODO
class CryptoManagerAbstract(Protocol):
    def encrypt_string(self, string_to_encrypt: str):
        ...


class CryptoManager:
    """
    This class is used for ecrypting and decrypting string
    """

    def __init__(self, password: str, salt: Optional[bytes]) -> None:
        """
        Pass a password for encrypting and decrypting strings.
        There is a posibility to add a salt kwarg that changes parameter for key generation

        Args:
            password (str): String used for key generation
        """
        if salt is None:
            self._salt = password.encode()
        else:
            self._salt = salt

        self._key = self._generate_key_from_password(password)

    def encrypt_string(self, string_to_encrypt: str) -> str:
        """
        Method return a bytes string from string input. Password passed to init method is used
        to generate key that encrypts string

        Args:
            string_to_encrypt (str): from this string is bytes string generated

        Returns:
            bytes: bytes string from which original string can be reconstructed
        """
        cipher = Fernet(self._key)
        encrypted_bytes = cipher.encrypt(string_to_encrypt.encode())
        return encrypted_bytes.decode()

    def decrypt_string(self, string_to_decrypt: str) -> str:
        """
        Method returns orignal string. Bytes string are used as an input. Password passed to init method is used
        to generate key that dencrypts bytes string. If wrong password/key is used. WrongPasswordError is raised

        Args:
            bytes_to_decrypt (bytes): bytes string from which original string is reconstructed

        Raises:
            WrongPasswordError: If wrong password is used, this error is raised

        Returns:
            str: If correct password is used, original string is returned
        """
        cipher = Fernet(self._key)  # TODO - necessary to instantiate Fernet every time?
        try:
            decrypted_string = cipher.decrypt(string_to_decrypt.encode()).decode()
        except Exception:
            raise WrongPasswordError("Password cannot be decrypted")

        return decrypted_string

    def _generate_key_from_password(self, password):
        """
        Private method that generates key.
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), iterations=100000, salt=self._salt, length=32
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
