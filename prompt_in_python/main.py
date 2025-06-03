import json
import requests
import openai
from datetime import datetime

# 1. Configure OpenAI API key
openai.api_key = "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"
# 4. Build the “system” prompt (inject TODAY’S date)


BASE_URL = "https://coffeehome.ca/api/dental_clinic"

class PatientServiceTools:
    def __init__(self, from_phone):
        """
        Initialize the service with a customer's information.
        """
        self.messages = []
        self.phone = from_phone
        res = self.GetPatientByPhone()

        self.full_name = res['full_name']
        self.email = res['email']
        self.dob = res['dob']
        self.notes = res['notes']
        today = datetime.now().strftime("%Y-%m-%d")
        prompt_variables = f"""# Customer Service Prompt Template

# Static Variables (define these before running the prompt)
full_name: "{self.full_name}"
phone: "{from_phone}"
email: "{self.email}"
TODAY: {today}

---
        """

        with open("system_prompt_2.txt", "r", encoding="utf-8") as f:
            system_prompt_body = f.read()
        system_prompt = prompt_variables+system_prompt_body
        self.add_message("system", system_prompt)

        pass

    def CreatePatient(self) -> dict:
        """
        Create a new patient record via the API.
        POST /patients
        Body:
        {
          "full_name": ...,
          "phone": ...,
          "email": ...,
          "dob": ...,
          "notes": ...
        }
        """
        url = f"{BASE_URL}/patients"
        payload = {
            "full_name": self.full_name,
            "phone": self.phone,
            "email": self.email,
            "dob": self.dob,
            "notes": self.notes
        }
        resp = requests.post(url, json=payload)
        try:
            return resp.json()
        except ValueError:
            return {"success": False, "message": f"Invalid JSON response: {resp.text}"}

    def GetPatientByPhone(self) -> dict:
        """
        Look up a patient by phone number via the API.
        GET /patients/<phone_number>
        """
        url = f"{BASE_URL}/patients/{self.phone}"
        resp = requests.get(url)
        if resp.status_code == 200:
            try:
                return resp.json()
            except ValueError:
                return {}
        else:
            return {}

    def ModifyPatient(self, new_full_name: str = None, new_email: str = None) -> dict:
        """
        Update patient details using phone as identifier.
        PUT /patients/modify
        Body:
        {
          "phone": ...,
          "full_name": ...,
          "email": ...
        }
        """
        url = f"{BASE_URL}/patients/modify"
        payload = {"phone": self.phone}
        if new_full_name:
            payload["full_name"] = new_full_name
        if new_email:
            payload["email"] = new_email

        resp = requests.put(url, json=payload)
        try:
            data = resp.json()
        except ValueError:
            return {"success": False, "message": f"Invalid JSON response: {resp.text}"}

        # Update internal attributes if success
        if data.get("success"):
            if new_full_name:
                self.full_name = new_full_name
            if new_email:
                self.email = new_email
        return data

    def CreateAppointment(self, date: str, time: str) -> dict:
        """
        Create a new appointment via the API.
        POST /appointments
        Body:
        {
          "phone": ...,
          "date": ...,
          "time": ...
        }
        """
        url = f"{BASE_URL}/appointments"
        payload = {
            "phone": self.phone,
            "date": date,
            "time": time
        }
        resp = requests.post(url, json=payload)
        try:
            return resp.json()
        except ValueError:
            return {"success": False, "message": f"Invalid JSON response: {resp.text}"}

    def ListAppointmentsByPhone(self) -> list[dict]:
        """
        List upcoming appointments for a given phone via the API.
        POST /appointments/list/by_phone
        Body:
        {
          "phone": ...
        }
        """
        url = f"{BASE_URL}/appointments/list/by_phone"
        payload = {"phone": self.phone}
        resp = requests.post(url, json=payload)
        try:
            return resp.json()
        except ValueError:
            return []

    def CancelAppointmentByPhone(self, date: str, time: str) -> dict:
        """
        Cancel a future appointment using patient phone, date, and time via the API.
        DELETE /appointments/cancel/by_phone
        Body:
        {
          "phone": ...,
          "date": ...,
          "time": ...
        }
        """
        url = f"{BASE_URL}/appointments/cancel/by_phone"
        payload = {
            "phone": self.phone,
            "date": date,
            "time": time
        }
        resp = requests.delete(url, json=payload)
        try:
            return resp.json()
        except ValueError:
            return {"success": False, "message": f"Invalid JSON response: {resp.text}"}

    def RescheduleAppointmentByPhone(
        self,
        date: str,
        time: str,
        new_date: str,
        new_time: str,
        notes: str = ""
    ) -> dict:
        """
        Reschedule an existing appointment via the API.
        PUT /appointments/reschedule/by_phone
        Body:
        {
          "phone": ...,
          "date": ...,
          "time": ...,
          "new_date": ...,
          "new_time": ...,
          "notes": ...
        }
        """
        url = f"{BASE_URL}/appointments/reschedule/by_phone"
        payload = {
            "phone": self.phone,
            "date": date,
            "time": time,
            "new_date": new_date,
            "new_time": new_time,
            "notes": notes
        }
        resp = requests.put(url, json=payload)
        try:
            return resp.json()
        except ValueError:
            return {"success": False, "message": f"Invalid JSON response: {resp.text}"}

    def GetAvailableTimeSlots(self, date: str, operator: str, time: str) -> list[dict]:
        """
        Return next 3 available time slots via the API.
        POST /schedule/available
        Body:
        {
          "date": ...,
          "operator": ...,
          "time": ...
        }
        """
        url = f"{BASE_URL}/schedule/available"
        payload = {
            "date": date,
            "operator": operator,
            "time": time
        }
        resp = requests.post(url, json=payload)
        try:
            return resp.json()
        except ValueError:
            return []


    # Helper to call OpenAI ChatCompletion (unchanged)
    def call_openai_chat(self, messages: list[dict], model: str = "gpt-4o", temperature: float = 0.0) -> str:
        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message.content


    # Orchestration: process a single user input (updated to instantiate with customer info)
    def handle_incoming_message(self, user_text: str):
        """
        Simulate a single-turn conversation:
        - Initialize PatientServiceTools with given customer info
        - Look up patient by phone
        - Send context + user_text to GPT
        - If GPT responds with {"tool": "...", "input": {...}}, dispatch to the tool
        - Otherwise, return GPT’s natural-language response
        """

        tools.add_message("user", user_text)
        # Step 3: call OpenAI
        gpt_reply = self.call_openai_chat(self.messages)
        tools.add_message("assistant", gpt_reply)
        print(gpt_reply)
        # Step 4: attempt to parse tool call
        try:
            reply_obj = json.loads(gpt_reply)
            tool_name = reply_obj.get("tool")
            tool_input = reply_obj.get("input", {})

            if tool_name == "CreatePatient":
                result = tools.CreatePatient()
                return {"tool_result": result}
            elif tool_name == "GetPatientByPhone":
                result = tools.GetPatientByPhone()
                return {"tool_result": result}
            elif tool_name == "ModifyPatient":
                result = tools.ModifyPatient(
                    new_full_name=tool_input.get("full_name"),
                    new_email=tool_input.get("email")
                )
                return {"tool_result": result}
            elif tool_name == "CreateAppointment":
                result = tools.CreateAppointment(
                    date=tool_input["date"],
                    time=tool_input["time"]
                )
                message = f'Your appointment on {tool_input["date"]} at {tool_input["time"]} is confirmed'
                print(message)
                self.add_message("assistant", message)
                return {"tool_result": result}
            elif tool_name == "ListAppointmentsByPhone":
                result = tools.ListAppointmentsByPhone()
                message = "Do you want to change any of your appointments?"
                print (message)
                self.add_message("assistant", message)
                return {"tool_result": result}
            elif tool_name == "CancelAppointmentByPhone":
                result = tools.CancelAppointmentByPhone(
                    date=tool_input["date"],
                    time=tool_input["time"]
                )
                message = "Your appointment has been cancelled. Is there anything I can do for you"
                print(message)
                self.add_message("assistant", message)
                return {"tool_result": result}
            elif tool_name == "RescheduleAppointmentByPhone":
                result = tools.RescheduleAppointmentByPhone(
                    date=tool_input["date"],
                    time=tool_input["time"],
                    new_date=tool_input["new_date"],
                    new_time=tool_input["new_time"],
                    notes=tool_input.get("notes", "")
                )
                message = "Your appointment has been rescheduled successfully. "
                print(message)
                self.add_message("assistant", message)
                return {"tool_result": result}
            elif tool_name == "GetAvailableTimeSlots":
                result = tools.GetAvailableTimeSlots(
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

    def add_message(self, role, message):
        self.messages.append({"role": role, "content": message})

# Example usage
if __name__ == "__main__":
    from_phone = "6476248506"
    #from_phone = "1111111111"
    tools = PatientServiceTools(from_phone)

    while True:
    # Initialize with a sample customer
        # Simulate a user message
        user_text = input("\nYou: ").strip()

        output = tools.handle_incoming_message(user_text=user_text)

        if "tool_result" in output:
            print("Tool result:", output["tool_result"])
        else:
            print("AI response:", output["response"])
