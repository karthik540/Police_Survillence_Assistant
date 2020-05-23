from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Set up Assistant service.
authenticator = IAMAuthenticator('2_KIdcA2HIx-V2p5eXhN-1G40cDUolsI-ChINtcUGK-b') # replace with API key
service = AssistantV2(
    version = '2019-02-28',
    authenticator = authenticator
)

assistant_id = 'a34f8aab-f7dc-46fc-a907-171b8aa1bf6d' # replace with assistant ID

service.set_service_url(
    'https://api.eu-gb.assistant.watson.cloud.ibm.com'
)

# Create session.
session_id = service.create_session(
    assistant_id = assistant_id
).get_result()['session_id']

# Initialize with empty value to start the conversation.
message_input = {
    'message_type:': 'text',
    'text': ''
}

def botResponseReciever(queryMessage):

    message_input = {
        'message_type:': 'text',
        'text': queryMessage
    }
    response = service.message(
        assistant_id,
        session_id,
        input = message_input
    ).get_result()

    send_data = (
        response['output']['generic'][0]['text'],
        response['output']['intents'][0]['intent']
    )
    
    return send_data

#print(botResponseReciever("Track Shyam"))