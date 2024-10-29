# Import required libraries
from composio_openai import ComposioToolSet, Action
import os
import groq
from dotenv import load_dotenv

# Initialize Composio toolset with API key
tool_set = ComposioToolSet(api_key=os.environ["COMPOSIO_API_KEY"])

# Initialize Groq client for LLM interaction
groq_client = groq.Groq(api_key=os.environ["GROQ_API_KEY"])

# Load environment variables
load_dotenv()

# ===== Email Fetching =====
# Fetch latest newsletter emails from Gmail
payload = tool_set.execute_action(
    Action.GMAIL_FETCH_EMAILS,
    {"max_results": 1, "query": "newsletters"},  # Adjust max_results to fetch more emails
)

# Initialize Slack messaging tools
tools = tool_set.get_tools(actions=[Action.SLACK_SENDS_A_MESSAGE_TO_A_SLACK_CHANNEL])

# ===== Content Processing =====
# Extract email content from the payload
newsletter_content = payload["data"]["response_data"]

# Combine all email content into a single string
final_content = ""
for email in newsletter_content:
    final_content += email["messageText"]

# ===== Prompt Configuration =====
# Define system prompt for the AI's role
system_prompt = """
Summarize the content given to you in a concise, succinct, and informative way. Then send it to the user on the general channel of their Slack.
"""

# Create user prompt with the newsletter content
user_prompt = f"""
    Summarize and send the following newsletter content {final_content} to the user on the general channel of their Slack.
    """

# Prepare messages for the LLM
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt},
]

# ===== LLM Interaction =====
# Get completion from Groq LLM
response = groq_client.chat.completions.create(
    model="llama-3.2-90b-text-preview",
    messages=messages,
    tools=tools,
    tool_choice="auto",
    max_tokens=8192,
)

# ===== Execute Slack Message =====
# Handle tool calls to send the summary to Slack
response_after_tool_calls = tool_set.handle_tool_calls(response=response)

# Print the result of the operation
print(response_after_tool_calls)
