import os
import pandas as pd
# from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import tool
from datetime import datetime

# Load environment
# load_dotenv()
api_key = 'AIzaSyBZ4JkMlnKCluUlN1XNJM_VQU_sszF9VMw'

if not api_key:
    print("❌ ERROR: Add GEMINI_API_KEY to .env file!")
    exit(1)

# Initialize Gemini
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", google_api_key=api_key , convert_system_message_to_human=True)

# CSV Storage
CONTACTS_FILE = "contacts.csv"
if not os.path.exists(CONTACTS_FILE):
    pd.DataFrame(columns=["name", "email", "notes", "last_interaction"]).to_csv(CONTACTS_FILE, index=False)

@tool
def add_contact(name: str, email: str) -> str:
    """Add a new contact to the CRM. Format: name, email"""
    df = pd.read_csv(CONTACTS_FILE)
    notes = "New lead"
    new_row = {
        "name": name, 
        "email": email, 
        "notes": notes,
        "last_interaction": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(CONTACTS_FILE, index=False)
    return f"✅ Added: {name} ({email})"

@tool
def get_contacts() -> str:
    """Get all contacts from CRM."""
    df = pd.read_csv(CONTACTS_FILE)
    if df.empty:
        return "📝 No contacts yet."
    return df.to_string(index=False)

@tool
def update_notes(name: str, notes: str) -> str:
    """Update notes for existing contact."""
    df = pd.read_csv(CONTACTS_FILE)
    if name in df["name"].values:
        df.loc[df["name"] == name, "notes"] = notes
        df.loc[df["name"] == name, "last_interaction"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        df.to_csv(CONTACTS_FILE, index=False)
        return f"📝 Updated notes for {name}"
    return f"❌ Contact '{name}' not found"

@tool
def search_contact(name: str) -> str:
    """Search for a specific contact by name."""
    df = pd.read_csv(CONTACTS_FILE)
    match = df[df["name"].str.contains(name, case=False, na=False)]
    if match.empty:
        return f"❌ No contact found with '{name}'"
    return match.to_string(index=False)

# **PERFECT WORKING AGENT**
tools = [add_contact, get_contacts, update_notes, search_contact]
agent = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    handle_parsing_errors=True
)

# Run
print("🤖 AI CRM Agent Started!")
print("Try: 'Add John Doe, john@email.com' or 'Show all contacts' or 'exit'")

while True:
    query = input("\n💬 You: ").strip()
    if query.lower() in ['exit', 'quit', 'bye']:
        print("👋 Goodbye!")
        break
    if not query:
        continue
    response = agent.run(query)
    print(f"\n🤖 Agent: {response}\n")