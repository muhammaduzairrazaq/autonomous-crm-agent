from langgraph.prebuilt import create_react_agent
import hubspot
from pprint import pprint
from hubspot.crm.contacts import SimplePublicObjectInputForCreate, ApiException
from hubspot.crm.contacts import SimplePublicObjectInput
import json

# Load config
with open("config/config.json") as f:
    config = json.load(f)

client = hubspot.Client.create(access_token=config["HUBSPOT_ACCESSTOKEN"])

"""
Creates a new deal in HubSpot using the specified details.

Parameters:
- amount (str): The monetary value of the deal.
- dealname (str): The name of the deal.
- dealstage (str): The stage of the deal (default is "closedwon").
- pipeline (str): The pipeline where the deal is tracked (default is "default").

Returns:
- str: Success message with the deal ID or an error message.
"""

def create_deal(amount: str, dealname: str, dealstage: str = "closedwon", pipeline: str = "default"):
    """Create a new deal on HubSpot"""

    properties = {
        "amount": amount,
        "dealname": dealname,
        "dealstage": dealstage,
        "pipeline": pipeline,
    }

    simple_public_object_input_for_create = SimplePublicObjectInputForCreate(properties=properties)

    try:
        api_response = client.crm.deals.basic_api.create(
            simple_public_object_input_for_create=simple_public_object_input_for_create
        )
        return f"Deal '{dealname}' created successfully with ID: {api_response.id}"
    except ApiException as e:
        return f"Failed to create deal '{dealname}': {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred while creating the deal: {str(e)}"

"""
Updates an existing deal in HubSpot with the provided details.

Parameters:
- deal_id (str): The unique ID of the deal to update.
- amount (str): Updated amount for the deal.
- dealname (str): Updated deal name.
- dealstage (str): Updated deal stage (default is "closedwon").
- pipeline (str): Updated pipeline (default is "default").

Returns:
- str: Success message with the deal ID or an error message.
"""

def update_deal(deal_id: str, amount: str, dealname: str, dealstage: str = "closedwon", pipeline: str = "default"):
    """Update an existing deal on HubSpot"""

    properties = {
        "amount": amount,
        "dealname": dealname,
        "dealstage": dealstage,
        "pipeline": pipeline,
    }

    simple_public_object_input = SimplePublicObjectInput(properties=properties)

    try:
        api_response = client.crm.deals.basic_api.update(
            deal_id=deal_id,
            simple_public_object_input=simple_public_object_input
        )
        return f"Deal '{dealname}' (ID: {deal_id}) updated successfully."
    except ApiException as e:
        return f"Failed to update deal (ID: {deal_id}): {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred while updating the deal: {str(e)}"

"""
Creates a new contact in HubSpot with the specified information.

Parameters:
- email (str): Contact's email address.
- lastname (str): Contact's last name.
- firstname (str): Contact's first name.
- phone (str): Contact's phone number.

Returns:
- str: Success message with the contact ID or an error message.
"""

def create_contact(email: str, lastname: str, firstname: str, phone: str):
    """Create contact on HubSpot"""

    properties = {
        "email": email,
        "lastname": lastname,
        "firstname": firstname,
        "phone": phone
    }

    simple_public_object_input_for_create = SimplePublicObjectInputForCreate(properties=properties)

    try:
        api_response = client.crm.contacts.basic_api.create(
            simple_public_object_input_for_create=simple_public_object_input_for_create
        )
        return f"Contact '{firstname} {lastname}' created successfully with ID: {api_response.id}"
    except ApiException as e:
        return f"Failed to create contact: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

"""
Updates an existing contact in HubSpot based on contact ID and provided data.

Parameters:
- email (str): Updated email address.
- lastname (str): Updated last name.
- firstname (str): Updated first name.
- phone (str): Updated phone number.
- id (str): Contact ID to identify the contact to update.

Returns:
- str: Success message with contact ID or an error message.
"""

def update_contact(email: str, lastname: str, firstname: str, phone: str, id: str):
    """Update contact on HubSpot"""

    properties = {
        "email": email,
        "lastname": lastname,
        "firstname": firstname,
        "phone": phone
    }

    simple_public_object_input = SimplePublicObjectInput(properties=properties)

    try:
        api_response = client.crm.contacts.basic_api.update(
            contact_id=id,
            simple_public_object_input=simple_public_object_input
        )
        return f"Contact '{firstname} {lastname}' (ID: {id}) updated successfully."
    except ApiException as e:
        return f"Failed to update contact (ID: {id}): {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred while updating contact: {str(e)}"

"""
Initializes and returns a LangGraph ReAct agent configured for HubSpot CRM operations.

The agent can handle:
- Creating and updating contacts.
- Creating and updating deals.

Returns:
- A configured LangGraph agent for CRM tasks with embedded prompt instructions.
"""

def get_hubspot_agent():
    return create_react_agent(
        model="openai:gpt-4.1",
        tools=[create_contact, update_contact, create_deal, update_deal],
        prompt=(
            "You are a hubspot agent.\n\n"
            "INSTRUCTIONS:\n"
            "- Assist ONLY with crm related tasks create/update contact/deal\n"
            "- If the user asks you to update a contact/deal always ask the contact/deal id for identifying the contact/deal and then ask for the details that the user wants to update like email, first name, last name, phone you should also be able to update any one detail at a time\n"
            "- Perform basic checks for email and phone number, amount it should be in correct format\n"
            "- After you're done with your tasks, respond to the supervisor directly\n"
            "- Respond ONLY with the results of your work, do NOT include ANY other text."
        ),
        name="hubspot_agent",
    )

