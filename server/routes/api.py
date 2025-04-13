# server/routes/api.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import sqlite3
import re
from datetime import datetime
from utils.sentiment import analyze_sentiment
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api")
security = HTTPBasic()

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = "admin"
    correct_password = "password123"
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@router.get("/products")
async def get_products():
    try:
        conn = sqlite3.connect("sales.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        rows = [{"id": r[0], "name": r[1], "price": r[2], "stock": r[3], "discount": r[4]} for r in cursor.fetchall()]
        conn.close()
        return rows
    except Exception as e:
        logger.error(f"Error in get_products: {str(e)}")
        raise

@router.post("/chat")
async def post_chat(data: dict):
    try:
        text = data["text"]
        user_sentiment = analyze_sentiment(text)
        conn = sqlite3.connect("sales.db")
        cursor = conn.cursor()
        user_message_id = str(int(datetime.now().timestamp() * 1000))
        cursor.execute(
            "INSERT INTO messages (id, text, sender, sentiment, timestamp) VALUES (?, ?, ?, ?, ?)",
            (user_message_id, text, "user", user_sentiment, datetime.now())
        )
        clean_text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = clean_text.split()
        logger.info(f"Words after cleaning: {words}")
        product_name = None
        cursor.execute("SELECT name FROM products")
        product_names = [row[0].lower() for row in cursor.fetchall()]
        for word in words:
            if word in product_names:
                product_name = word
                break
        if product_name:
            logger.info(f"Looking for product: {product_name}")
            cursor.execute("SELECT * FROM products WHERE LOWER(name) = ?", (product_name,))
            row = cursor.fetchone()
            if row:
                product = {"id": row[0], "name": row[1], "price": row[2], "stock": row[3], "discount": row[4]}
                reply = f"{product['name']} is ${product['price']}."
                if product["stock"] >= 50:
                    reply += " 5% off!"
                elif product["stock"] >= 20:
                    reply += " 3% off!"
                bot_message_id = str(int(datetime.now().timestamp() * 1000) + 1)
                bot_sentiment = "positive"
                cursor.execute(
                    "INSERT INTO messages (id, text, sender, sentiment, timestamp) VALUES (?, ?, ?, ?, ?)",
                    (bot_message_id, reply, "bot", bot_sentiment, datetime.now())
                )
                conn.commit()
                conn.close()
                return {"reply": reply, "user_sentiment": user_sentiment, "bot_sentiment": bot_sentiment}
        bot_message_id = str(int(datetime.now().timestamp() * 1000) + 1)
        bot_sentiment = "positive"
        cursor.execute(
            "INSERT INTO messages (id, text, sender, sentiment, timestamp) VALUES (?, ?, ?, ?, ?)",
            (bot_message_id, "Product not found.", "bot", bot_sentiment, datetime.now())
        )
        conn.commit()
        conn.close()
        return {"reply": "Product not found.", "user_sentiment": user_sentiment, "bot_sentiment": bot_sentiment}
    except Exception as e:
        logger.error(f"Error in post_chat: {str(e)}")
        raise

@router.get("/sentiment/monthly", dependencies=[Depends(verify_credentials)])
async def get_monthly_sentiment():
    try:
        conn = sqlite3.connect("sales.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT strftime('%Y-%m', timestamp) as month,
                   SUM(CASE WHEN sentiment = 'positive' AND sender = 'user' THEN 1 ELSE 0 END) * 100.0 / SUM(CASE WHEN sender = 'user' THEN 1 ELSE 0 END) as positive,
                   SUM(CASE WHEN sentiment = 'neutral' AND sender = 'user' THEN 1 ELSE 0 END) * 100.0 / SUM(CASE WHEN sender = 'user' THEN 1 ELSE 0 END) as neutral,
                   SUM(CASE WHEN sentiment = 'negative' AND sender = 'user' THEN 1 ELSE 0 END) * 100.0 / SUM(CASE WHEN sender = 'user' THEN 1 ELSE 0 END) as negative
            FROM messages
            GROUP BY strftime('%Y-%m', timestamp)
            HAVING SUM(CASE WHEN sender = 'user' THEN 1 ELSE 0 END) > 0
        """)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({
                "month": row[0],
                "positive": round(row[1], 2) if row[1] is not None else 0,
                "neutral": round(row[2], 2) if row[2] is not None else 0,
                "negative": round(row[3], 2) if row[3] is not None else 0
            })
        conn.close()
        return result
    except Exception as e:
        logger.error(f"Error in get_monthly_sentiment: {str(e)}")
        raise

@router.delete("/chat/history", dependencies=[Depends(verify_credentials)])
async def clear_chat_history():
    try:
        conn = sqlite3.connect("sales.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM messages")
        conn.commit()
        conn.close()
        return {"message": "Chat history cleared"}
    except Exception as e:
        logger.error(f"Error in clear_chat_history: {str(e)}")
        raise

@router.get("/messages", dependencies=[Depends(verify_credentials)])
async def get_messages():
    try:
        conn = sqlite3.connect("sales.db")
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, sender, text, sentiment FROM messages ORDER BY timestamp")
        rows = [{"timestamp": r[0], "sender": r[1], "text": r[2], "sentiment": r[3]} for r in cursor.fetchall()]
        conn.close()
        return rows
    except Exception as e:
        logger.error(f"Error in get_messages: {str(e)}")
        raise

@router.post("/products", dependencies=[Depends(verify_credentials)])
async def add_product(data: dict):
    try:
        conn = sqlite3.connect("sales.db")
        cursor = conn.cursor()
        # Get the highest existing ID and increment it
        cursor.execute("SELECT MAX(CAST(id AS INTEGER)) FROM products")
        max_id = cursor.fetchone()[0]
        product_id = str(max_id + 1) if max_id is not None else "1"
        cursor.execute(
            "INSERT INTO products (id, name, price, stock, discount) VALUES (?, ?, ?, ?, ?)",
            (product_id, data["name"], float(data["price"]), int(data["stock"]), data["discount"])
        )
        conn.commit()
        conn.close()
        return {"message": "Product added successfully"}
    except Exception as e:
        logger.error(f"Error in add_product: {str(e)}")
        raise