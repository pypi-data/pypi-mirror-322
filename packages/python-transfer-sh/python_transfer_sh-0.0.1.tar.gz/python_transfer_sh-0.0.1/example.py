from transfersh_client import TransferManager

# ===== Example Usage =====
if __name__ == "__main__":
    host = "https://some.transfer.sh"  # Can be 'http://192.168.1.100:8080', 'https://some.transfer.sh', etc.
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
