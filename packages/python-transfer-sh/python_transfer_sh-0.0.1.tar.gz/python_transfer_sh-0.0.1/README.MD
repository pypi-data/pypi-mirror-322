# Transfer.sh Client

`transfersh-client` is a Python library designed to upload files to [transfer.sh](https://github.com/dutchcoders/transfer.sh) servers. It supports both public transfer.sh instances and self-hosted servers, provided that the server is already running.

## Features

- **File Uploading**: Upload files to a transfer.sh server using HTTP PUT requests.
- **Authentication**: Supports HTTP Basic Authentication for secured servers.
- **Filename Management**: Option to use original filenames or generate random filenames using UUIDs, with optional preservation of file extensions.
- **Upload Constraints**: Set maximum number of downloads and expiration days for uploaded files.
- **Flexible Host Configuration**: Supports various host formats, including local IPs with ports and HTTP/HTTPS protocols.

## Installation

Install `python-transfer-sh` via `pip`:

```bash
pip install python-transfer-sh
```

## Usage

### Importing the Library

```python
from transfer_sh_client.manager import TransferManager
```

### Initializing `TransferManager`

```python
host = "https://some.transfer.sh"  # Examples: 'http://localhost:8080', 'https://192.168.1.100:8443'
username = "admin"                         # Optional
password = "X9kmP2vL5nQ8j"                 # Optional

manager = TransferManager(host, username, password)
```

- **host**: The transfer.sh server's URL or IP address, including the protocol (`http` or `https`) and port if necessary.
  - Examples:
    - `http://localhost:8080`
    - `https://192.168.1.100:8443`
    - `https://some.transfer.sh`
- **username**: (Optional) Username for HTTP Basic Authentication.
- **password**: (Optional) Password for HTTP Basic Authentication.

### Uploading a File

```python
file_to_upload = "path/to/your/file.txt"

try:
    download_link = manager.upload(
        file_path=file_to_upload,
        max_downloads=3,               # Optional: Maximum number of downloads
        max_days=7,                    # Optional: Number of days the file will be available
        generate_random_filename=True, # Optional: Generate a random filename
        save_ext=True                  # Optional: Preserve the file extension if generating a random filename
    )
    print("File uploaded successfully!")
    print("Download link:", download_link)
except Exception as e:
    print("Upload failed:", e)
```

#### Parameters

- **file_path** (`str`): Path to the local file you want to upload.
- **max_downloads** (`int`, optional): Maximum number of times the file can be downloaded. Defaults to `None` (no limit).
- **max_days** (`int`, optional): Number of days the file will remain available on the server. Defaults to `None` (no expiration).
- **generate_random_filename** (`bool`, optional): If set to `True`, the file will be uploaded with a randomly generated UUID filename. If `False`, the original filename will be used. Defaults to `False`.
- **save_ext** (`bool`, optional): If `generate_random_filename` is `True`, setting this to `True` will preserve the original file's extension. If `False`, the file will be uploaded without an extension. Defaults to `True`.

### Docker-compose for transfer.sh example

You can use this template as example of transfer.sh server:

```yaml
version: '3'
services:
  transfer:
    container_name: transfer.sh
    image: dutchcoders/transfer.sh:latest
    ports:
      - "192.168.1.96:8080:8080" # change to your ip and port, if you have nginx you can use 443 port
    volumes:
      - /path/to/transfer/data:/data
    environment:
      - PURGE_DAYS=7
      - MAX_UPLOAD_SIZE=2147483648  # 2GB
      - RATE_LIMIT=100
      - HTTP_AUTH_USER=admin # Optional
      - HTTP_AUTH_PASS=some_password  # Optional
    command: >
      --provider local
      --basedir /data
      --temp-path /data/temp
      --log /data/transfer.log
    restart: unless-stopped
    networks:
      - transfer_net

networks:
  transfer_net:
    driver: bridge
```

### Example Scenarios

#### 1. Uploading with Original Filename

```python
download_link = manager.upload(
    file_path="document.pdf"
)
print("Download link:", download_link)
```

#### 2. Uploading with Random Filename and Preserved Extension

```python
download_link = manager.upload(
    file_path="image.png",
    generate_random_filename=True,
    save_ext=True
)
print("Download link:", download_link)
```

#### 3. Uploading with Random Filename without Extension and Constraints

```python
download_link = manager.upload(
    file_path="archive.zip",
    generate_random_filename=True,
    save_ext=False,
    max_downloads=5,
    max_days=10
)
print("Download link:", download_link)
```

## Supported Host Formats

The `host` parameter accepts various formats to accommodate different server configurations:

- **Localhost with Port**:
  - `http://localhost:8080`
  - `https://localhost:8443`

- **Local IP with Port**:
  - `http://192.168.1.100:8080`
  - `https://192.168.1.100:8443`

- **Domain with Protocol**:
  - `http://some.transfer.sh:8080`
  - `https://some.transfer.sh`

Ensure that the transfer.sh server you are uploading to is running and configured to handle HTTP PUT requests.

## Error Handling

The `upload` method raises exceptions in the following scenarios:

- **FileNotFoundError**: If the specified file does not exist.
- **RuntimeError**: If the upload fails due to network issues, authentication errors, or server-side problems.

Example:

```python
try:
    download_link = manager.upload("nonexistent.file")
except FileNotFoundError as fnf_error:
    print(fnf_error)
except RuntimeError as runtime_error:
    print(runtime_error)
```

## Dependencies

`transfersh-client` relies on the `requests` library, which is automatically installed when you install `transfersh-client` via `pip`.

If you need to install it manually:

```bash
pip install requests
```

## License

This project is licensed under the [MIT License](LICENSE).
