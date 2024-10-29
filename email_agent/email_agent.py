# Import required libraries
from composio_openai import App, ComposioToolSet
import groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
tool_set = ComposioToolSet(api_key=os.environ["COMPOSIO_API_KEY"])

# Initialize Groq client for LLM interaction
groq_client = groq.Groq(api_key=os.environ["GROQ_API_KEY"])

# ===== User Input Collection =====
# Get email recipient and purpose from user
email_sender = input("Enter the email address of the person you want to send it to: ")
email_purpose = input("Enter the purpose: ")

# ===== Tool and API Setup =====
# Initialize Composio tools for Gmail integration
tools = tool_set.get_tools(apps=[App.GMAIL])

# ===== Prompt Configuration =====
# System prompt defining the AI agent's role
system_prompt = """
You are an AI Agent that writes and sends emails
to the input email id and writes based on the input purpose.
"""

# User prompt with specific email instructions
user_prompt = f"""
Write and send an email to {email_sender} with the purpose: {email_purpose}
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

# ===== Email Execution =====
# Execute the email sending operation using tool calls
response_after_tool_calls = tool_set.handle_tool_calls(response=response)

# Print the result of the operation
print(response_after_tool_calls)
