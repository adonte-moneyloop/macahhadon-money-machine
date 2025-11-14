import json
import random
from decimal import Decimal

RESPONSES = [
    '{"answer": "Drink water to stay sharp.", "ad": "HydratePro"}',
    '{"answer": "Use Pomodoro: 25 min on, 5 min off.", "ad": "FocusTimer"}',
    '{"answer": "Read 10 pages daily.", "ad": "BookBoost"}'
]

WALLET_FILE = "/tmp/wallet.txt"

def load_wallet():
    try:
        with open(WALLET_FILE) as f:
            return Decimal(f.read().strip())
    except:
        return Decimal("0")

def save_wallet(wallet):
    with open(WALLET_FILE, "w") as f:
        f.write(str(wallet))

def handler(event, context=None):
    wallet = load_wallet()
    resp = random.choice(RESPONSES)
    data = json.loads(resp)
    
    earned = Decimal("0.004")
    wallet += earned
    save_wallet(wallet)
    
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "earned": float(earned),
            "total": float(wallet),
            "answer": data["answer"],
            "ad": data["ad"]
        })
    }