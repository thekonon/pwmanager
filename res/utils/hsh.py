from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64


class WrongPasswordError(Exception):
    """
    This excetion is return if CryptoManager is unable to decrypt bytes string
    """

    def __init__(self, msg, *args: object) -> None:
        super().__init__(*args)
        self.msg = msg

    def __str__(self) -> str:
        return self.msg


class CryptoManager:
    """
    This class is used for ecrypting and decrypting string
    """

    def __init__(self, password: str, *args, **kwargs) -> None:
        """
        Pass a password for encrypting and decrypting strings.
        There is a posibility to add a salt kwarg that changes parameter for key generation

        Args:
            password (str): String used for key generation
        """
        if not "salt" in kwargs.keys():
            self._salt = password.encode()
        else:
            self._salt = kwargs["salt"]

        self._key = self._generate_key_from_password(password)

    def encrypt_string(self, string_to_encrypt: str) -> bytes:
        """
        Method return a bytes string from string input. Password passed to init method is used
        to generate key that encrypts string

        Args:
            string_to_encrypt (str): from this string is bytes string generated

        Returns:
            bytes: bytes string from which original string can be reconstructed
        """
        cipher = Fernet(self._key)
        encrypted_string = cipher.encrypt(string_to_encrypt.encode())
        return encrypted_string

    def decrypt_string(self, bytes_to_decrypt: bytes) -> str:
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
        cipher = Fernet(self._key)
        try:
            decrypted_string = cipher.decrypt(bytes_to_decrypt).decode()
        except Exception as e:
            raise WrongPasswordError("Wrong password")

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

if __name__ == '__main__':
    pass