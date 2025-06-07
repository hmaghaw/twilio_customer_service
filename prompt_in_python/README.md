# Patient Service Tools

A Python client and conversational agent demonstrating how to integrate OpenAI with HTTP-backed “tools.” This example shows:

- Defining API-driven tools in code  
- Describing those tools in a system prompt  
- Letting GPT decide when and how to call each tool via JSON “tool invocation”  
- Maintaining conversation state and dispatching calls  

---

## Table of Contents

1. [Prerequisites](#prerequisites)  
2. [Configuration](#configuration)  
3. [How It Works](#how-it-works)  
4. [Agent Prompt & Tool Protocol](#agent-prompt--tool-protocol)  
5. [Tool Methods](#tool-methods)  
6. [Conversation Loop](#conversation-loop)  
7. [Getting Started](#getting-started)  
8. [Extension Guide](#extension-guide)  

---

## Prerequisites

- Python 3.7+  
- `requests`  
- `openai`  
- Set your OpenAI API key in the environment:

```bash
pip install requests openai
export OPENAI_API_KEY="sk-…"
```

---

## Configuration

- **`BASE_URL`**:  
  The root URL for the dental-clinic API.  
  ```python
  BASE_URL = "https://coffeehome.ca/api/dental_clinic"
  ```
- **`system_prompt_2.txt`**:  
  Contains the body of your system prompt (tool descriptions, behavior guidelines). Place it alongside your code.

---

## How It Works

1. **Tool Definitions in Code**  
   Each API endpoint is wrapped in a method that handles HTTP calls and JSON parsing.

2. **Static Variables Injection**  
   On initialization, patient data is fetched by phone, and static context variables (`full_name`, `phone`, `email`, `TODAY`) are prepended to the system prompt.

3. **Message Buffer**  
   Maintains a list of `{ role: system|user|assistant, content: ... }` messages for full context.

4. **Agent Pattern / Tool Invocation**  
   The system prompt instructs the model to emit **only** a JSON object when it wants to call a tool, e.g.:

   ```json
   {"tool":"CreateAppointment","input":{"date":"2025-06-15","time":"14:30"}}
   ```

   Otherwise, it replies in natural language.

5. **Dispatch & Response Handling**  
   - `handle_incoming_message()` appends the user’s message, calls OpenAI, attempts `json.loads()` on the reply, dispatches to the matching method if a `"tool"` field is present, or returns a plain-text response.

6. **State Updates**  
   Methods like `ModifyPatient` update in-memory attributes so subsequent prompts see fresh data.

---

## Agent Prompt & Tool Protocol

**System Prompt** (loaded from `system_prompt_2.txt`) is prefixed with:

\`\`\`
You are an AI assistant for CoffeeHome Dental Clinic. You have access to the following “tools” (Python methods) to look up and manage patient records and appointments. Use these tools whenever needed to fulfil the user’s request.

When you want to call a tool, you must output **only** a JSON object in this exact format and then stop:
{
  "tool": "<ToolName>",
  "input": {
    <parameter_name>: <value>,
    …
  }
}

The host application will run that tool and return the result. After the tool result is provided, continue your reasoning or final answer normally.

If you do not need to call a tool, respond in natural language without JSON.

––––––––––––––––––––––––––––––––––––––––––
STATIC VARIABLES (already defined before this prompt runs):
full_name:  "{full_name}"
phone:      "{phone}"
email:      "{email}"
TODAY:      {TODAY}

These variables are available for you to reference directly.

––––––––––––––––––––––––––––––––––––––––––
PERSONALIZED GREETING:
If **full_name** is non-empty, begin your first response with:
“Hi {full_name}, how can I help you today?”
Otherwise, start with:
“Hello! How can I assist you today?”
––––––––––––––––––––––––––––––––––––––––––

AVAILABLE TOOLS:
1. CreatePatient – Create a new patient record. Input: `{}`  
2. GetPatientByPhone – Look up patient by phone. Input: `{}`  
3. ModifyPatient – Update name/email. Input: `{"full_name":…,"email":…}`  
4. CreateAppointment – Schedule appointment. Input: `{"date":"YYYY-MM-DD","time":"HH:MM"}`  
5. ListAppointmentsByPhone – List upcoming appointments. Input: `{}`  
6. CancelAppointmentByPhone – Cancel appointment. Input: `{"date":"YYYY-MM-DD","time":"HH:MM"}`  
7. RescheduleAppointmentByPhone – Reschedule appointment. Input: `{"date":…,"time":…,"new_date":…,"new_time":…,"notes":…}`  
8. GetAvailableTimeSlots – Fetch next slots. Input: `{"date":…,"operator":…,"time":…}`  

––––––––––––––––––––––––––––––––––––––––––
USAGE GUIDELINES:
- Output tool-call JSON **only** when invoking a tool.  
- Do **not** wrap JSON in extra text. After emitting it, stop.  
- Wait for the host to return results, then continue.  
- Otherwise, answer in plain language.

Begin now.
\`\`\`

---

## Tool Methods

| Method                            | HTTP Endpoint                                | Description                                 |
|-----------------------------------|----------------------------------------------|---------------------------------------------|
| `CreatePatient()`                 | `POST /patients`                             | Register a new patient                     |
| `GetPatientByPhone()`             | `GET /patients/{phone}`                      | Retrieve patient details                   |
| `ModifyPatient(...)`              | `PUT /patients/modify`                       | Update the patient’s name/email            |
| `CreateAppointment(...)`          | `POST /appointments`                         | Schedule an appointment                    |
| `ListAppointmentsByPhone()`       | `POST /appointments/list/by_phone`           | List upcoming appointments                 |
| `CancelAppointmentByPhone(...)`   | `DELETE /appointments/cancel/by_phone`       | Cancel an appointment                      |
| `RescheduleAppointmentByPhone(...)` | `PUT /appointments/reschedule/by_phone`     | Reschedule an appointment                  |
| `GetAvailableTimeSlots(...)`      | `POST /schedule/available`                   | Fetch next available time slots            |

---

## Conversation Loop

\`\`\`python
from patient_service_tools import PatientServiceTools

tools = PatientServiceTools(from_phone="6476248506")

while True:
    user_text = input("You: ").strip()
    output = tools.handle_incoming_message(user_text)
    if "tool_result" in output:
        print("Tool result:", output["tool_result"])
    else:
        print("AI response:", output["response"])
\`\`\`

---

## Getting Started

1. Copy this module into your project.  
2. Install dependencies and export your OpenAI API key.  
3. Ensure `system_prompt_2.txt` is present.  
4. Run the CLI example or integrate `PatientServiceTools` into your app.

---

## Extension Guide

- **Add a New Tool**  
  1. Write a new method for the endpoint.  
  2. Document it in the system prompt.  
  3. Add a dispatch case in `handle_incoming_message()`.

- **Refine GPT Behavior**  
  - Edit `system_prompt_2.txt`.  
  - Tweak model parameters in `call_openai_chat()`.

- **Enhance Error Handling**  
  - Add retries, logging, and robust JSON/failure handling.

This pattern empowers GPT to orchestrate API calls while your code handles data flow and business logic.
