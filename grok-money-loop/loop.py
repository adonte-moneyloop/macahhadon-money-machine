import os
import time
import json
import random
from decimal import Decimal

# ==== CONFIG ====
GROK_API = "https://api.x.ai/v1/chat/completions"
GROK_KEY = os.getenv("GROK_KEY")  # Optional: Will be ignored in SIMULATED mode
WALLET = Decimal("0")                    # Starts at $0
TARGETS = [100, 1_000, 10_000]           # Milestones
MULTIPLIERS = [1.5, 3.0, 10.0]            # Reinvest aggressiveness
CURRENT_MULT_IDX = 0

# ==== SIMULATED GROK RESPONSES (No API Call) ====
SIMULATED_RESPONSES = [
    '{"answer": "Quick tip: Drink water to stay focused and energized.", "ad": "Try HydratePro → https://example.com"}',
    '{"answer": "Use the Pomodoro technique: 25 min work, 5 min break.", "ad": "Get FocusTimer → https://example.com"}',
    '{"answer": "Read 10 pages daily to build knowledge over time.", "ad": "Join BookBoost → https://example.com"}',
    '{"answer": "Walk 10,000 steps daily for better health.", "ad": "Track with StepMaster → https://example.com"}',
    '{"answer": "Sleep 7–8 hours to boost memory and mood.", "ad": "Try SleepWell → https://example.com"}',
    '{"answer": "Meditate 5 minutes daily to reduce stress.", "ad": "Use CalmMind → https://example.com"}'
]

# ==== SIMULATED GROK CALL (No API, No 403) ====
def call_grok():
    response = random.choice(SIMULATED_RESPONSES)
    print(f"[SIMULATED] Grok → {response[:70]}...")
    return response

# ==== MONETIZE (Simulated $0.004 per answer) ====
def monetize():
    return Decimal("0.004")  # Replace with real AdSense later

# ==== MAIN FEEDBACK LOOP ====
def main():
    global WALLET, CURRENT_MULT_IDX
    print("Grok Money Loop STARTED | Wallet: $0.00 | SIMULATED MODE")
    print("Every answer earns $0.004 → reinvested → compounds to $10,000\n")
    
    iteration = 0
    while WALLET < TARGETS[-1]:
        iteration += 1
        
        # 1. Get Grok answer (simulated)
        raw_response = call_grok()
        try:
            data = json.loads(raw_response)
            answer = data["answer"]
        except:
            answer = "Simulated answer"
        
        # 2. Earn money
        earned = monetize()
        WALLET += earned
        
        # 3. Check milestone & upgrade multiplier
        if CURRENT_MULT_IDX < len(TARGETS) and WALLET >= TARGETS[CURRENT_MULT_IDX]:
            print(f"\nHIT ${TARGETS[CURRENT_MULT_IDX]:,.2f}! MULTIPLIER → ×{MULTIPLIERS[CURRENT_MULT_IDX]}")
            CURRENT_MULT_IDX += 1
        
        # 4. Log progress
        next_target = TARGETS[CURRENT_MULT_IDX] if CURRENT_MULT_IDX < len(TARGETS) else "MAX"
        print(f"Iter {iteration:4} | Earned ${earned:.4f} | Total ${WALLET:8.2f} | Next: ${next_target:,}")
        
        # 5. Respect rate limits (even in sim)
        time.sleep(1.5)

if __name__ == "__main__":
    main()