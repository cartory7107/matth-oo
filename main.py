import os
import requests

# পরিবেশ থেকে ভ্যারিয়েবল গ্রহণ
ollama_key = os.environ.get("ollama") or os.environ.get("OLLAMA") or os.environ.get("OLLAMA_API_KEY")
wa_token = os.environ.get("WHATSAPP_TOKEN")
wa_phone_id = os.environ.get("WHATSAPP_PHONE_ID")
wa_to = os.environ.get("WHATSAPP_TO")
bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")

prompt = (
    "You are an inspiring Bangladeshi math teacher. Create an engaging, unique daily math puzzle "
    "or brainteaser in clear, beautiful Bengali (বাংলা ভাষায়) suitable for high school students. "
    "Format nicely with math emojis: "
    "১) 🧩 আজকের গণিত ধাঁধা (Title) "
    "২) ❓ সমস্যা (The Problem) "
    "৩) 💡 ছোট্ট ইঙ্গিত (Hint). "
    "Do NOT reveal the final answer. The entire message must be in Bengali."
)

# ওলামা দিয়ে কুইজ তৈরি
print("Generating 5-hour quiz from Ollama Cloud...")
res = requests.post(
    "https://ollama.com/api/chat",
    headers={"Authorization": f"Bearer {ollama_key.strip()}", "Content-Type": "application/json"},
    json={"model": "gemma4:31b-cloud", "messages": [{"role": "user", "content": prompt}], "stream": False},
    timeout=60,
)
res.raise_for_status()
puzzle_text = res.json().get("message", {}).get("content")

# ১) হোয়াটসঅ্যাপে পাঠানো
if wa_token and wa_phone_id and wa_to:
    wa_url = f"https://graph.facebook.com/v21.0/{wa_phone_id}/messages"
    headers_wa = {"Authorization": f"Bearer {wa_token.strip()}", "Content-Type": "application/json"}
    payload_wa = {"messaging_product": "whatsapp", "to": wa_to.strip(), "type": "text", "text": {"body": puzzle_text}}
    wa_res = requests.post(wa_url, headers=headers_wa, json=payload_wa)
    print(f"WhatsApp status: {wa_res.status_code}")

# ২) টেলিগ্রাম চ্যানেলেও পাঠানো (যদি থাকে)
if bot_token and chat_id:
    tg_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    tg_res = requests.post(tg_url, json={"chat_id": chat_id, "text": puzzle_text})
    print(f"Telegram status: {tg_res.status_code}")

print("৫ ঘণ্টার কুইজ সফলভাবে পাঠানো হয়েছে!")
