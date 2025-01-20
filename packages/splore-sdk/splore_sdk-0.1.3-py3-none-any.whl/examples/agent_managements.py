from splore_sdk import SploreSDK

sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")
response = sdk.get_agents(agentId="YOUR_AGENT_ID")
print(response)