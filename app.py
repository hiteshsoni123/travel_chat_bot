from fastapi import FastAPI, WebSocket
from openai import OpenAI
import os, json
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")

app = FastAPI()

@app.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            message = await websocket.receive_text()
            data = json.loads(message)
            user_message = data.get("user", "")

            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are a travel assistant for India."},
                    {"role": "user", "content": user_message}
                ]
            )

            bot_reply = response.choices[0].message.content
            await websocket.send_text(json.dumps({"bot": bot_reply}))

        except Exception as e:
            await websocket.send_text(json.dumps({"error": str(e)}))
            break
