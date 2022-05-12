# Azure Functions for PALSAR STACification #
## Palsar ##
### Trigger ###
Queue

### Purpose ###
This function downloads the file at the path in the message body from the "dltest" blob storage container to local storage, COGifies the tile and generates a STAC record.
To do this, the function interfaces with the python code in this repository.

Once a file is processed, a record is pushed to the "processed-queue" Queue for recording and diff-ing purposes, and the generated COGs and STAC record are uploaded to blob storage.

### Environment vars ###
- Name: ConnectionStringInput
  Purpose: Connection string for the input storage account containing the blob container set by "input_container" in the python function code.
- Name: ConnectionStringOutput
  Purpose: Connection string for the output storage account containing the output blob container set by "output_container_name" in the python function code.
- Name: ConnectionStringQueue
  Purpose: Connection string for the storage account containing the "processed-queue" queue
  
### Body ###
Type: Raw String
Content: Path in "dltest" to find file at. EG: "pub/25_MSC/N00E000/N01E001.tar.gz"
