import os
import json
import random
import requests
from decimal import Decimal

# ==== CONFIG ====
GROK_API = "https...
GROK_KEY = os.getenv("GROK_KEY")
WALLET = Decimal("0")
TARGETS = [100, 1000, 10000]
MULTIPLIERS = [1.5, 3.0, 10.0]
CURRENT_MULT_IDX = 0

# ==== PROMPT ====
PROMPT = """You are a premium AI assistant.
Generate a short, high-value productivity tip.
Return ONLY valid JSON: {"answer": "Your tip here", "ad": "Try FocusApp → https://example.com"}"""

# ==== SIMULATED FALLBACK ====
SIMULATED = [
    '{"answer": "Drink water to stay sharp.", "ad": "Try HydratePro → https://example.com"}',
    '{"answer": "Use Pomodoro: 25 min on, 5 min off.", "ad": "Get FocusTimer → https://example.com"}'
]

# ==== DEBUG LOGGING ====
def debug(msg):
    print(f"DEBUG: {msg}")

# ==== CALL GROK ====
def call_grok():
    debug("Calling Grok...")
    if not GROK_KEY:
        debug("No GROK_KEY → using simulated")
        return random.choice(SIMULATED)

    payload = {
        "model": "grok-3-mini",
        "messages": [{"role": "user", "content": PROMPT}],
        "temperature": 0.7,
        "max_tokens": 200
    }
    headers = {
        "Authorization": f"Bearer {GROK_KEY}",
        "Content-Type": "application/json"
    }
    try:
        debug("Sending request to xAI API...")
        r = requests.post(GROK_API, json=payload, headers=headers, timeout=30)
        debug(f"Response status: {r.status_code}")
        if r.status_code != 200:
            debug(f"API error: {r.text}")
            return random.choice(SIMULATED)
        response = r.json()["choices"][0]["message"]["content"]
        debug(f"Raw response: {response[:200]}...")
        return response
    except Exception as e:
        debug(f"Request failed: {e} → fallback")
        return random.choice(SIMULATED)

# ==== MONETIZE ====
def monetize():
    return Decimal("0.004")

# ====