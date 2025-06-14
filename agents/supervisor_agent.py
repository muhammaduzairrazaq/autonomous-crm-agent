from langgraph_supervisor import create_supervisor
from langchain.chat_models import init_chat_model

"""
Creates and compiles a supervisor agent that coordinates a HubSpot agent and an email agent.
Ensures sequential task delegation, assigning CRM tasks to the HubSpot agent first,
then notifying via the email agent based on the HubSpot agent’s actions.
"""

def get_supervisor(hubspot_agent, email_agent):
    return create_supervisor(
        model=init_chat_model("openai:gpt-4.1"),
        agents=[hubspot_agent, email_agent],
        prompt=(
            "You are a supervisor managing two agents:\n"
            "- a hubspot agent. Assign crm related tasks to this agent\n"
            "- a email agent. Call this agent only after the hubspot agent has performed an action\n"
            "Assign work to one agent at a time, do not call agents in parallel.\n"
            "Do not do any work yourself."
        ),
        add_handoff_back_messages=True,
        output_mode="full_history",
    ).compile()
