import logging
import os
import time

import azure.functions as func  # type: ignore
from azure.storage.blob import BlobServiceClient  # type: ignore

from stactools.palsar import cog, stac

blob_service_client = BlobServiceClient.from_connection_string(
    os.environ["AzureWebJobsStorage"])

def main(msg: func.QueueMessage) -> None:
    input_container = "dltest"

    start_time = time.time()
    body = msg.get_body().decode('utf-8')
    if body[0] == '/':
        source_archive_file = body[1:]
    else:
        source_archive_file = body
    logging.info('Python queue trigger function processed a queue item: %s',
                 body)

    archive_rootdir, archive_name = os.path.split(source_archive_file)
    output_container_name = derive_output_container(archive_name)
    if output_container_name is None:
        logging.error("Neither MOS or FNF archive")
        return -1

    blob_client = blob_service_client.get_blob_client(container=input_container,
                                                      blob=source_archive_file)
    if blob_client.exists():
        cogs = download_and_process_cogs(source_archive_file, blob_client)
        logging.info(f"Saved COGs at {str(cogs)}")
        base_url = upload_cogs(archive_rootdir, output_container_name, cogs)
        logging.info(f"Uploaded COGs")
        stac_file_path = generate_stac(source_archive_file, cogs, base_url)
        logging.info(f"Generated STAC JSON at {str(stac_file_path)}")
        stac_url = upload_stac(archive_rootdir, output_container_name, stac_file_path)
        logging.info(f"Uploaded STAC JSON at {str(stac_url)}")

        cleanup_cogs(cogs)
        logging.info(f"Cleaned up COGs")

        os.remove(stac_file_path)
        logging.info(f"Cleaned up STAC file")

        end_time = time.time()
        logging.info(f"Runtime is {end_time - start_time}")
        logging.info("All wrapped up. Exiting")
    else:
        logging.error(f"File does not exist at {source_archive_file} in container {input_container}")


def derive_output_container(archive_name):
    output_container_name = None
    if "MOS" in archive_name:
        output_container_name = "output-mos"
    if "FNF" in archive_name:
        output_container_name = "output-fnf"
    return output_container_name


def upload_stac(rootdir, output_container_name, json_file_path):
    _, stac_file = os.path.split(json_file_path)
    output_stac_path = f'{rootdir}/{stac_file}'
    blob_client = blob_service_client.get_blob_client(
            container=output_container_name, blob=output_stac_path)
    with open(json_file_path, "rb") as data:
        try:
            blob_client.upload_blob(data, overwrite=True)
            logging.info(f"Successfully uploaded STAC JSON for {output_stac_path}")
            return blob_client.url
        except Exception as e:
            logging.info(f"Exception {e} for {json_file_path}")


def cleanup_cogs(cogs):
    for cogfile in list(cogs.values()):
        os.remove(cogfile)
        logging.info(f"Cleaned up {cogfile}")


def upload_cogs(rootdir, output_container, cogs):
    for cogfile in list(cogs.values()):
        _, cog_file = os.path.split(cogfile)
        blob_client = blob_service_client.get_blob_client(
            container=output_container, blob=rootdir + '/' + cog_file)
        with open(cogfile, "rb") as data:
            try:
                blob_client.upload_blob(data, overwrite=True)
                logging.info(f"Success for {cogfile}")
            except Exception as e:
                logging.info(f"Exception {e} for {cogfile}")

    base_url = os.path.dirname(blob_client.url)
    return base_url


def generate_stac(source_archive, cogs, base_url):
    source_basename = os.path.basename(source_archive)
    json_file = '_'.join(source_basename.split("_")[0:3])
    json_path = os.path.join('/tmp', f'{json_file}.json')
    self_href = os.path.join(base_url, os.path.basename(json_path))

    item = stac.create_item(cogs, base_url)
    item.set_self_href(self_href)
    item.validate()
    item.save_object(dest_href=json_path)

    logging.info(f"Saved STAC JSON at {json_path}")
    return json_path


def download_and_process_cogs(input_filename, blob_client):
    bd = blob_client.download_blob()

    _, file = os.path.split(input_filename)
    input_targz_filepath = f'/tmp/{file}'
    with open(input_targz_filepath, 'wb') as target_file:
        bd.readinto(target_file)

    logging.info(f"Saved input at {input_targz_filepath}")

    cogs = cog.cogify(input_targz_filepath, '/tmp')
    logging.info(f"COGified {input_targz_filepath}")
    return cogs
