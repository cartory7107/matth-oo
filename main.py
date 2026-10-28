import os
import requests

# পরিবেশ থেকে ভ্যারিয়েবল গ্রহণ
ollama_key = os.environ.get("ollama") or os.environ.get("OLLAMA") or os.environ.get("OLLAMA_API_KEY")
wa_token = os.environ.get("WHATSAPP_TOKEN")
wa_phone_id = os.environ.get("WHATSAPP_PHONE_ID")
wa_to = os.environ.get("WHATSAPP_TO")

prompt = (
    "You are an inspiring Bangladeshi math teacher. Create an engaging, creative daily math puzzle "
    "or brainteaser in clear, beautiful Bengali (বাংলা ভাষায়) suitable for high school students. "
    "Format nicely with math emojis: "
    "১) 🧩 আজকের গণিত ধাঁধা (Title) "
    "২) ❓ সমস্যা (The Problem) "
    "৩) 💡 ছোট্ট ইঙ্গিত (Hint). "
    "Do NOT reveal the final answer. The entire message must be in Bengali."
)

# ওলামা ক্লাউড দিয়ে বাংলায় ধাঁধা তৈরি
print("Generating math puzzle from Ollama Cloud...")
ollama_res = requests.post(
    "https://ollama.com/api/chat",
    headers={"Authorization": f"Bearer {ollama_key.strip()}", "Content-Type": "application/json"},
    json={
        "model": "gemma4:31b-cloud",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    },
    timeout=60,
)
ollama_res.raise_for_status()
puzzle_text = ollama_res.json().get("message", {}).get("content")

# মেটা ক্লাউড এপিআই দিয়ে হোয়াটসঅ্যাপে পাঠানো
wa_url = f"https://graph.facebook.com/v21.0/{wa_phone_id}/messages"
headers_wa = {
    "Authorization": f"Bearer {wa_token.strip()}",
    "Content-Type": "application/json",
}
payload_wa = {
    "messaging_product": "whatsapp",
    "to": wa_to.strip(),
    "type": "text",
    "text": {"body": puzzle_text},
}

print(f"Sending puzzle to WhatsApp: {wa_to}...")
wa_res = requests.post(wa_url, headers=headers_wa, json=payload_wa)
print(f"WhatsApp status: {wa_res.status_code}")
if wa_res.status_code != 200:
    print(f"WhatsApp error response: {wa_res.text}")
wa_res.raise_for_status()
print("ধাঁধা সফলভাবে হোয়াটসঅ্যাপে পৌঁছে গেছে!")
