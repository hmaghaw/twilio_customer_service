# Twilio Media Stream ↔ OpenAI Realtime Bridge

An async FastAPI service that connects incoming Twilio Media Streams to OpenAI’s Realtime API (gpt-4o-realtime-preview). Enables live, bidirectional voice conversations between callers and an AI assistant.

## Features

- **FastAPI HTTP & WebSocket**  
  - `GET /` health check  
  - `POST/GET /incoming-call` returns TwiML to start a Twilio media stream  
  - `WS /media-stream` bridges audio between Twilio and OpenAI  
- **Voice & Text Modalities**  
  - Full-duplex G.711 μ-law audio  
  - Real-time transcript logging (`response.content.text` & `.done`)  
- **Server-side VAD & Truncation**  
  - Interrupts AI playback when user starts speaking  
  - Sends “marks” for alignment and handles truncation events  
- **Configurable Prompt & Voice**  
  - Load your system instructions from `sample_prompt.txt`  
  - Choose built-in OpenAI voice via `VOICE` env var  
- **Structured Logging**  
  - Uses Python `logging` for key lifecycle events  
  - Optional silencing of low-level websockets/uvicorn debug logs  

---

## Getting Started

### Prerequisites

- Python 3.10+  
- An OpenAI API key with Realtime access  
- Twilio account (for Media Streams)  
- `ngrok` or public HTTPS endpoint for Twilio callbacks  

### Install

```bash
git clone https://github.com/your-org/twilio-openai-realtime.git
cd twilio-openai-realtime
pip install -r requirements.txt
```

### Configuration

Create a `.env` in the project root:

```dotenv
OPENAI_API_KEY=sk-...
PORT=5050
VOICE=alloy           # (optional) any supported voice
```

Place your assistant’s instructions in `sample_prompt.txt` (UTF-8).

### Running Locally

```bash
uvicorn main:app   --host 0.0.0.0   --port $PORT   --reload
```

---

## How It Works

1. **Incoming Call**  
   Twilio sends the call to `/incoming-call`. We reply with TwiML that speaks a prompt then opens a WebSocket to `/media-stream`.

2. **WebSocket Media Stream**  
   - Accept Twilio’s WebSocket (`twilio_ws`)  
   - Dial out to OpenAI’s Realtime WebSocket (`openai_ws`)  
   - In parallel:  
     - **receive_from_twilio** → forward Twilio’s `media` frames as `input_audio_buffer.append` to OpenAI  
     - **send_to_twilio** → forward OpenAI’s `response.audio.delta` frames as Twilio `media` events  
   - Handle VAD interrupts: when `input_audio_buffer.speech_started` arrives, truncate AI audio and drop queued buffers.

3. **Transcript Logging**  
   Partial text (`response.content.text`) and final text (`response.content.done`) events are printed/logged for debugging or storage.

---

## Project Structure

\`\`\`
.
├── main.py           # FastAPI app & session logic
├── sample_prompt.txt # Your assistant’s system instructions
├── requirements.txt  # Python dependencies
├── .env              # Environment variables (gitignored)
└── README.md         # This file
\`\`\`

---

## Extending & Customization

- **Custom “first prompt”**  
  Uncomment and modify \`send_initial_conversation_item()\` to have the AI speak first.  
- **Logging Levels**  
  Adjust or silence \`websockets\` / \`uvicorn\` logs via the commented \`logging.getLogger(...)\` lines.  
- **VAD Tuning**  
  Swap \`server_vad\` for a different turn-detection method or configure \`SHOW_TIMING_MATH\` for debug math prints.  
- **Voice Models**  
  Change \`VOICE\` to any voice supported by your OpenAI beta region.  

---

## Troubleshooting

- **WebSocket Failures**  
  Ensure your OpenAI key has \`realtime\` access and that you include the \`"OpenAI-Beta": "realtime=v1"\` header.  
- **Twilio Connection Errors**  
  Make sure your \`/incoming-call\` URL is reachable via HTTPS (use \`ngrok\` in dev).  
- **Audio Artefacts**  
  Verify both input/output formats are set to \`"g711_ulaw"\`.  

---

## License

[MIT License](LICENSE)

> _Happy coding—and may your AI voice assistant never drop a packet!_
