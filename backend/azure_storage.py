# backend/azure_storage.py
import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER_NAME = os.getenv('AZURE_STORAGE_CONTAINER_NAME')

blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

def upload_file_to_blob(file_path, blob_name):
    try:
        blob_client = container_client.get_blob_client(blob_name)
        with open(file_path, 'rb') as data:
            blob_client.upload_blob(data, overwrite=True)
        url = blob_client.url
        return url
    except Exception as e:
        print(f"Error uploading to blob: {e}")
        return None

def list_blobs():
    try:
        blobs = container_client.list_blobs()
        blob_urls = [container_client.get_blob_client(blob.name).url for blob in blobs]
        return blob_urls
    except Exception as e:
        print(f"Error listing blobs: {e}")
        return []

def upload_blob_with_sas(container_sas_url, local_file_path, blob_name='speech.wav'):
    try:
        # Extract the container URL and the SAS token
        container_url, sas_token = container_sas_url.split("?")

        # Construct the blob URL by appending the blob name to the container URL
        blob_url_with_sas = f"{container_url}/{blob_name}?{sas_token}"

        # Create a BlobClient using the constructed blob URL with SAS
        blob_client = BlobClient.from_blob_url(blob_url_with_sas)

        # Upload the file
        with open(local_file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        # Retrieve and return the blob's URL without the SAS token for public access
        blob_url_without_sas = f"{container_url}/{blob_name}"
        print_with_date(f"File uploaded successfully to {blob_url_without_sas}")
        return blob_url_without_sas
    except Exception as e:
        print_with_date(f"Failed to upload blob: {e}")
        return None