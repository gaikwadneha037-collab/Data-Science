AutoStream: Agentic Sales & Support Assistant
AutoStream is an intelligent agentic system designed to handle pricing inquiries (via RAG) and capture high-intent leads (via Tool Calling). Powered by GPT-4o-mini and orchestrated with LangGraph, it moves beyond simple chatbots by managing a complex state-driven workflow.

How to Run Locally
1. Prerequisites
Python 3.10+

A GitHub Personal Access Token (for GPT-4o-mini access)

2. Installation
Clone the repository and install the dependencies:

pip install langgraph langchain-openai python-dotenv

3. Environment Setup
Create a .env file in the root directory and add your token:

GITHUB_TOKEN=ghp_your_token_here

4. Project Files
Ensure pricingData.json is present in the root folder with your service plans and policies.

5. Launch
python autoStream.py

Architecture Explanation
Why LangGraph?
I chose LangGraph over other frameworks like AutoGen because of its cyclical nature and fine-grained control. While AutoGen excels at multi-agent conversations, LangGraph is built on top of Pregel's graph processing, allowing for a structured, deterministic flow. This is critical for a sales agent where you need specific "guardrails"—ensuring the agent identifies intent before offering pricing, and validates data before calling a lead-capture tool.

State Management
State is managed through a central TypedDict called AgentState. Unlike standard LLM chains that only pass a string, this state acts as a persistent memory for the agent. It stores:

Message History: The full context of the conversation.

Lead Information: A structured dictionary that tracks which user details (Name, Email, Platform) have been collected.

Intent Flags: Metadata that tells the router where to move the user next.

This architecture allows the agent to be "interrupted" or "resumed." For example, if a user provides an invalid email, the state preserves the name and platform already collected, asking only for the corrected email rather than starting over.

------------------------------------------------------------------------------------------------

WhatsApp Deployment (Webhooks)
To move this agent from the terminal to WhatsApp, I would use a Twilio WhatsApp API or the Meta Business API integration via Webhooks.

Integration Workflow:
The Webhook: I would set up a FastAPI or Flask server that exposes a /webhook endpoint. When a user sends a message on WhatsApp, Meta/Twilio sends an HTTP POST request to this URL.

Processing: The server receives the JSON payload (containing the user's phone number and message). It uses the Phone Number as a Unique ID to retrieve that specific user's AgentState from a database (like Redis or PostgreSQL).

The Brain: The message is passed into the app.invoke(state) logic. The agent decides whether to pull from the RAG node or the Lead Capture node.

The Response: Once the agent generates a response, the server sends an API call back to the WhatsApp provider to deliver the message to the user's phone.

Key Features Included
Intent Classification: Automatically distinguishes between "just looking" and "ready to buy."

RAG Pipeline: Answers pricing questions using verified local JSON data.

Resilient LLM: Features a safe_llm wrapper with 3x retry logic for production stability.

Data Validation: Uses Regex to verify email formats before "storing" lead data.

https://github.com/user-attachments/assets/14ec3e62-abc9-49b3-a195-d308862beda7






