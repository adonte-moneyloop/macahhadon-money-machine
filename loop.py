"""
Macahhdon Money Machine - loop.py

Each run:
- Reads this instance's wallet file (wallet_<INSTANCE_ID>.txt)
- Adds $0.05
- Writes it back with 4 decimal places

INSTANCE_ID is set by the GitHub Actions matrix.
"""

from decimal import Decimal
import os

INSTANCE_ID = os.getenv("INSTANCE_ID", "1")
WALLET_FILE = f"wallet_{INSTANCE_ID}.txt"


def load_wallet(path: str) -> Decimal:
  """Load the current wallet balance for this instance."""
  try:
    with open(path, "r") as f:
      return Decimal(f.read().strip().lstrip("$"))
  except Exception:
    # If file doesn't exist or is invalid, start at 0
    return Decimal("0")


def save_wallet(path: str, amount: Decimal) -> None:
  """Save the updated wallet balance."""
  with open(path, "w") as f:
    f.write(f"${amount:.4f}")


def main() -> None:
  # Load current wallet
  w = load_wallet(WALLET_FILE)

  # Earn $0.05 per job
  w += Decimal("0.05")

  # Save updated wallet
  save_wallet(WALLET_FILE, w)

  # Log for GitHub Actions
  print(f"[Instance {INSTANCE_ID}] Wallet updated to ${w:.4f}")


if __name__ == "__main__":
  main()
