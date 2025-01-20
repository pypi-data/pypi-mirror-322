from splore_sdk import SploreSDK

sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")
extraction_agent = sdk.init_agent(agent_id="YOUR_AGENT_ID")
extraction_agent.extract(file_path="absolute_file_path")
# response = extraction_agent.extractions.all_extracted_response()
# print(response)