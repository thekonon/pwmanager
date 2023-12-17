import unittest, string, os
from res.utils import DBHandler, PWGenerator, CryptoManager, WrongPasswordError
from tempfile import NamedTemporaryFile

class TestCryptoManager(unittest.TestCase):
    def setUp(self):
        self.password = "my_secret_password"
        self.salt = b"my_salt"
        self.crypto_manager = CryptoManager(password=self.password, salt=self.salt)

    def test_generate_key_from_password(self):
        key = self.crypto_manager._generate_key_from_password(self.password)
        self.assertIsNotNone(key)

    def test_encrypt_string(self):
        test_string = "Hello, World!"
        encrypted_string = self.crypto_manager.encrypt_string(test_string)
        self.assertNotEqual(test_string, encrypted_string)

    def test_decrypt_string(self):
        test_string = "Hello, World!"
        encrypted_string = self.crypto_manager.encrypt_string(test_string)
        decrypted_string = self.crypto_manager.decrypt_string(encrypted_string)
        self.assertEqual(test_string, decrypted_string)

    def test_wrong_password_exception(self):
        wrong_password = "wrong_password"
        wrong_crypto_manager = CryptoManager(password=wrong_password, salt=self.salt)
        test_string = "Hello, World!"
        encrypted_string = self.crypto_manager.encrypt_string(test_string)
        with self.assertRaises(WrongPasswordError):
            wrong_crypto_manager.decrypt_string(encrypted_string)


class TestPWGenerator(unittest.TestCase):
    def test_default_password_length(self):
        pw_generator = PWGenerator()
        password = pw_generator.get_random_password()
        self.assertEqual(len(password), 12)

    def test_custom_password_length(self):
        pw_generator = PWGenerator(length=16)
        password = pw_generator.get_random_password()
        self.assertEqual(len(password), 16)

    def test_include_lowercase_letters(self):
        pw_generator = PWGenerator(lower_case_letters=True)
        password = pw_generator.get_random_password()
        self.assertTrue(any(c.islower() for c in pw_generator._all_chars))

    def test_include_uppercase_letters(self):
        pw_generator = PWGenerator(upper_case_letters=True)
        password = pw_generator.get_random_password()
        self.assertTrue(any(c.isupper() for c in pw_generator._all_chars))

    def test_include_digits(self):
        pw_generator = PWGenerator(digits=True)
        password = pw_generator.get_random_password()
        self.assertTrue(string.digits in pw_generator._all_chars)

    def test_include_symbols(self):
        pw_generator = PWGenerator(symbols=True)
        password = pw_generator.get_random_password()
        self.assertTrue(string.punctuation in pw_generator._all_chars)


class TestDBHandler(unittest.TestCase):
    def setUp(self):
        # Create a temporary database file for testing
        self.db_file = NamedTemporaryFile(delete=False)
        self.db_url = f'sqlite:///{self.db_file.name}'
        self.db_handler = DBHandler(database_url=self.db_url)

    def test_save_and_get_password(self):
        site = "TestSite"
        password = "TestPassword".encode()

        # Save the password
        self.db_handler.save_password(site, password)

        # Retrieve the password
        retrieved_password = self.db_handler.get_password(site)

        # Check if the retrieved password matches the original password
        self.assertEqual(retrieved_password, password)

    def test_get_password_nonexistent_site(self):
        nonexistent_site = "NonExistentSite"

        # Try to get a password for a site that does not exist
        with self.assertRaises(ValueError) as context:
            self.db_handler.get_password(nonexistent_site)

        # Check if the correct exception is raised
        self.assertEqual(str(context.exception), "Site is not in the database!")

    def test_get_all_sites(self):
        sites = ["Site1", "Site2", "Site3"]

        # Save passwords for multiple sites
        for site in sites:
            self.db_handler.save_password(site, f"{site}_password".encode())

        # Retrieve all site names
        retrieved_sites = self.db_handler.get_all_sites()

        # Check if the retrieved site names match the original site names
        self.assertCountEqual(retrieved_sites, sites)

if __name__ == "__main__":
    unittest.main()
