import logging

import azure.functions as func
from stactools.palsar import cog
from azure.storage.blob import BlobServiceClient
import os

def main(msg: func.QueueMessage) -> None:
    body = msg.get_body().decode('utf-8')
    if body[0] == '/':
        filename = body[1:]
    else:
        filename = body
    logging.info('Python queue trigger function processed a queue item: %s', body)
    blob_service_client = BlobServiceClient.from_connection_string(os.environ["AzureWebJobsStorage"])
    blob_client = blob_service_client.get_blob_client(container="dltest", blob=filename)
    if blob_client.exists():
        bd = blob_client.download_blob()
        path_segments = filename.split('/')
        path = '/'.join(path_segments[:len(path_segments) - 1])
        file = filename.replace(path,'')
        target_path = '/tmp/' + file
        with open(target_path, 'wb') as target_file:
            bd.readinto(target_file)
        logging.info('Saved input at ' + target_path)
        cogs = cog.cogify(target_path, '/tmp')
        logging.info('Saved COGs at' + str(cogs))
        for cogfile in cogs:
            _, tail = os.path.split(cogfile)
            
            dir, _ = os.path.split(filename)
            blob_client = blob_service_client.get_blob_client(container="output", blob=dir + '/' + tail)
            # Upload the created file
            temp_path = cogfile
            with open(temp_path, "rb") as data:
                try:
                    blob_client.upload_blob(data, overwrite = True)
                    logging.info("Success for " + temp_path + "@" + dir + tail)
                except Exception as e:
                    logging.info("Exception for " + temp_path)
                os.remove(temp_path)
