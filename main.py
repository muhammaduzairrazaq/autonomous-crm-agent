import os
import json
from langchain_core.messages import convert_to_messages
from agents.hubspot_agent import get_hubspot_agent
from agents.email_agent import get_email_agent
from agents.supervisor_agent import get_supervisor


# Load config
with open("config/config.json") as f:
    config = json.load(f)

os.environ["OPENAI_API_KEY"] = config["OPENAI_API_KEY"]

# Create agents
hubspot_agent = get_hubspot_agent()
email_agent = get_email_agent()
supervisor = get_supervisor(hubspot_agent, email_agent)

# --- Printing functions ---
def pretty_print_message(message, indent=False):
    pretty_message = message.pretty_repr(html=True)
    print("\n".join("\t" + c if indent else c for c in pretty_message.split("\n")))

def pretty_print_messages(update, last_message=False):
    is_subgraph = isinstance(update, tuple)
    if is_subgraph:
        ns, update = update
        if len(ns) == 0:
            return
        print(f"Update from subgraph {ns[-1].split(':')[0]}:\n")

    for node_name, node_update in update.items():
        print(f"{'Update from node ' + node_name}:\n")
        messages = convert_to_messages(node_update["messages"])
        for m in messages[-1:] if last_message else messages:
            pretty_print_message(m, indent=is_subgraph)
        print()

# --- Interaction loop ---
while True:
    user_input = input("Hey! what you want me to do now (enter 'exit' to stop): ")
    if user_input.lower() == 'exit':
        break

    for chunk in supervisor.stream({"messages": [{"role": "user", "content": user_input}]}):
        pretty_print_messages(chunk, last_message=True)

    final_message_history = chunk["supervisor"]["messages"]
