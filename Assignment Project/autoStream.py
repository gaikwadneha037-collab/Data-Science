import os
import re
import json
import time
from typing import TypedDict, Annotated, List, Optional

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
# --- CHANGED: Use OpenAI instead of Google ---
from langchain_openai import ChatOpenAI 
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool

# ----------------------
# 1. TOOL
# ----------------------
@tool
def mock_lead_capture(name: str, email: str, platform: str):
    """
    Capture user lead details including name, email, and platform.
    Only call this when all fields are available.
    """
    print(f"Lead captured successfully: {name}, {email}, {platform}")
    return "✅ Lead stored successfully!"

# ----------------------
# 2. STATE
# ----------------------
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "chat history"]
    lead_info: dict
    intent: Optional[str]
    tool_called: bool

# ----------------------
# 3. SETUP
# ----------------------
load_dotenv()

# --- CHANGED: Point to GitHub's GPT-4o-mini endpoint ---
llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("GITHUB_TOKEN"),      # Ensure GITHUB_TOKEN is in your .env
    base_url="https://models.github.ai/inference",
    temperature=0.2
)

# ----------------------
# 4. SYSTEM PROMPT
# ----------------------
BASE_SYSTEM = SystemMessage(content="""
You are Autostream AI Assistant.

Rules:
- Answer ONLY using provided pricing data
- Be concise and clear
- If user shows interest → collect Name, Email, Platform
- DO NOT call any tool yourself
""")

# ----------------------
# 5. HELPERS
# ----------------------
def classify_intent(text: str) -> str:
    text = text.lower()
    if any(x in text for x in ["price", "cost", "plan"]):
        return "pricing"
    elif any(x in text for x in ["try", "buy", "sign up", "register"]):
        return "signup"
    elif any(x in text for x in ["hi", "hello"]):
        return "greeting"
    return "unknown"


def extract_lead_info(text: str):
    text_lower = text.lower()

    name_match = re.search(r"(?:name is|i am|i'm)\s+(\w+)", text_lower)
    email_match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    platform_match = re.search(r"(youtube|instagram|tiktok)", text_lower)

    return {
        "name": name_match.group(1) if name_match else None,
        "email": email_match.group(0) if email_match else None,
        "platform": platform_match.group(1) if platform_match else None
    }


def is_valid_email(email: str) -> bool:
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))


def safe_llm(messages):
    for _ in range(3):
        try:
            return llm.invoke(messages)
        except Exception as e:
            print("Retrying due to:", e)
            time.sleep(3)
    return SystemMessage(content="⚠️ System busy. Please try again.")

# ----------------------
# 6. NODES
# ----------------------
def intent_node(state: AgentState):
    last = state["messages"][-1].content
    return {"intent": classify_intent(last)}


def rag_node(state: AgentState):
    with open("pricingData.json", "r") as f:
        kb = json.load(f)

    plans = kb["plans"]
    policies = kb["policies"]

    context = f"""
Plans:
{plans}

Policies:
{policies}
"""

    system_prompt = SystemMessage(content=f"Use ONLY this data:\n{context}")

    response = safe_llm([BASE_SYSTEM, system_prompt] + state["messages"])
    return {"messages": [response]}


def lead_node(state: AgentState):
    last_msg = state["messages"][-1].content
    extracted = extract_lead_info(last_msg)

    lead_info = state.get("lead_info", {})
    lead_info.update({k: v for k, v in extracted.items() if v})

    required = ["name", "email", "platform"]
    missing = [k for k in required if not lead_info.get(k)]

    if missing:
        return {
            "lead_info": lead_info,
            "messages": [SystemMessage(content=f"Please provide your {', '.join(missing)}.")]
        }

    if not is_valid_email(lead_info["email"]):
        return {
            "messages": [SystemMessage(content="Invalid email. Please enter a valid email.")]
        }

    return {
        "lead_info": lead_info,
        "tool_called": True
    }


def tool_node(state: AgentState):
    info = state["lead_info"]
    result = mock_lead_capture.invoke(info)

    return {
        "messages": [SystemMessage(content=result)],
        "tool_called": False  # reset
    }


def default_node(state: AgentState):
    response = safe_llm([BASE_SYSTEM] + state["messages"])
    return {"messages": [response]}

# ----------------------
# 7. ROUTERS
# ----------------------
def router(state: AgentState):
    if state["intent"] == "pricing":
        return "rag"
    elif state["intent"] == "signup":
        return "lead"
    return "default"


def lead_router(state: AgentState):
    if state.get("tool_called"):
        return "tool"
    return END

# ----------------------
# 8. GRAPH
# ----------------------
workflow = StateGraph(AgentState)

workflow.add_node("intent", intent_node)
workflow.add_node("rag", rag_node)
workflow.add_node("lead", lead_node)
workflow.add_node("tool", tool_node)
workflow.add_node("default", default_node)

workflow.set_entry_point("intent")

workflow.add_conditional_edges("intent", router, {
    "rag": "rag",
    "lead": "lead",
    "default": "default"
})

workflow.add_edge("rag", END)
workflow.add_edge("default", END)

workflow.add_conditional_edges("lead", lead_router, {
    "tool": "tool",
    END: END
})

workflow.add_edge("tool", END)

app = workflow.compile()

# ----------------------
# 9. RUN
# ----------------------
if __name__ == "__main__":
    state = {
        "messages": [],
        "lead_info": {},
        "intent": None,
        "tool_called": False
    }

    print("🚀 Agent started (Powered by GPT-4o-mini). Type 'exit' to quit.\n")

    while True:
        user_input = input("User: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        state["messages"].append(HumanMessage(content=user_input))

        output = app.invoke(state)

        print("Agent:", output["messages"][-1].content)

        state.update(output)