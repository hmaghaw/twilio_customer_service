from flask import Flask, request, jsonify, Response
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse, Gather
import os
from openai import OpenAI

#openai.api_key = os.environ["OPENAI_API_KEY"]
api_key = "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"
app = Flask(__name__)

# In-memory session store (can be replaced with Redis or DB)
session_memory = {}

def get_conversation(session_id):
    return session_memory.get(session_id, [
        {"role": "system", "content": "You are a helpful and concise phone assistant."}
    ])

def update_conversation(session_id, user_input, ai_reply):
    if session_id not in session_memory:
        session_memory[session_id] = []
    session_memory[session_id].append({"role": "user", "content": user_input})
    session_memory[session_id].append({"role": "assistant", "content": ai_reply})
    session_memory[session_id] = session_memory[session_id][-6:]  # Keep last 6 messages

@app.route("/ai_intro", methods=["POST"])
def ai_intro():
    resp = VoiceResponse()
    resp.say("Hi! How can I help you today?", voice="alice")
    resp.redirect("/ai_gather")
    return Response(str(resp), mimetype="application/xml")

@app.route("/ai_gather", methods=["POST"])
def ai_gather():
    resp = VoiceResponse()
    gather = Gather(
        input="speech",
        action="/ai_process",
        method="POST",
        speech_timeout="auto",
        language="en-US",
        barge_in=True
    )
    resp.append(gather)
    resp.redirect("/ai_gather")  # fallback if no input
    return Response(str(resp), mimetype="application/xml")

@app.route("/ai_process", methods=["POST"])
def ai_process():
    session_id = request.form.get("CallSid", "default")
    user_input = request.form.get("SpeechResult", "").strip()
    print(f"user_input: {user_input}")

    if not user_input:
        vr = VoiceResponse()
        vr.say("Sorry, I didn’t catch that. Can you say it again?")
        vr.redirect("/ai_gather")
        return Response(str(vr), mimetype="application/xml")

    #messages = get_conversation(session_id)
    messages = [
        {"role": "system", "content": "You are a helpful and concise phone assistant."}
    ]
    messages.append({"role": "user", "content": user_input})

    try:
        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )

        ai_reply = response.choices[0].message.content
    except Exception as e:
        print(e)
        ai_reply = "I'm having trouble with Chat GPT responding right now. Please try again later."

    update_conversation(session_id, user_input, ai_reply)

    vr = VoiceResponse()
    vr.say(ai_reply, voice="alice")
    vr.redirect("/ai_gather")
    return Response(str(vr), mimetype="application/xml")

# Endpoint to send an outbound SMS
@app.route("/send_sms", methods=["POST"])
def send_sms():
    data = request.json
    to_number = data.get("to")
    message_body = data.get("message")

    if not to_number or not message_body:
        return jsonify({"error": "Missing 'to' or 'message'"}), 400

    try:
        client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])
        message = client.messages.create(
            body=message_body,
            from_=os.environ["TWILIO_PHONE_NUMBER"],
            to=to_number
        )
        return jsonify({"sid": message.sid}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/create_call", methods=["POST"])
def create_call():
    data = request.json
    to_number = data.get("to")

    if not to_number:
        return jsonify({"error": "Missing 'to'"}), 400

    try:
        client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])
        call = client.calls.create(
            twiml='<Response><Say>Hello. This is a test call from Twilio API.</Say></Response>',
            from_=os.environ["TWILIO_PHONE_NUMBER"],
            to=to_number
        )
        return jsonify({"sid": call.sid}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Webhook for incoming SMS
@app.route("/incoming_sms", methods=["POST"])
def incoming_sms():
    incoming_msg = request.form.get("Body", "")
    from_number = request.form.get("From", "")

    print(f"Received SMS from {from_number}: {incoming_msg}")

    # Optional: create a reply
    resp = MessagingResponse()
    resp.message("Thanks for your message. We’ll get back to you shortly.")
    return Response(str(resp), mimetype="application/xml")

# Webhook for incoming Calls
@app.route("/incoming_call", methods=["POST"])
def incoming_call():
    from_number = request.form.get("From", "")
    print(f"Incoming call from {from_number}")

    # Respond with TwiML
    resp = VoiceResponse()
    resp.say("Thank you for calling. Please leave a message after the beep.", voice="alice")
    resp.record(timeout=10, maxLength=30)
    resp.hangup()
    return Response(str(resp), mimetype="application/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
