from splore_sdk import SploreSDK
from examples.aws import download_from_s3

##  example -1 (basic flow to complete extraction using S3)
# intialise the sdk with API key base_id and agentId from splore console
sdk = SploreSDK(api_key="", base_id="", agent_id="")
extraction_agent = sdk.init_agent(agent_id="")
# create a temporary file destination to download file from s3.
file_ref = sdk.file_uploader.create_temp_file_destination()
s3_uri = "s3://abc/def/abc.pdf"
download_from_s3(s3_uri, file_ref)
response = extraction_agent.extract(file_path=file_ref)
    
