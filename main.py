import os
import requests
from google import genai

# পরিবেশ থেকে সিক্রেট মান গ্রহণ
gemini_key = os.environ.get("GEMINI_API_KEY")
bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")

# জেমিনি মডেল দিয়ে পাজল তৈরি
client = genai.Client(api_key=gemini_key)
prompt = (
    "You are an inspiring math teacher. Create a fun, creative daily math puzzle "
    "or brainteaser suitable for high school students. "
    "Include: 1) Puzzle Title, 2) The Problem, 3) A small hint. "
    "Do NOT give the final answer. Keep it engaging with math emojis."
)

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=prompt,
)

# টেলিগ্রাম চ্যানেলে মেসেজ পাঠানো
telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
payload = {
    "chat_id": chat_id,
    "text": response.text,
}
requests.post(telegram_url, json=payload)
