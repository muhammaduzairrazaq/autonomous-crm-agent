from langgraph.prebuilt import create_react_agent
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import json

# Load config
with open("config/config.json") as f:
    config = json.load(f)

sg = SendGridAPIClient(config["SENDGRID_ACCESSTOKEN"])

"""
Sends an email using SendGrid with the given subject and HTML-formatted body.
Reads sender and recipient addresses from the loaded config.
"""

def send_email(email_subject: str, email_body: str):
    """Send email"""

    message = Mail(
        from_email=config['FROM_EMAIL'],
        to_emails=config['TO_EMAIL'],
        subject=f'{email_subject}',
        html_content=f'<strong>{email_body}</strong>')
    try:
        # sg.set_sendgrid_data_residency("eu")
        # uncomment the above line if you are sending mail using a regional EU subuser
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

def get_email_agent():
    return create_react_agent(
        model="openai:gpt-4.1",
        tools=[send_email],
        prompt=(
            "You are a email agent.\n\n"
            "INSTRUCTIONS:\n"
            "- Assist ONLY with email related tasks\n"
            "- You will be called after the hubspot agent\n"
            "- Your job is to write an email considering the action performed by hubspot agent and based on the success and failure of that action\n"
            "- Dont ask from user what to write in the email just do it yourself\n"
            "- Remember your are not writing this email to the user its just a notification for admin to update him on the action that he is trying to perform so write the email subject and email body accordingly\n"
            "- After you're done with your tasks, respond to the supervisor directly\n"
            "- Respond ONLY with the results of your work, do NOT include ANY other text."
        ),
        name="email_agent",
    )
