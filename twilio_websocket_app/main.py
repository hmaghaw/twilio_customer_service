import os
import json
import base64
import asyncio
import traceback
import websockets
from collections import deque
from typing import Optional, Deque

from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.websockets import WebSocketDisconnect
from twilio.twiml.voice_response import VoiceResponse, Connect, Say, Stream
from dotenv import load_dotenv

load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PORT = int(os.getenv("PORT", 5050))
SYSTEM_MESSAGE = (
    "You are a helpful and bubbly AI assistant who loves to chat about "
    "anything the user is interested in and is prepared to offer them facts. "
    "You have a penchant for dad jokes, owl jokes, and rickrolling – subtly. "
    "Always stay positive, but work in a joke when appropriate."
)
VOICE = "alloy"
LOG_EVENT_TYPES = [
    "error",
    "response.content.done",
    "rate_limits.updated",
    "response.done",
    "input_audio_buffer.committed",
    "input_audio_buffer.speech_stopped",
    "input_audio_buffer.speech_started",
    "session.created",
]
SHOW_TIMING_MATH = False

app = FastAPI()

# ------------------------------------------------------------------------------
# CallSession: holds shared state for each media-stream connection
# ------------------------------------------------------------------------------

class CallSession:
    def __init__(self, twilio_ws: WebSocket, openai_ws: websockets.WebSocketClientProtocol):
        self.twilio_ws: WebSocket = twilio_ws
        self.openai_ws: websockets.WebSocketClientProtocol = openai_ws

        # Twilio stream identifier (set on "start" events)
        self.stream_sid: Optional[str] = None

        # Latest timestamp (ms) from the inbound Twilio media event
        self.latest_media_timestamp: int = 0

        # The last OpenAI assistant item ID that was sent
        self.last_assistant_item: Optional[str] = None

        # Queue tracking outstanding "mark" events
        self.mark_queue: Deque[str] = deque()

        # When we began sending back the current assistant audio (ms)
        self.response_start_timestamp_twilio: Optional[int] = None


# ------------------------------------------------------------------------------
# Helper: initialize OpenAI Realtime session
# ------------------------------------------------------------------------------

async def initialize_session(openai_ws: websockets.WebSocketClientProtocol) -> None:
    """
    Send the initial 'session.update' message to configure formats, VAD, voice, instructions, etc.
    """
    session_update = {
        "type": "session.update",
        "session": {
            "turn_detection": {"type": "server_vad"},
            "input_audio_format": "g711_ulaw",
            "output_audio_format": "g711_ulaw",
            "voice": VOICE,
            "instructions": SYSTEM_MESSAGE,
            "modalities": ["text", "audio"],
            "temperature": 0.8,
        },
    }
    print("Sending session update:", json.dumps(session_update))
    await openai_ws.send(json.dumps(session_update))


# ------------------------------------------------------------------------------
# Helper: send initial conversation prompt if AI speaks first
# ------------------------------------------------------------------------------

async def send_initial_conversation_item(openai_ws: websockets.WebSocketClientProtocol) -> None:
    """
    If you want the AI to initiate the call, call this after initialize_session().
    """
    initial_conversation_item = {
        "type": "conversation.item.create",
        "item": {
            "type": "message",
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": (
                        "Greet the user with 'Hello there! I am an AI voice assistant powered by Twilio "
                        "and the OpenAI Realtime API. You can ask me for facts, jokes, or anything you can imagine. "
                        "How can I help you?'"
                    ),
                }
            ],
        },
    }
    await openai_ws.send(json.dumps(initial_conversation_item))
    await openai_ws.send(json.dumps({"type": "response.create"}))


# ------------------------------------------------------------------------------
# Helper: send "mark" to Twilio (for alignment)
# ------------------------------------------------------------------------------

async def send_mark(twilio_ws: WebSocket, stream_sid: Optional[str], session: CallSession) -> None:
    """
    Send a "mark" event to Twilio and push onto the session.mark_queue.
    """
    if not stream_sid:
        return

    mark_event = {
        "event": "mark",
        "streamSid": stream_sid,
        "mark": {"name": "responsePart"},
    }
    await twilio_ws.send_json(mark_event)
    session.mark_queue.append("responsePart")


# ------------------------------------------------------------------------------
# Helper: handle "speech_started" interruption
# ------------------------------------------------------------------------------

async def handle_speech_started_event(session: CallSession) -> None:
    """
    When the user begins speaking again and disrupts the AI response,
    truncate the last assistant item and clear queued audio for Twilio.
    """
    if session.mark_queue and session.response_start_timestamp_twilio is not None:
        elapsed_time = session.latest_media_timestamp - session.response_start_timestamp_twilio
        if SHOW_TIMING_MATH:
            print(
                f"Calculating elapsed time for truncation: "
                f"{session.latest_media_timestamp} - {session.response_start_timestamp_twilio} = {elapsed_time}ms"
            )

        if session.last_assistant_item:
            if SHOW_TIMING_MATH:
                print(
                    f"Truncating item with ID: {session.last_assistant_item}, "
                    f"Truncated at: {elapsed_time}ms"
                )
            truncate_event = {
                "type": "conversation.item.truncate",
                "item_id": session.last_assistant_item,
                "content_index": 0,
                "audio_end_ms": elapsed_time,
            }
            await session.openai_ws.send(json.dumps(truncate_event))

        # Instruct Twilio to drop any queued AI audio and return to listening
        await session.twilio_ws.send_json({"event": "clear", "streamSid": session.stream_sid})

        session.mark_queue.clear()
        session.last_assistant_item = None
        session.response_start_timestamp_twilio = None


# ------------------------------------------------------------------------------
# Coroutine: receive audio from Twilio, forward to OpenAI
# ------------------------------------------------------------------------------

async def receive_from_twilio(session: CallSession) -> None:
    """
    Read each Twilio media event and forward as OpenAI 'input_audio_buffer.append'.
    Also handle 'start' and 'mark' events from Twilio.
    """
    try:
        async for raw_message in session.twilio_ws.iter_text():
            data = json.loads(raw_message)

            event_type = data.get("event")
            if event_type == "media" and session.openai_ws.open:
                media = data.get("media", {})
                payload = media.get("payload")
                timestamp = media.get("timestamp")
                if payload is not None and timestamp is not None:
                    session.latest_media_timestamp = int(timestamp)
                    audio_append = {
                        "type": "input_audio_buffer.append",
                        "audio": payload,
                    }
                    await session.openai_ws.send(json.dumps(audio_append))

            elif event_type == "start":
                session.stream_sid = data["start"]["streamSid"]
                print(f"Incoming stream has started {session.stream_sid}")
                session.response_start_timestamp_twilio = None
                session.latest_media_timestamp = 0
                session.last_assistant_item = None

            elif event_type == "mark":
                # Twilio confirming receipt of a mark
                if session.mark_queue:
                    session.mark_queue.popleft()

    except WebSocketDisconnect:
        print("Twilio client disconnected.")
        if session.openai_ws.open:
            await session.openai_ws.close()

    except Exception as e:
        print("Error in receive_from_twilio:", e, traceback.format_exc())
        # Clean up both WebSockets if something unexpected happens
        try:
            if session.openai_ws.open:
                await session.openai_ws.close()
            await session.twilio_ws.close(code=1011)
        except Exception:
            pass


# ------------------------------------------------------------------------------
# Coroutine: receive audio from OpenAI, forward to Twilio
# ------------------------------------------------------------------------------

async def send_to_twilio(session: CallSession) -> None:
    """
    Read each OpenAI event and forward audio back to Twilio as 'media' events.
    Also watch for OpenAI's 'speech_started' VAD to interrupt AI audio.
    """
    try:
        async for openai_raw in session.openai_ws:
            response = json.loads(openai_raw)
            event_type = response.get("type")

            if event_type in LOG_EVENT_TYPES:
                print(f"Received event: {event_type}", response)

            # If this is an AI audio chunk, forward it directly
            if event_type == "response.audio.delta" and "delta" in response:
                # delta is already base64-encoded G.711μ-law; Twilio expects the same
                audio_delta = {
                    "event": "media",
                    "streamSid": session.stream_sid,
                    "media": {"payload": response["delta"]},
                }
                await session.twilio_ws.send_json(audio_delta)

                # Record when the AI started speaking (first chunk)
                if session.response_start_timestamp_twilio is None:
                    session.response_start_timestamp_twilio = session.latest_media_timestamp
                    if SHOW_TIMING_MATH:
                        print(
                            f"Setting start timestamp for new response: "
                            f"{session.response_start_timestamp_twilio}ms"
                        )

                # Track the item ID so we can truncate if interrupted
                if response.get("item_id"):
                    session.last_assistant_item = response["item_id"]

                await send_mark(session.twilio_ws, session.stream_sid, session)

            # If the caller starts speaking, interrupt any in-progress AI response
            if event_type == "input_audio_buffer.speech_started":
                print("Speech started detected by OpenAI VAD.")
                if session.last_assistant_item:
                    print(f"Interrupting response with id: {session.last_assistant_item}")
                await handle_speech_started_event(session)

    except Exception as e:
        print("Error in send_to_twilio:", e, traceback.format_exc())
        # Clean up both WebSockets on unexpected errors
        try:
            if session.openai_ws.open:
                await session.openai_ws.close()
            await session.twilio_ws.close(code=1011)
        except Exception:
            pass


# ------------------------------------------------------------------------------
# FastAPI route: health check
# ------------------------------------------------------------------------------

@app.get("/", response_class=JSONResponse)
async def index_page():
    return {"message": "Twilio Media Stream Server is running!"}


# ------------------------------------------------------------------------------
# FastAPI route: incoming call TwiML
# ------------------------------------------------------------------------------

@app.api_route("/incoming-call", methods=["GET", "POST"])
async def handle_incoming_call(request: Request):
    """
    Generate TwiML that instructs Twilio to open a Media Stream WebSocket to /media-stream.
    """
    response = VoiceResponse()
    response.say(
        "Please wait while we connect your call to the A. I. voice assistant, powered by Twilio and the Open-A.I. Realtime API"
    )
    response.pause(length=1)
    response.say("O.K. you can start talking!")

    host = request.url.hostname
    connect = Connect()
    connect.stream(url=f"wss://{host}/twilio-websocket/media-stream")
    response.append(connect)

    return HTMLResponse(content=str(response), media_type="application/xml")


# ------------------------------------------------------------------------------
# FastAPI route: WebSocket media stream
# ------------------------------------------------------------------------------

@app.websocket("/media-stream")
async def handle_media_stream(websocket: WebSocket):
    """
    Accept Twilio's WebSocket connection, then open a second WebSocket to OpenAI.
    Launch two concurrent coroutines to bridge audio in both directions.
    """
    print("Client connected (Twilio).")
    await websocket.accept()

    try:
        # Open OpenAI WebSocket
        async with websockets.connect(
            "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01",
            extra_headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "OpenAI-Beta": "realtime=v1",
            },
        ) as openai_ws:
            # Send initial session settings
            await initialize_session(openai_ws)

            # Create a shared session object
            session = CallSession(twilio_ws=websocket, openai_ws=openai_ws)

            # If you want the AI to speak first, uncomment this line:
            # await send_initial_conversation_item(openai_ws)

            # Run both coroutines concurrently
            await asyncio.gather(
                receive_from_twilio(session),
                send_to_twilio(session),
            )

    except Exception as e:
        print("Error establishing OpenAI WebSocket:", e, traceback.format_exc())
        # Close Twilio WebSocket if OpenAI fails to connect
        try:
            await websocket.close(code=1011)
        except Exception:
            pass


# ------------------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        reload=False,  # Turn off auto-reload in production
        log_level="debug",
    )
