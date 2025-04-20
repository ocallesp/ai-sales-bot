import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI

# ——— DEBUG: show us the key your code sees
api_key = os.getenv("OPENAI_API_KEY")
print("🔑 OPENAI_API_KEY =", api_key)

# ——— Configuration
client = OpenAI(api_key=api_key)

def ask_ai(prompt: str) -> str:
    messages = [
        {
            "role": "system",
            "content": """
    You are an enthusiastic and persuasive Real Estate agent. You only promote and sell real estate properties (homes, condos, land, etc.).  
    For each question about properties:  
    • Respond with enthusiasm (“Awesome!” or “You’ll love this!”)  
    • Highlight a key benefit (“This home has a spacious backyard perfect for families.”)  
    • Use motivating phrases (“Find your dream home today!”)  
    • End with a call to action (“Which property interests you?”)  
    If the question is not about real estate, politely redirect: “I’m thrilled to help with your property needs! What type of home are you looking for today?”  
    Always respond in English, with short and direct messages (2-3 sentences max), ideal for quick communication. Do not mention competitors or topics outside real estate. If users insist on unrelated topics, kindly repeat the redirection.
    """
        },
        # Few-shot example
        {
            "role": "user",
            "content": "I’m looking for a family home."
        },
        {
            "role": "assistant",
            "content": "Awesome! This 4-bedroom home has a large backyard and modern kitchen. Ready to schedule a tour?"
        },
        # Actual user prompt
        {
            "role": "user",
            "content": prompt
        }
    ]

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=200,
        temperature=0.8,
    )
    return resp.choices[0].message.content.strip()


app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    print("🔔 Webhook hit!")
    user_msg = request.values.get("Body", "").strip()
    print("▶️ Body =", user_msg)

    try:
        reply = ask_ai(user_msg)
        print("🤖 AI reply:", reply)    # <-- log it!
    except Exception as e:
        print("⚠️ OpenAI error:", e)
        reply = "Sorry, I'm having trouble right now."

    # Build TwiML
    twilio_resp = MessagingResponse()
    twilio_resp.message(reply)
    
    xml = str(twilio_resp)
    print("📨 TwiML response:\n", xml)   # ← new line
    return str(twilio_resp), 200, {"Content-Type": "application/xml"}

@app.route("/status", methods=["GET", "POST"])
def status_callback():
    # Twilio will send back parameters such as MessageSid and MessageStatus
    sid    = request.values.get("MessageSid")
    status = request.values.get("MessageStatus")
    print(f"🛰️ StatusCallback for {sid}: {status}")
    return ("", 204)   # 204 No Content is fine for callbacks

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
