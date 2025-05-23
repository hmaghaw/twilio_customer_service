from flask import Flask, request, jsonify, Response
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse
import os

app = Flask(__name__)

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
    app.run(host="0.0.0.0", port=5000)
