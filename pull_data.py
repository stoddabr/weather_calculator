from google.cloud import storage

# from https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/storage/cloud-client/snippets.py

def download(bucket_name, source_blob_name, 
        destination_file_name, verbose=False):
    """Downloads a blob from the bucket."""
    print('downloading from, to:',source_blob_name,destination_file_name) #REVIEW log

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    if verbose:
        print('Blob {} downloaded to {}.'.format(
            source_blob_name,
            destination_file_name))


def upload(bucket_name, source_file_name, destination_blob_name, verbose=False):
    """Uploads a file to the bucket."""
    print('uploading from, to:',source_file_name,destination_blob_name) #REVIEW log

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    if verbose:
        print('File {} uploaded to {}.'.format(
            source_file_name,
            destination_blob_name))