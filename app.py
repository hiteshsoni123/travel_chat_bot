# from fastapi import FastAPI, WebSocket
# from openai import OpenAI
# import os, json
# from dotenv import load_dotenv

# load_dotenv()
# client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")

# app = FastAPI()

# @app.websocket("/chat")
# async def chat(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         try:
#             message = await websocket.receive_text()
#             data = json.loads(message)
#             user_message = data.get("user", "")

#             response = client.chat.completions.create(
#                 model="llama3-8b-8192",
#                 messages=[
#                     {"role": "system", "content": "You are a travel assistant for India."},
#                     {"role": "user", "content": user_message}
#                 ]
#             )

#             bot_reply = response.choices[0].message.content
#             await websocket.send_text(json.dumps({"bot": bot_reply}))

#         except Exception as e:
#             await websocket.send_text(json.dumps({"error": str(e)}))
#             break
from fastapi import FastAPI, WebSocket
from openai import OpenAI
import os, json
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")

app = FastAPI()

# Common handler
async def chat_handler(websocket: WebSocket, system_prompt: str):
    await websocket.accept()
    while True:
        try:
            message = await websocket.receive_text()
            data = json.loads(message)
            user_message = data.get("user", "")

            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )

            bot_reply = response.choices[0].message.content
            await websocket.send_text(json.dumps({"bot": bot_reply}))

        except Exception as e:
            await websocket.send_text(json.dumps({"error": str(e)}))
            break


# 1️⃣ Travel Chat
@app.websocket("/chat/travel")
async def travel_chat(websocket: WebSocket):
    await chat_handler(websocket, "You are a travel assistant for India. Provide recommendations, guides, and tips.")


# 2️⃣ Beauty Chat
@app.websocket("/chat/beauty")
async def beauty_chat(websocket: WebSocket):
    await chat_handler(websocket, "You are a beauty advisor. Give skincare, haircare, and makeup advice.")


# 3️⃣ General Chat
@app.websocket("/chat/general")
async def general_chat(websocket: WebSocket):
    await chat_handler(websocket, "You are a friendly assistant for general conversations.")
