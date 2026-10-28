import os
import time
import requests

ollama_key = (
    os.environ.get("ollama")
    or os.environ.get("OLLAMA")
    or os.environ.get("OLLAMA_API_KEY")
)
bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")

headers = {
    "Authorization": f"Bearer {ollama_key.strip()}",
    "Content-Type": "application/json",
}

prompt = (
    "You are an inspiring Bangladeshi math teacher. Create an engaging, unique, and creative math puzzle "
    "or brainteaser in clear, beautiful Bengali (বাংলা ভাষায়) suitable for high school students. "
    "Format nicely with math emojis: "
    "১) 🧩 আজকের গণিত ধাঁধা (Title) "
    "২) ❓ সমস্যা (The Problem) "
    "৩) 💡 ছোট্ট ইঙ্গিত (Hint). "
    "Do NOT reveal the final answer. The entire message must be in Bengali."
)

telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

# ২০ মিনিটের লাইভ এক্সপেরিমেন্ট (প্রতি ১ মিনিটে ১টি, মোট ২০টি)
TOTAL_ROUNDS = 20

for round_num in range(1, TOTAL_ROUNDS + 1):
    print(f"--- Round {round_num}/{TOTAL_ROUNDS} ---")
    try:
        res = requests.post(
            "https://ollama.com/api/chat",
            headers=headers,
            json={
                "model": "gemma4:31b-cloud",
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
            },
            timeout=60,
        )
        if res.status_code == 200:
            puzzle_text = res.json().get("message", {}).get("content")
            if puzzle_text:
                full_message = f"📢 ধাঁধা #{round_num} (লাইভ টেস্ট):\n\n{puzzle_text}"
                requests.post(telegram_url, json={"chat_id": chat_id, "text": full_message})
                print(f"Posted puzzle #{round_num} to Telegram!")
        else:
            print(f"Ollama error: {res.text}")
    except Exception as e:
        print(f"Error in round {round_num}: {e}")

    # শেষ রাউন্ড ছাড়া বাকিগুলোতে ৬০ সেকেন্ড বিরতি
    if round_num < TOTAL_ROUNDS:
        print("Waiting 60 seconds...")
        time.sleep(60)

print("২০ মিনিটের টেস্ট সফলভাবে সম্পন্ন হয়েছে!")
