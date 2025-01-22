import io
import os
import tempfile

from cryptography.fernet import Fernet
from dotenv import dotenv_values


class CredentialsManager:
    def __init__(self, env_name="development", key_path="master.key"):
        """
        Initializes the CredentialsManager.

        :param env_name: Environment name (e.g., development, production).
        :param key_path: Master key file path.
        """
        self.env_name = env_name
        self.key_path = key_path
        self.env_enc_path = f".env.{env_name}.enc"
        self.key = self._load_or_create_key()

    def _load_or_create_key(self):
        """
        Loads or generates the master key.

        :return: Master key (bytes).
        """
        if os.path.exists(self.key_path):
            with open(self.key_path, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_path, "wb") as f:
                f.write(key)
            return key

    def create_empty_env_enc(self):
        """
        Creates an empty .env.enc file.
        """
        with open(self.env_enc_path, "wb") as f:
            f.write(b"")
        print(f"Created empty encrypted file: {self.env_enc_path}")

    def decrypt_to_temp(self):
        """
        Decrypts the .env.enc file to a temporary file.

        :return: Temporary file path.
        """
        if not os.path.exists(self.env_enc_path):
            raise FileNotFoundError(f"Encrypted file {self.env_enc_path} not found.")

        with open(self.env_enc_path, "rb") as f:
            encrypted_data = f.read()

        cipher_suite = Fernet(self.key)
        decrypted_data = (
            cipher_suite.decrypt(encrypted_data).decode("utf-8")
            if encrypted_data
            else ""
        )
        # Creates a temporary file
        with tempfile.NamedTemporaryFile(
            delete=False, mode="w", suffix=".env"
        ) as temp_file:
            temp_file.write(decrypted_data)

        return temp_file.name

    def decrypt_env(self):
        """
        Decrypts the .env.enc file and returns the environment variables dictionary.

        :return: Decrypted environment variables dictionary.
        """
        if not os.path.exists(self.env_enc_path):
            raise FileNotFoundError(f"Encrypted file {self.env_enc_path} not found.")

        with open(self.env_enc_path, "rb") as f:
            encrypted_data = f.read()

        cipher_suite = Fernet(self.key)
        decrypted_data = cipher_suite.decrypt(encrypted_data).decode("utf-8")

        # Convert the decrypted string to a stream for dotenv_values
        decrypted_stream = io.StringIO(decrypted_data)
        # Parse the decrypted content using dotenv_values
        return dotenv_values(stream=decrypted_stream)

    def encrypt_from_temp(self, temp_file_path):
        """
        Re-encrypts from the temporary file to the .env.enc file.

        :param temp_file_path: Temporary file path.
        """
        with open(temp_file_path, "rb") as f:
            plain_data = f.read()

        cipher_suite = Fernet(self.key)
        encrypted_data = cipher_suite.encrypt(plain_data)

        with open(self.env_enc_path, "wb") as f:
            f.write(encrypted_data)

        print(f"Re-encrypted and saved to {self.env_enc_path}")

    def cleanup_temp_file(self, temp_file_path):
        """
        Cleans up the temporary file.

        :param temp_file_path: Temporary file path.
        """
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            print(f"Cleaned up temporary file: {temp_file_path}")

    def ensure_files_exist(self):
        """
        Ensures the master key and .env.enc file exist.
        """
        if not os.path.exists(self.key_path):
            self._load_or_create_key()
            print(f"Created master key: {self.key_path}")

        if not os.path.exists(self.env_enc_path):
            self.create_empty_env_enc()
