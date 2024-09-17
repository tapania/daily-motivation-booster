# backend/azure_storage.py
import os
from urllib.parse import urlparse, parse_qs
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv

load_dotenv()

CONTAINER_SAS_URL = os.getenv('AZURE_CONTAINER_SAS_URL')

if not CONTAINER_SAS_URL:
    raise ValueError("AZURE_CONTAINER_SAS_URL environment variable is not set")

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

def list_blobs():
    try:
        blobs = container_client.list_blobs()
        blob_urls = [container_client.get_blob_client(blob.name).url.split('?')[0] for blob in blobs]
        return blob_urls
    except Exception as e:
        print(f"Error listing blobs: {e}")
        return []

    
def upload_file_to_blob(file_path, blob_name):
    try:
        # Get the blob client from the container client
        blob_client = container_client.get_blob_client(blob_name)
        
        # Upload the file
        with open(file_path, 'rb') as data:
            blob_client.upload_blob(data, overwrite=True)
        
        # Get the blob URL
        blob_url = blob_client.url
        
        # Remove the SAS token from the URL for public access
        public_url = blob_url.split('?')[0]
        
        print(f"File uploaded successfully to {public_url}")
        return public_url
    except Exception as e:
        print(f"Error uploading to blob: {e}")
        return None