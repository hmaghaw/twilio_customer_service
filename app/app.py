from flask import Flask, request, jsonify, Response
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse, Gather
import os
from openai import OpenAI
import mysql.connector
import requests

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host="twilio_call_log",
        user="voiceuser",
        password="voicepass",
        database="ai_voice"
    )

def update_conversation(call_sid, role, message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO conversation_log (call_sid, role, message)
        VALUES (%s, %s, %s)
    """, (call_sid, role, message))
    conn.commit()
    cursor.close()
    conn.close()

def get_conversation(call_sid):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT role, message FROM conversation_log
        WHERE call_sid = %s
        ORDER BY created_at ASC
    """, (call_sid,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert to OpenAI-style messages
    messages = [{"role": row["role"], "content": row["message"]} for row in rows]
    if not any(m["role"] == "system" for m in messages):
        messages.insert(0, {
            "role": "system",
            "content": "You are a helpful and concise phone assistant."
        })
    return messages

def get_ai_reply(call_sid, user_input):
    url = "https://ideationmax.info/webhook/94b76b3b-95e3-4cb8-88db-6db6bc63e70a"
    payload = {
        "call_sid": call_sid,
        "user_input": user_input
    }

    response = requests.post(url, json=payload)

    ai_reply = response.json()['ai_reply']
    update_conversation(call_sid, "user", user_input)

    return ai_reply

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
    call_sid = request.form.get("CallSid", "default")
    user_input = request.form.get("SpeechResult", "").strip()
    print(f"user_input: {user_input}")

    if not user_input:
        vr = VoiceResponse()
        vr.say("Sorry, I didn’t catch that. Can you say it again?")
        vr.redirect("/ai_gather")
        return Response(str(vr), mimetype="application/xml")

    ai_reply = get_ai_reply(call_sid, user_input)

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
