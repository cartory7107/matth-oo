import os
import requests

# পরিবেশ থেকে ভ্যারিয়েবল গ্রহণ
ollama_key = (
    os.environ.get("ollama")
    or os.environ.get("OLLAMA")
    or os.environ.get("OLLAMA_API_KEY")
)
bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")

# এপিআই কী চেক করা
print(f"Ollama key loaded: {bool(ollama_key)}")
if not ollama_key:
    raise ValueError(
        "API Key পাওয়া যায়নি! দয়া করে .github/workflows/daily.yml ফাইলের env অংশে ollama যোগ করুন।"
    )

headers = {
    "Authorization": f"Bearer {ollama_key.strip()}",
    "Content-Type": "application/json",
}

prompt = (
    "You are an inspiring Bangladeshi math teacher. Create an engaging and creative daily math puzzle "
    "or brainteaser in clear, beautiful Bengali (বাংলা ভাষায়) suitable for high school students. "
    "Format the response nicely with math emojis and structure it with: "
    "১) 🧩 আজকের গণিত ধাঁধা (Title) "
    "২) ❓ সমস্যা (The Problem) "
    "৩) 💡 ছোট্ট ইঙ্গিত (Hint). "
    "Do NOT reveal the final answer. The entire post must be in Bengali."
)

models = ["gemma4:31b-cloud"]
puzzle_text = None

for model in models:
    try:
        print(f"Trying Ollama Cloud model: {model}...")
        res = requests.post(
            "https://ollama.com/api/chat",
            headers=headers,
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
            },
            timeout=60,
        )
        if res.status_code == 200:
            data = res.json()
            puzzle_text = data.get("message", {}).get("content")
            if puzzle_text:
                print(f"Success with {model}!")
                break
        else:
            print(f"Ollama response ({res.status_code}): {res.text}")
    except Exception as e:
        print(f"Error with {model}: {e}")

if not puzzle_text:
    raise RuntimeError("Ollama Cloud থেকে ধাঁধা তৈরি করা যায়নি।")

# টেলিগ্রাম চ্যানেলে পাঠানো
telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
tel_res = requests.post(telegram_url, json={"chat_id": chat_id, "text": puzzle_text})
print(f"Telegram status: {tel_res.status_code}")
if tel_res.status_code != 200:
    print(f"Telegram error details: {tel_res.text}")
tel_res.raise_for_status()
