from flask import Flask, request, jsonify
from twilio.rest import Client
import os

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
