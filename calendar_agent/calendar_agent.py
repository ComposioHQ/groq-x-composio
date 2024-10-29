# Import required libraries
from composio_openai import App, ComposioToolSet,Action
from datetime import datetime
from dotenv import load_dotenv
import os, groq

# load environment variables
load_dotenv()

# Initialize Groq client for LLM interaction
groq_client = groq.Groq(api_key=os.environ["GROQ_API_KEY"])
tool_set = ComposioToolSet()

# ===== Calendar Tasks Definition =====
# Define the schedule of tasks to be added to calendar
todo = """
    1PM - 3PM -> Code,
    5PM - 7PM -> Meeting,
    9AM - 12AM -> Learn something,
    8PM - 10PM -> Game
"""
# agent should book slots according to the todo

# ===== Date and Time Configuration =====
# Get current date in YYYY-MM-DD format and timezone
date = datetime.today().strftime("%Y-%m-%d")
timezone = datetime.now().astimezone().tzinfo

# ===== Tool and API Setup =====
# Initialize Composio tools for Google Calendar integration
tools = tool_set.get_tools(actions=[Action.GOOGLECALENDAR_CREATE_EVENT])

# ===== Prompt Configuration =====
# System prompt defining the AI agent's role
system_prompt = """
You are an AI agent responsible for taking actions on Google Calendar on users' behalf. You need to take action on Calendar using Google Calendar APIs. Use correct tools to run APIs from the given tool-set.
"""

# User prompt with specific scheduling instructions
user_prompt = f"""
Book slots according to {todo}. 
Properly Label them with the work provided to be done in that time period. 
Schedule it for today. 
Today's date is {date} (it's in YYYY-MM-DD format) and make the timezone be {timezone}.
"""

# Prepare messages for the LLM
messages = [{
    "role": "system",
    "content": system_prompt
}, {
    "role": "user",
    "content": user_prompt,
}]

# ===== LLM Interaction =====
# Get completion from Groq LLM
response = groq_client.chat.completions.create(
    model="llama-3.2-90b-text-preview",
    messages=messages, #type: ignore
    tools=tools, #type: ignore
    tool_choice="auto",
    max_tokens=8192,
)

# Handle tool calls to perform calendar operations
# it iterates over the tool calls and executes them
response_after_tool_calls = tool_set.handle_tool_calls(response=response) #type: ignore

# Print final response
print(response_after_tool_calls)
