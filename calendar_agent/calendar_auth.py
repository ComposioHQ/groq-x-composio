# Import required libraries
import os  
from dotenv import load_dotenv  # For loading environment variables from .env file
from composio_langchain import App, ComposioToolSet  # Composio SDK for API integration

load_dotenv()

# Initialize Composio toolset with API key and entity ID
# The toolset provides methods to interact with various apps like Google Calendar
toolset = ComposioToolSet(
    api_key=os.environ["COMPOSIO_API_KEY"],  # API key from environment variables
    entity_id="Soham"  # Unique identifier for the user
)

# Start OAuth flow to connect with Google Calendar
# This generates a URL that the user needs to visit to grant permissions
connection_request = toolset.initiate_connection(app=App.GOOGLECALENDAR)

# Display the authorization URL to the user
print("Connection Request Redirect URL: ", connection_request.redirectUrl)

# Pause execution until user completes authorization in browser
# User should visit the URL, grant permissions, and then return here
input("Press Enter after completing authorization in browser...")

# Get the connection status after user grants permission
# This verifies if the connection was successful
connection_object = toolset.get_connected_account(id=connection_request.connectedAccountId)

# Display the final connection status
# Should show "connected" if authorization was successful
print("Status of the connection: ", connection_object.status)
print("Connected Account ID: ", connection_object.id)
print("Connected Account Details: ", connection_object)
