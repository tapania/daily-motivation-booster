# backend/azure_storage.py
import os
from urllib.parse import urlparse, parse_qs
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv
import logging

load_dotenv()

CONTAINER_SAS_URL = os.getenv('AZURE_CONTAINER_SAS_URL')

if not CONTAINER_SAS_URL:
    raise ValueError("AZURE_CONTAINER_SAS_URL environment variable is not set")


def list_blobs():
    try:
        # Parse the SAS URL to extract necessary components
        parsed_url = urlparse(CONTAINER_SAS_URL)
        account_name = parsed_url.netloc.split('.')[0]
        container_name = parsed_url.path.split('/')[-1]
        sas_token = parsed_url.query

        # Create the base URL for the storage account
        account_url = f"https://{account_name}.blob.core.windows.net"

        # Create BlobServiceClient using account URL and SAS token
        blob_service_client = BlobServiceClient(account_url=account_url, credential=sas_token)

        # Get a client to interact with the container
        container_client = blob_service_client.get_container_client(container_name)

        blobs = container_client.list_blobs()
        blob_urls = [container_client.get_blob_client(blob.name).url.split('?')[0] for blob in blobs]
        return blob_urls
    except Exception as e:
        logging.error(f"Error listing blobs: {e}")
        return []
    
def upload_file_to_blob(local_file_path, blob_name='speech.wav'):
    try:
        # Extract the container URL and the SAS token
        container_url, sas_token = CONTAINER_SAS_URL.split("?")

        # Construct the blob URL by appending the blob name to the container URL
        blob_url_with_sas = f"{container_url}/{blob_name}?{sas_token}"

        # Create a BlobClient using the constructed blob URL with SAS
        blob_client = BlobClient.from_blob_url(blob_url_with_sas)

        # Upload the file
        with open(local_file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        # Retrieve and return the blob's URL without the SAS token for public access
        blob_url_without_sas = f"{container_url}/{blob_name}"
        #print(f"File uploaded successfully to {blob_url_without_sas}")
        return blob_url_without_sas
    except Exception as e:
        logging.error(f"Failed to upload blob: {e}")
        return None