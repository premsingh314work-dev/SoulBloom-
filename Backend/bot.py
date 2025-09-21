import google.genai as genai
from datetime import datetime
from database import db
import uuid
client = genai.Client(api_key="AIzaSyDzX6NrBh-02my-Sll8stjoUYffBkgVB4Y")
chats = db["bloosm_chats"]

# Save a message to session
async def save_message(session_id: str, role: str, content: str):
    msg = {"role": role, "content": content, "timestamp": datetime.utcnow()}
    await chats.update_one({"session_id": session_id}, {"$push": {"messages": msg}})
#creating session id
async def get_or_create_session(user_id: str):
    session = await chats.find_one({"user_id": user_id, "active": True})
    if session:
        return session
    # Create new session
    new_session = {
        "user_id": user_id,
        "session_id": str(uuid.uuid4()),
        "messages": [],
        "created_at": datetime.utcnow(),
        "active": True
    }
    await chats.insert_one(new_session)
    return new_session


#gemini response 
async def gemini_response(user_id: str, user_input: str):
    #  Get or create session
    session = await get_or_create_session(user_id)
    session_id = session["session_id"]

    #  Save user's message
    await save_message(session_id, "user", user_input)

    # Get updated session with all messages
    session = await chats.find_one({"session_id": session_id})
    structured_contents = [
        {"role": msg["role"] if msg["role"]=="assistant" else "user", "parts": [{"text": msg["content"]}]}
        for msg in session["messages"]
    ]

    #  Call Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=structured_contents,
        config={
            "system_instruction": (
                "You are Bloosm, a compassionate mental health consultant for students. "
                "Your role is to listen, understand their feelings, and provide supportive, "
                "short replies under 30 words. Be empathetic and helpful like a mentor."
            )
        }
    )

    bot_reply_text = response.text

    #  Save bot reply
    await save_message(session_id, "assistant", bot_reply_text)

    return {"reply": bot_reply_text, "session_id": session_id}

