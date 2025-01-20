import os
import requests
from pathlib import Path
import uuid
import zipfile

from blocks_cli.config.config import config
from blocks_cli.builds import api_client

def get_bundle_upload_url():
    response = api_client.put(f"{config.clients.client_url}/v1/bundles/upload")
    response.raise_for_status()
    return response.json()

def upload_bundle_zip(bundle_upload_url: str, base_path: Path):
    try:
        # Generate a unique ID for the run
        random_file_name = str(uuid.uuid4())
        zip_filename = f"{random_file_name}.zip"

        if os.path.exists(zip_filename):
            os.remove(zip_filename)

        # Create the zip archive from the current directory contents, ignoring specified folders
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(base_path):
                # Skip specified directories
                dirs[:] = [d for d in dirs if d not in ['.git', '.env']]
                for file in files:
                    if file == zip_filename:
                        continue
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, base_path)

                    zipf.write(file_path, arcname)

        # Confirm the creation of the zip file
        if not os.path.exists(zip_filename):
            raise Exception(f"Failed to create {zip_filename}")

        # Upload the zip file to presigned S3 url
        response = requests.put(bundle_upload_url, files={
            "file": (zip_filename, open(zip_filename, "rb"))
        })
        response.raise_for_status() 
    except Exception:
        raise
    finally:
        # remove the zip file
        os.remove(zip_filename)

    return response.text