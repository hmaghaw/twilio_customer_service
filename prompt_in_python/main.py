import os
import json
import openai
from datetime import datetime

# 1. Configure OpenAI API key
openai.api_key = "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"
# 4. Build the “system” prompt (inject TODAY’S date)
TODAY = datetime.now().strftime("%Y-%m-%d")
SYSTEM_PROMPT = f"""
Today is: {TODAY}
You are a professional, friendly, and efficient AI-powered customer service agent for IdeationMax Dental Clinic.
You handle calls based on these scenarios:
- New Patient
- Existing Patient
- Book Appointment
- Modify Appointment
- Cancel Appointment
- Update Patient Information
- Service Inquiry

You have access to the following Python helper functions (tools). 
When you want to call a tool, respond with JSON of the form:
{{ "tool": "<ToolName>", "input": {{ ... }} }}

Otherwise, respond with natural language to guide the caller.

Tools:
1. CreatePatient(full_name, phone, email, dob, notes)
   Returns: {{ "success": true, "message": "Patient created." }}

2. GetPatientByPhone(phone_number)
   Returns: {{ "full_name": "...", "phone": "...", "email": "...", "dob": "YYYY-MM-DD", "notes": "..." }}
   If no record, return an empty object.

3. ModifyPatient(phone, full_name (optional), email (optional))
   Returns: {{ "success": true/false, "message": "..." }}

4. CreateAppointment(phone, date, time, dentist_name (optional))
   Returns: {{ "success": true, "message": "Appointment created." }}

5. ListAppointmentsByPhone(phone)
   Returns: a list of appointments:
      [ {{ "date": "YYYY-MM-DD", "time": "HH:MM", "dentist_name": "..." }}, ... ]

6. CancelAppointmentByPhone(phone, date, time)
   Returns: {{ "success": true, "message": "Appointment cancelled." }}

7. RescheduleAppointmentByPhone(phone, date, time, new_date, new_time, notes (optional))
   Returns: {{ "success": true, "message": "Appointment rescheduled." }}

8. GetAvailableTimeSlots(date, operator, time)
   Returns: a list of slots:
      [ {{ "date": "YYYY-MM-DD", "time": "HH:MM" }}, ... ]

Initial greeting each call must start:
  “Hello! Thank you for calling IdeationMax Dental Clinic. How can I help you today?”

Classify intents by caller’s phrasing:
- New Patient → “I’m a new patient” / “I need to register”
- Existing Patient → “I already have an appointment” / “I’m an existing patient”
- Book Appointment → “I want to book an appointment”
- Modify Appointment → “I need to change my appointment”
- Cancel Appointment → “I need to cancel my appointment”
- Service Inquiry → “What services do you offer?”
- Update Patient Info → “My email/phone has changed”

For each intent, follow the scripted steps as described in the n8n specification.
"""



# 2. Define “tool” stubs (replace with your actual implementations)

def CreatePatient(full_name: str, phone: str, email: str, dob: str, notes: str = "") -> dict:
    """
    Stub: create a new patient record in your database.
    Return example: { "success": True, "message": "Patient created." }
    """
    # TODO: insert into your DB or call your REST endpoint
    return {"success": True, "message": "Patient created."}


def GetPatientByPhone(phone_number: str) -> dict:
    """
    Stub: look up a patient by phone.
    Return example:
      {
        "full_name": "John Doe",
        "phone": "6471234567",
        "email": "john@example.com",
        "dob": "1990-01-01",
        "notes": "Has allergies"
      }
    """
    # TODO: query your DB or call your REST endpoint
    # If not found, return {} or raise an error
    return {
        "full_name": "John Doe",
        "phone": phone_number,
        "email": "john@example.com",
        "dob": "1990-01-01",
        "notes": "Has allergies"
    }


def ModifyPatient(phone: str, full_name: str = None, email: str = None) -> dict:
    """
    Stub: update patient’s name or email.
    Return HTTP 200 on success, or { "success": False, "message": "..."} on error.
    """
    # TODO: perform update in your DB or via REST
    return {"success": True, "message": "Patient modified."}


def CreateAppointment(phone: str, date: str, time: str, dentist_name: str = "") -> dict:
    """
    Stub: create a new appointment.
    Return example: { "success": True, "message": "Appointment created." }
    """
    # TODO: insert appointment into DB or call REST
    return {"success": True, "message": "Appointment created."}


def ListAppointmentsByPhone(phone: str) -> list[dict]:
    """
    Stub: return a list of upcoming appointments for this phone.
    Example:
      [
        { "date": "2025-06-05", "time": "10:30", "dentist_name": "Dr. Smith" },
        { "date": "2025-06-12", "time": "14:00", "dentist_name": "Dr. Lee" }
      ]
    """
    # TODO: query your DB
    return [
        {"date": "2025-06-05", "time": "10:30", "dentist_name": "Dr. Smith"},
        {"date": "2025-06-12", "time": "14:00", "dentist_name": "Dr. Lee"},
    ]


def CancelAppointmentByPhone(phone: str, date: str, time: str) -> dict:
    """
    Stub: cancel the specified appointment.
    Return example: { "success": True, "message": "Appointment cancelled." }
    """
    # TODO: delete or mark appointment as cancelled
    return {"success": True, "message": "Appointment cancelled."}


def RescheduleAppointmentByPhone(
        phone: str,
        date: str,
        time: str,
        new_date: str,
        new_time: str,
        notes: str = ""
) -> dict:
    """
    Stub: reschedule an existing appointment.
    Return example: { "success": True, "message": "Appointment rescheduled." }
    """
    # TODO: update the appointment record in your DB
    return {"success": True, "message": "Appointment rescheduled."}


def GetAvailableTimeSlots(date: str, operator: str, time: str) -> list[dict]:
    """
    Stub: return available time slots after the given time on a date.
    Example output:
      [
        { "date": "2025-06-05", "time": "10:30" },
        { "date": "2025-06-06", "time": "11:00" },
        { "date": "2025-06-07", "time": "09:00" }
      ]
    """
    # TODO: query your scheduling logic or DB
    return [
        {"date": date, "time": "10:30"},
        {"date": date, "time": "11:00"},
        {"date": date, "time": "14:00"},
    ]

# 3. Helper to call OpenAI ChatCompletion
def call_openai_chat(messages: list[dict], model: str = "gpt-4o", temperature: float = 0.0) -> str:
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content



# 5. Orchestration example: process a single user input
def handle_incoming_message(from_phone: str, user_text: str):
    """
    Simulate a single-turn conversation:
    - Look up patient by phone
    - Send context + user_text to GPT
    - If GPT responds with {"tool": "...", "input": {...}}, dispatch to the tool
    - Otherwise, return GPT’s natural-language response
    """
    # Step 1: fetch patient data (if any)
    patient = GetPatientByPhone(from_phone)
    patient_json = json.dumps(patient) if patient else "{}"

    # Step 2: build message list
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "assistant",
            "content": f"Caller’s phone number: {from_phone}\n"
                       f"Patient record: {patient_json}\n"
                       f"Next, user says:"
        },
        {"role": "user", "content": user_text}
    ]

    # Step 3: call OpenAI
    gpt_reply = call_openai_chat(messages)

    # Step 4: attempt to parse tool call
    try:
        reply_obj = json.loads(gpt_reply)
        tool_name = reply_obj.get("tool")
        tool_input = reply_obj.get("input", {})

        if tool_name == "CreatePatient":
            result = CreatePatient(
                full_name=tool_input["full_name"],
                phone=tool_input["phone"],
                email=tool_input["email"],
                dob=tool_input["dob"],
                notes=tool_input.get("notes", "")
            )
            return {"tool_result": result}

        if tool_name == "GetPatientByPhone":
            result = GetPatientByPhone(tool_input["phone_number"])
            return {"tool_result": result}

        if tool_name == "ModifyPatient":
            result = ModifyPatient(
                phone=tool_input["phone"],
                full_name=tool_input.get("full_name"),
                email=tool_input.get("email")
            )
            return {"tool_result": result}

        if tool_name == "CreateAppointment":
            result = CreateAppointment(
                phone=tool_input["phone"],
                date=tool_input["date"],
                time=tool_input["time"],
                dentist_name=tool_input.get("dentist_name", "")
            )
            return {"tool_result": result}

        if tool_name == "ListAppointmentsByPhone":
            result = ListAppointmentsByPhone(tool_input["phone"])
            return {"tool_result": result}

        if tool_name == "CancelAppointmentByPhone":
            result = CancelAppointmentByPhone(
                phone=tool_input["phone"],
                date=tool_input["date"],
                time=tool_input["time"]
            )
            return {"tool_result": result}

        if tool_name == "RescheduleAppointmentByPhone":
            result = RescheduleAppointmentByPhone(
                phone=tool_input["phone"],
                date=tool_input["date"],
                time=tool_input["time"],
                new_date=tool_input["new_date"],
                new_time=tool_input["new_time"],
                notes=tool_input.get("notes", "")
            )
            return {"tool_result": result}

        if tool_name == "GetAvailableTimeSlots":
            result = GetAvailableTimeSlots(
                date=tool_input["date"],
                operator=tool_input["operator"],
                time=tool_input["time"]
            )
            return {"tool_result": result}

        # If no recognized tool, return GPT’s text
        return {"response": gpt_reply}

    except json.JSONDecodeError:
        # Not a JSON tool call → normal response
        return {"response": gpt_reply}


# 6. Example usage
if __name__ == "__main__":
    # Simulate Twilio webhook by reading from stdin or hardcode for testing
    test_phone = "+16471234567"
    test_user_text = "I want to book an appointment"

    output = handle_incoming_message(test_phone, test_user_text)
    if "tool_result" in output:
        print("Tool result:", output["tool_result"])
    else:
        print("AI response:", output["response"])
