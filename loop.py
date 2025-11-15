import os
import json
import random
import requests
from decimal import Decimal

# ==== CONFIG ====
GROK_API = "https://api.x.ai/v1/chat/completions"
GROK_KEY = os.getenv("GROK_KEY")
INSTANCE_ID = os.getenv("INSTANCE_ID", "1")
ULTRA_FAST = os.getenv("ULTRA_FAST", "0") == "1"  # Set to 1 for max speed
WALLET_FILE = f"wallet_{INSTANCE_ID}.txt"

# Load wallet
try:
    with open(WALLET_FILE, "r") as f:
        WALLET = Decimal(f.read().strip().lstrip("$"))
except:
    WALLET = Decimal("0")

# Simulated responses
SIMULATED = [
    '{"answer": "Drink water.", "ad": "HydratePro"}',
    '{"answer": "Use Pomodoro.", "ad": "FocusTimer"}'
]

def debug(msg):
    print(f"DEBUG [Instance {INSTANCE_ID}]: {msg}")

def call_grok():
    debug("Calling Grok...")
    if not GROK_KEY:
        debug("No key → simulated")
        return random.choice(SIMULATED)
    try:
        payload = {
            "model": "grok-3-mini",
            "messages": [{"role": "user", "content": "Short tip in JSON: {\"answer\": \"...\", \"ad\": \"...\"}"}],
            "temperature": 0.7,
            "max_tokens": 100
        }
        headers = {"Authorization": f"Bearer {GROK_KEY}", "Content-Type": "application/json"}
        r = requests.post(GROK_API, json=payload, headers=headers, timeout=30)
        if r.status_code != 200:
            debug(f"Error {r.status_code}")
            return random.choice(SIMULATED)
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        debug(f"API error: {e}")
        return random.choice(SIMULATED)

def main():
    global WALLET
    debug("LIVE LOOP STARTED")

    # === ULTRA-FAST MODE ===
    if ULTRA_FAST:
        debug("ULTRA-FAST MODE: Skipping API")
        earned = Decimal("0.05")
    else:
        raw = call_grok()
        try:
            data = json.loads(raw)
        except:
            data = {"answer": "Error", "ad": "Retry"}
        earned = Decimal("0.05")

    # === EARN & SAVE ===
    WALLET += earned
    debug(f"Earned ${earned} → ${WALLET:.4f}")

    with open(WALLET_FILE, "w") as f:
        f.write(f"${WALLET:.4f}")
    debug(f"Saved to {WALLET_FILE}")

if __name__ == "__main__":
    main()
