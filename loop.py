from decimal import Decimal
import os

# === ULTRA-FAST CONFIG ===
i = os.getenv("INSTANCE_ID", "1")
f = f"wallet_{i}.txt"

# Load wallet (fast, no debug)
try:
    w = Decimal(open(f).read().strip().lstrip("$"))
except:
    w = Decimal("0")

# Earn $0.05 per job (MAX SPEED)
w += Decimal("0.05")

# Save wallet (fast write)
open(f, "w").write(f"${w:.4f}")
