# transfer_client/transfer_manager.py

import os
import uuid
import requests
from requests.auth import HTTPBasicAuth


class TransferManager:
    def __init__(self, host, username=None, password=None):
        """
        Initializes the TransferManager with the specified host and optional authentication.

        :param host:     Hostname or IP address with optional port (e.g., 'some.transfer.sh',
                         '192.168.1.100:8080', 'http://localhost:8080', 'https://localhost:8080')
        :param username: Username for basic authentication (optional)
        :param password: Password for basic authentication (optional)
        """
        self.host = host.rstrip('/')  # Ensure no trailing slash
        self.username = username
        self.password = password

    def generate_random_filename(self, original_file_path, save_ext=True):
        """
        Generates a random filename using UUID. Optionally preserves the original file's extension.

        :param original_file_path: Path to the original file.
        :param save_ext:            If True, preserves the file extension. Otherwise, no extension is added.
        :return:                    Generated random filename.
                                     Examples: 'd4f5c6e7-8a9b-4c2d-9e0f-1a2b3c4d5e6f.png' or 'd4f5c6e78a9b4c2d9e0f1a2b3c4d5e6f'
        """
        random_uuid = str(uuid.uuid4())
        if save_ext:
            _, ext = os.path.splitext(original_file_path)
            return random_uuid + ext
        return random_uuid

    def upload(self, file_path, max_downloads=None, max_days=None, generate_random_filename=False, save_ext=True):
        """
        Uploads a file to the server and returns the download URL.

        :param file_path:               Path to the local file to be uploaded.
        :param max_downloads:           (int) Maximum number of downloads allowed (optional).
        :param max_days:                (int) Maximum number of days the file will be available (optional).
        :param generate_random_filename: (bool) Generate a random filename. If False, use the original filename.
        :param save_ext:                (bool) Preserve the file extension when generating a random filename.
        :return:                        A string containing the URL where the file can be downloaded.
        :raises FileNotFoundError:     If the specified file does not exist.
        :raises RuntimeError:          If the upload fails.
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File '{file_path}' does not exist.")

        # Determine the filename for upload
        if generate_random_filename:
            upload_filename = self.generate_random_filename(file_path, save_ext=save_ext)
        else:
            upload_filename = os.path.basename(file_path)

        # Construct the upload URL
        upload_url = f"{self.host}/{upload_filename}"

        # Prepare headers
        headers = {}
        if max_downloads is not None:
            headers['Max-Downloads'] = str(max_downloads)
        if max_days is not None:
            headers['Max-Days'] = str(max_days)

        # Read the file content
        with open(file_path, 'rb') as f:
            file_data = f.read()

        try:
            # Send PUT request to upload the file
            response = requests.put(
                upload_url,
                data=file_data,
                headers=headers,
                auth=HTTPBasicAuth(self.username, self.password) if self.username and self.password else None
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error during file upload: {e}")

        # Assuming the server returns the download link in the response body
        download_link = response.text.strip()
        return download_link


# ===== Example Usage =====
if __name__ == "__main__":
    host = "http://localhost:8080"  # Can be 'http://192.168.1.100:8080', 'https://some.transfer.sh', etc.
    username = "some_username"
    password = "some_password"

    manager = TransferManager(host, username, password)
    
    file_to_upload = "test.txt"
    
    try:
        link = manager.upload(
            file_path=file_to_upload,
            max_downloads=1,               # Limit to 1 download
            max_days=5,                    # Keep the file for 5 days
            generate_random_filename=True, # Generate a random filename
            save_ext=True                  # Preserve the file extension
        )
        print("File uploaded successfully!")
        print("Download link:", link)
    except Exception as e:
        print("Upload failed:", e)
