import os

from google.cloud import dialogflow

projectid = os.environ["GCP_PROJECT_ID"]


async def intent_reply(session_id, text):
    session_client = dialogflow.SessionsAsyncClient()
    session = session_client.session_path(projectid, session_id)
    text_input = dialogflow.TextInput(text=text, language_code="en-US")
    query_input = dialogflow.QueryInput(text=text_input)
    return await session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
