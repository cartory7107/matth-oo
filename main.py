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

# বর্তমান সক্রিয় দুটি মডেল
models_to_try = ["gemini-3.8-flash", "gemini-3.8-pro"]
puzzle_text = None

for model_name in models_to_try:
    print(f"Trying model: {model_name}...")
    for attempt in range(1, 4):
        try:
            print(f"Attempt {attempt} with {model_name}...")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            if response and response.text:
                puzzle_text = response.text
                print(f"Success with {model_name}!")
                break
        except Exception as e:
            print(f"Error on attempt {attempt}: {e}")
            if attempt < 3:
                time.sleep(10)  # সার্ভারের চাপ কমার জন্য ১০ সেকেন্ড অপেক্ষা
    if puzzle_text:
        break

if not puzzle_text:
    raise RuntimeError("সার্ভার ব্যস্ত থাকায় ধাঁধা তৈরি করা যায়নি।")

# টেলিগ্রাম চ্যানেলে পাঠানো
telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
res = requests.post(telegram_url, json={"chat_id": chat_id, "text": puzzle_text})
print(f"Telegram status: {res.status_code}")
if res.status_code != 200:
    print(f"Telegram error details: {res.text}")
res.raise_for_status()
