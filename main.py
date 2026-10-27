import os
import time
import requests
from google import genai

gemini_key = os.environ.get("GEMINI_API_KEY")
bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")

client = genai.Client(api_key=gemini_key)
prompt = (
    "You are an inspiring math teacher. Create a fun, creative daily math puzzle "
    "or brainteaser suitable for high school students. "
    "Include: 1) Puzzle Title, 2) The Problem, 3) A small hint. "
    "Do NOT give the final answer. Keep it engaging with math emojis."
)

# একটি মডেল ব্যস্ত থাকলে স্বয়ংক্রিয়ভাবে পরেরটি কাজ করবে
models_to_try = ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-2.0-flash"]
puzzle_text = None

for model_name in models_to_try:
    try:
        print(f"Trying {model_name}...")
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        if response and response.text:
            puzzle_text = response.text
            print(f"Success with {model_name}!")
            break
    except Exception as e:
        print(f"Busy or error with {model_name}: {e}")
        time.sleep(2)

if not puzzle_text:
    raise RuntimeError("সবগুলো মডেল এই মুহূর্তে ব্যস্ত রয়েছে।")

# টেলিগ্রাম চ্যানেলে পাঠানো
telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
res = requests.post(telegram_url, json={"chat_id": chat_id, "text": puzzle_text})
print(f"Telegram status: {res.status_code}")
