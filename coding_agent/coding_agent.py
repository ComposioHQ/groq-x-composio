# Import required libraries
from composio_openai import App, ComposioToolSet, Action
import groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq & Composio clients for LLM interaction
groq_client = groq.Groq(api_key=os.environ["GROQ_API_KEY"])
tool_set = ComposioToolSet(api_key=os.environ["COMPOSIO_API_KEY"])

# User prompt with specific file editing instruction
user_prompt = "Create a file test.py file and make it say print('Hello world')"

# ===== Tool and API Setup =====
# Initialize Composio tools for file operations
tools = tool_set.get_tools(actions=[Action.FILETOOL_CREATE_FILE, Action.FILETOOL_EDIT_FILE])

# ===== Prompt Configuration =====
# System prompt defining the AI agent's role and capabilities
system_prompt = """
You are an AI Agent that has access to file tool. 
You can create, edit and read files in any directory.
Perform the action requested by the user.
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

# ===== Execute File Operations =====
# Handle tool calls to perform file operations
response_after_tool_calls = tool_set.handle_tool_calls(response=response)

# Print the result of the operation
print(response_after_tool_calls)
