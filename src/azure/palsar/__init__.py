import logging
import os
import shutil
import tempfile
import time
from urllib.parse import urlsplit, urlunsplit

import azure.functions as func  # type: ignore
from azure.storage.blob import BlobServiceClient  # type: ignore

from stactools.palsar import cog, stac

input_blob_service_client = BlobServiceClient.from_connection_string(
    os.environ["ConnectionStringInput"])
output_blob_service_client = BlobServiceClient.from_connection_string(
    os.environ["ConnectionStringOutput"])


def main(msg: func.QueueMessage, context: func.Context) -> None:
    invocation_id = context.invocation_id
    input_container = "dltest"

    logging.getLogger("azure").setLevel(logging.WARNING)

    start_time = time.time()
    body = msg.get_body().decode('utf-8')

    if body[0] == '/':
        source_archive_file = body[1:]
    else:
        source_archive_file = body

    logging.info(
        f"{invocation_id} - Python queue trigger function processed a queue item: %s",
        body)
    tempdir = tempfile.mkdtemp(prefix="palsar-", dir='/home')
    logging.info(f"{invocation_id} - Created tempdir {tempdir}")

    try:

        archive_rootdir, archive_name = os.path.split(source_archive_file)
        output_container_name = 'palsar'
        output_directory = derive_output_directory(archive_name)
        if output_directory is None:
            logging.error(f"{invocation_id} - Neither MOS or FNF archive")
            exit
        upload_rootdir = f'{output_directory}'

        blob_client = input_blob_service_client.get_blob_client(
            container=input_container, blob=source_archive_file)
        if blob_client.exists():
            _, file = os.path.split(source_archive_file)
            input_targz_filepath = os.path.join(tempdir, file)
            download_input_tgz(input_targz_filepath, blob_client,
                               invocation_id)

            cogs = cog.cogify(input_targz_filepath, tempdir)
            logging.info(
                f"COGified {input_targz_filepath} and saved COGs at {str(cogs)}"
            )

            os.remove(input_targz_filepath)
            logging.info(
                f"{invocation_id} - Cleaned up source TarGZ at {input_targz_filepath}"
            )

            upload_cogs(upload_rootdir, output_container_name, cogs,
                        invocation_id)
            logging.info(f"{invocation_id} - Uploaded COGs")

            base_url = os.path.join(
                remove_query_params_and_fragment(
                    output_blob_service_client.url), output_container_name,
                output_directory)
            stac_file_path = generate_stac(tempdir, source_archive_file, cogs,
                                           base_url, invocation_id)
            logging.info(
                f"{invocation_id} - Generated STAC JSON at {str(stac_file_path)}"
            )

            stac_url = upload_stac(upload_rootdir, output_container_name,
                                   stac_file_path, invocation_id)
            logging.info(
                f"{invocation_id} - Uploaded STAC JSON at {str(stac_url)}")

            end_time = time.time()
            logging.info(
                f"{invocation_id} - Runtime is {end_time - start_time}")
            logging.info(f"{invocation_id} - All wrapped up. Exiting")
        else:
            logging.error(
                f"{invocation_id} - File does not exist {source_archive_file} \n"
                f"container {input_container}")
    except Exception as e:
        logging.info(
            f"{invocation_id} - Exception {e} for queue message with body '{body}' "
        )
    shutil.rmtree(tempdir)
    logging.info(f"{invocation_id} - Done. Tempdir removed at {tempdir}")


def derive_output_directory(archive_name):
    output_directory = None
    if "FNF" in archive_name:
        output_directory = "alos_fnf_mosaic"
    if "MOS" in archive_name:
        output_directory = "alos_palsar_mosaic"
    return output_directory


def upload_stac(rootdir, output_container_name, json_file_path, invocation_id):
    _, stac_file = os.path.split(json_file_path)
    output_stac_path = f'{rootdir}/{stac_file}'
    blob_client = output_blob_service_client.get_blob_client(
        container=output_container_name, blob=output_stac_path)
    with open(json_file_path, "rb") as data:
        try:
            blob_client.upload_blob(data, overwrite=True)
            logging.info(
                f"{invocation_id} - Successfully uploaded STAC JSON to {output_stac_path}"
            )
            return blob_client.url
        except Exception as e:
            logging.info(
                f"{invocation_id} - Exception {e} for {json_file_path}")


def upload_cogs(output_rootdir, output_container, cogs, invocation_id):
    for key in list(cogs.keys()):
        cogfile = cogs[key]
        _, cog_file = os.path.split(cogfile)
        output_cog_path = f'{output_rootdir}/{cog_file}'
        blob_client = output_blob_service_client.get_blob_client(
            container=output_container, blob=output_cog_path)
        with open(cogfile, "rb") as data:
            try:
                blob_client.upload_blob(data, overwrite=True)
                logging.info(
                    f"{invocation_id} - Successfully uploaded COG to {output_cog_path}"
                )
            except Exception as e:
                logging.info(f"{invocation_id} - Exception {e} for {cogfile}")


def generate_stac(tempdir, source_archive, cogs, base_url, invocation_id):
    source_basename = os.path.basename(source_archive)
    json_file = '_'.join(source_basename.split("_")[0:3])
    json_path = os.path.join(tempdir, f'{json_file}.json')
    self_href = os.path.join(base_url, os.path.basename(json_path))

    item = stac.create_item(cogs, base_url)
    item.set_self_href(self_href)
    item.validate()
    item.save_object(dest_href=json_path)

    logging.info(f"{invocation_id} - Saved STAC JSON at {json_path}")
    return json_path


def download_input_tgz(input_targz_filepath, blob_client, invocation_id):
    bd = blob_client.download_blob()
    with open(input_targz_filepath, 'wb') as target_file:
        bd.readinto(target_file)

    logging.info(f"{invocation_id} - Saved input at {input_targz_filepath}")


def remove_query_params_and_fragment(url):
    return urlunsplit(urlsplit(url)._replace(query="", fragment=""))
