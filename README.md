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

---