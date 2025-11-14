import os
import time
import json
import random
import requests
from decimal import Decimal

# ==== CONFIG ====
GROK_API = "https://api.x.ai/v1/chat/completions"
GROK_KEY = os.getenv("GROK_KEY")  # Set in GitHub Secrets

WALLET = Decimal("0")
TARGETS = [100, 1_000, 10_000]
MULTIPLIERS = [1.5, 3.0, 10.0]
CURRENT_MULT_IDX = 0

# ==== PROMPT (Includes AdSense Link) ====
PROMPT = """You are a premium AI assistant.
Generate a short, high-value productivity tip.
Return ONLY valid JSON in this format:
{"answer": "Your tip here", "ad": "Try FocusApp → https://your-adsense-link.com"}"""

# ==== SIMULATED RESPONSES (Fallback if API fails) ====
SIMULATED_RESPONSES = [
    '{"answer": "Drink water to stay sharp.", "ad": "Try HydratePro → https://example.com"}',
    '{"answer": "Use Pomodoro: 25 min on, 5 min off.", "ad": "Get FocusTimer → https://example.com"}',
    '{"answer": "Read 10 pages daily.", "ad": "Join BookBoost → https://example.com"}'
]

# ==== CALL GROK (REAL API + Fallback) ====
def call_grok():
    if not GROK_KEY:
        print("GROK_KEY not set → using simulated response")
        return random.choice(SIMULATED_RESPONSES)

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
        r = requests.post(GROK_API, json=payload, headers=headers, timeout=30)
        if r.status_code == 403:
            print("403: Check GROK_KEY or model access")
            return random.choice(SIMULATED_RESPONSES)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"API Error: {e} → using simulated")
        return random.choice(SIMULATED_RESPONSES)

# ==== MONETIZE (AdSense Revenue) ====
def monetize():
    # Replace with real AdSense tracking later
    # For now: $0.004 per answer (average)
    return Decimal("0.004")

# ==== MAIN LOOP ====
def main():
    global WALLET, CURRENT_MULT_IDX
    print("Grok Money Loop STARTED | Wallet: $0.00 | LIVE MODE")
    
    iteration = 0
    while WALLET < TARGETS[-1]:
        iteration += 1
        
        # 1. Get Grok answer
        raw = call_grok()
        try:
            data = json.loads(raw)
            answer = data["answer"]
            ad = data["ad"]
        except:
            answer = "Tip unavailable"
            ad = "Try again → https://example.com"
        
        # 2. Earn money
        earned = monetize()
        WALLET += earned
        
        # 3. Milestone check
        if CURRENT_MULT_IDX < len(TARGETS) and WALLET >= TARGETS[CURRENT_MULT_IDX]:
            print(f"\nHIT ${TARGETS[CURRENT_MULT_IDX]:,.2f}! MULTIPLIER ×{MULTIPLIERS[CURRENT_MULT_IDX]}")
            CURRENT_MULT_IDX += 1
        
        # 4. Log
        next_target = TARGETS[CURRENT_MULT_IDX] if CURRENT_MULT_IDX < len(TARGETS) else "MAX"
        print(f"Iter {iteration:4} | Earned ${earned:.4f} | Total ${WALLET:8.2f} | Next: ${next_target:,}")
        print(f"Answer: {answer}")
        print(f"Ad: {ad}\n")
        
        # 5. Save wallet to file (for GitHub Actions)
        with open("wallet.txt", "w") as f:
            f.write(f"${WALLET:.4f}")
        
        time.sleep(1)  # Be gentle

if __name__ == "__main__":
    main()