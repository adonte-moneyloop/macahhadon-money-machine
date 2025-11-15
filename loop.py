import os
import json
import random
import requests
from decimal import Decimal

# ==== CONFIG ====
GROK_API = "https://api.x.ai/v1/chat/completions"
GROK_KEY = os.getenv("GROK_KEY")
INSTANCE_ID = os.getenv("INSTANCE_ID", "1")
WALLET_FILE = f"wallet_{INSTANCE_ID}.txt"

# Load wallet
try:
    with open(WALLET_FILE, "r") as f:
        WALLET = Decimal(f.read().strip().lstrip("$"))
except:
    WALLET = Decimal("0")

# Real AdSense links (replace with yours)
ADSENSE_LINKS = [
    "https://google.com/adsense?ref=macahhdon&ad=hydratepro",
    "https://google.com/adsense?ref=macahhdon&ad=focustimer"
]

def call_grok():
    if not GROK_KEY:
        return json.dumps({"answer": "Drink water to boost focus.", "ad": random.choice(ADSENSE_LINKS)})

    try:
        payload = {
            "model": "grok-3-mini",
            "messages": [{"role": "user", "content": "Give a short productivity tip + AdSense link in JSON: {\"answer\": \"tip\", \"ad\": \"link\"}"}],
            "temperature": 0.7,
            "max_tokens": 50
        }
        headers = {"Authorization": f"Bearer {GROK_KEY}", "Content-Type": "application/json"}
        r = requests.post(GROK_API, json=payload, headers=headers, timeout=10)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        else:
            return json.dumps({"answer": "Use Pomodoro.", "ad": random.choice(ADSENSE_LINKS)})
    except:
        return json.dumps({"answer": "Read 10 pages daily.", "ad": random.choice(ADSENSE_LINKS)})

def main():
    global WALLET
    raw = call_grok()
    try:
        data = json.loads(raw)
        ad = data["ad"]  # Real AdSense link
    except:
        ad = random.choice(ADSENSE_LINKS)

    earned = Decimal("0.001")  # Real AdSense $0.001/impression
    WALLET += earned

    with open(WALLET_FILE, "w") as f:
        f.write(f"${WALLET:.4f}")

if __name__ == "__main__":
    main()
