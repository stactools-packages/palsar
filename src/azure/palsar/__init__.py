import logging
import os
import time

import azure.functions as func  # type: ignore
from azure.storage.blob import BlobServiceClient  # type: ignore

from stactools.palsar import cog, stac

blob_service_client = BlobServiceClient.from_connection_string(
    os.environ["AzureWebJobsStorage"])

def main(msg: func.QueueMessage) -> None:
    start_time = time.time()
    body = msg.get_body().decode('utf-8')
    if body[0] == '/':
        filename = body[1:]
    else:
        filename = body
    logging.info('Python queue trigger function processed a queue item: %s',
                 body)
    rootdir, archive_name = os.path.split(filename)
    output_container = None
    if "MOS" in archive_name:
        output_container = "output-mos"
    if "FNF" in archive_name:
        output_container = "output-fnf"
    if output_container is None:
        logging.error("Neither MOS or FNF archive")
        return -1

    blob_client = blob_service_client.get_blob_client(container="dltest",
                                                      blob=filename)
    if blob_client.exists():
        bd = blob_client.download_blob()

        _, file = os.path.split(filename)
        input_targz_filepath = '/tmp/' + file
        with open(input_targz_filepath, 'wb') as target_file:
            bd.readinto(target_file)
        logging.info('Saved input at ' + input_targz_filepath)

        cogs = cog.cogify(input_targz_filepath, '/tmp')

        logging.info('Saved COGs at' + str(cogs))
        for cogfile in list(cogs.values()):
            _, tail = os.path.split(cogfile)
            blob_client = blob_service_client.get_blob_client(
                container=output_container, blob=rootdir + '/' + tail)
            with open(cogfile, "rb") as data:
                try:
                    blob_client.upload_blob(data, overwrite=True)
                    logging.info("Success for " + cogfile)
                except Exception as e:
                    logging.info(f"Exception {e} for {cogfile}")

        base_url = os.path.dirname(blob_client.url)
        item = stac.create_item(cogs, base_url)
        json_file = '_'.join((os.path.basename(filename)).split("_")[0:3])
        json_path = os.path.join('/tmp', f'{json_file}.json')
        item.set_self_href(os.path.join(base_url, os.path.basename(json_path)))
        # TODO: gracefully fail if validate doesn't work
        item.validate()
        item.save_object(dest_href=json_path)

        logging.info("Saved STAC JSON at " + json_path)

        _, tail = os.path.split(json_path)
        blob_client = blob_service_client.get_blob_client(
            container=output_container, blob=rootdir + '/' + tail)
        with open(json_path, "rb") as data:
            try:
                blob_client.upload_blob(data, overwrite=True)
                logging.info("Successfully uploaded STAC JSON for " + filename)
            except Exception as e:
                logging.info(f"Exception {e} for {json_path}")

        for cogfile in list(cogs.values()):
            os.remove(cogfile)
            logging.info("Cleaned up " + cogfile)

        end_time = time.time()
        logging.info(f"Runtime is {end_time - start_time}")
        logging.info("All wrapped up. Exiting")
