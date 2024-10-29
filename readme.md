# AI Agent Toolkit

This repository contains a collection of AI agents built using the Composio SDK and Groq LLM to automate various tasks.

## Agents

### Email Agent
Located in `email_agent/`, this agent can:
- Write and send emails based on user input
- Integrates with Gmail using Composio tools
- Uses Groq LLM for natural language email composition

### Newsletter Summarizer
Located in `newsletter_summariser_agent/`, this agent:
- Fetches newsletter emails from Gmail
- Summarizes content using Groq LLM
- Posts summaries to Slack channels automatically

### Coding Agent
Located in `coding_agent/`, this agent can:
- Create and edit files programmatically
- Execute coding tasks based on natural language instructions
- Uses file operation tools from Composio

### Calendar Agent 
Located in `calendar_agent/`, this agent:
- Handles Google Calendar authentication
- Provides OAuth flow for calendar access
- Manages calendar operations through Composio SDK

## Setup

1. Clone this repository
2. Create a `.env` file with the following keys:
   ```
   COMPOSIO_API_KEY=your_composio_key
   GROQ_API_KEY=your_groq_key
   ```
3. Create a virtual environment and install dependencies:
    ```bash
    python -m venv venv 
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## Usage

Each agent is contained in its own directory with a dedicated Python script.
