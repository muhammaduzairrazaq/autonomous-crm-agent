# 🧠 CRM Assistant with LangChain & LangGraph

A modular, intelligent CRM automation assistant built using [LangChain](https://www.langchain.com/) and [LangGraph](https://www.langgraph.dev/). This assistant can manage HubSpot CRM operations (create/update contacts and deals) and send follow-up email notifications using SendGrid—all orchestrated by a Supervisor agent.

## 🚀 Features

- ✅ **HubSpot CRM Integration**
  - Create/update **contacts**
  - Create/update **deals**
  - Validates inputs (email, phone, amount)
  
- 📧 **Email Notifications via SendGrid**
  - Sends follow-up emails to an admin after CRM actions are performed
  - Fully automated; requires no user input for email content

- 🤖 **Supervisor Agent (LangGraph)**
  - Routes tasks between the CRM and Email agents
  - Ensures actions are performed sequentially and correctly
  - Full interaction traceability with streaming message updates

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/crm-assistant.git
cd crm-assistant
````

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Create a file at `config/config.json` with the following structure:

```json
{
  "OPENAI_API_KEY": "your_openai_key_here",
  "HUBSPOT_ACCESSTOKEN": "your_hubspot_token_here",
  "SENDGRID_ACCESSTOKEN": "your_sendgrid_token_here",
  "FROM_EMAIL": "your_verified_sender_email",
  "TO_EMAIL": "admin_recipient_email"
}
```

> 🔐 Add `config/config.json` to `.gitignore` to keep credentials secure.

### 4. Run the Assistant

```bash
python main.py
```

You’ll be prompted with:

```
Hey! what you want me to do now (enter 'exit' to stop):
```

Start giving natural-language commands like:

* "Create a contact with name John Doe and email [john@example.com](mailto:john@example.com)"
* "Update deal with ID 12345 and change the amount to 5000"

---

## 🧠 How It Works

1. **User Input** → sent to **Supervisor Agent**
2. Supervisor chooses:

   * `hubspot_agent` for CRM-related actions
   * `email_agent` to notify after CRM actions
3. Supervisor ensures **step-by-step coordination**, never executing agents in parallel
4. Email agent sends a formatted admin update using SendGrid

---

## 📦 Dependencies

See `requirements.txt`, which includes:

* `langchain`
* `langgraph`
* `hubspot-api-client`
* `sendgrid`
* `openai`

---

## 📄 License

MIT License. Feel free to use, modify, and build on top of this project.

---

## 🙌 Credits

Built by [Uzair Razzaq](mailto:muhammaduzairrazaq@gmail.com) using the power of LangChain, LangGraph, and modern cloud APIs.
