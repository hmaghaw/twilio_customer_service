# 🚀 Automation & Messaging Stack: n8n + Twilio API

This stack includes:

- 🌐 [n8n](https://n8n.io): Visual workflow automation
- 📲 Twilio API: SMS messaging powered by Flask
- 🔐 HTTPS reverse proxy via NGINX with SSL certificates from Certbot

---

## 🔗 Live URLs

| Service     | URL                                |
|-------------|-------------------------------------|
| n8n         | [https://ideationmax.info/](https://ideationmax.info/)      |
| Twilio API  | [https://ideationmax.info/api/](https://ideationmax.info/api/) |

---

## 📤 Send an SMS via API

### Endpoint

```
POST https://ideationmax.info/api/send_sms
```

### Headers

```
Content-Type: application/json
```

### Request Body

```json
{
  "to": "+1XXXXXXXXXX",
  "message": "Hello from Twilio API!"
}
```

### Sample `curl` command

```bash
curl -X POST https://ideationmax.info/api/send_sms \
  -H "Content-Type: application/json" \
  -d '{"to": "+1XXXXXXXXXX", "message": "Hello from Twilio API!"}'
```

---

## 🧾 .env Configuration

Environment variables are managed via the `.env` file. Sample:

```env
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=admin
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

---

## 🐳 Deployment

```bash
docker-compose up -d
```

Ensure that the following files are in the project root:

- `docker-compose.yml`
- `nginx.conf`
- `.env`

Certificates must be available at: `/opt/n8n/certs/privkey.pem` and `fullchain.pem`.

---

## 🔐 HTTPS Note

All requests are served over HTTPS via port `443`.

------

## 🧠 Flask App Overview

The Flask app provides the following Twilio integrations:

### 1. ✅ Send Outbound SMS

**POST** `/api/send_sms`

Sends an SMS using Twilio API.

**Request JSON:**
```json
{
  "to": "+1XXXXXXXXXX",
  "message": "Hello from Twilio API!"
}
```

**Sample curl:**
```bash
curl -X POST https://ideationmax.info/api/send_sms \
  -H "Content-Type: application/json" \
  -d '{"to": "+1XXXXXXXXXX", "message": "Hello from Twilio API!"}'
```

---

### 2. 📩 Handle Incoming SMS

**POST** `/api/incoming_sms`

This endpoint is used as a webhook to handle incoming SMS messages sent to your Twilio number.

- Logs the message
- Replies with an automated message

**Twilio Webhook Configuration (SMS):**
Set your Twilio number's messaging webhook to:
```
https://ideationmax.info/api/incoming_sms
```

---

### 3. ☎️ Handle Incoming Calls

**POST** `/api/incoming_call`

This endpoint handles incoming voice calls to your Twilio number:

- Greets the caller
- Records a message
- Hangs up

**Twilio Webhook Configuration (Voice):**
Set your Twilio number's voice webhook to:
```
https://ideationmax.info/api/incoming_call
```

------

### 4. 📞 Create Outbound Voice Call

**POST** `/api/create_call`

Initiates an outbound call using the Twilio Voice API and plays a predefined message.

**Request JSON:**
```json
{
  "to": "+1XXXXXXXXXX"
}
```

**Sample curl:**
```bash
curl -X POST https://ideationmax.info/api/create_call \
  -H "Content-Type: application/json" \
  -d '{"to": "+1XXXXXXXXXX"}'
```

**Response:**
```json
{
  "sid": "CAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

---