# Macahhdon Money Machine 💸

An automated **AI money loop** running entirely on **GitHub Actions**.

Every few minutes, 20 instances run a tiny Python script (`loop.py`) that
increments their own wallet file. A second job sums all instance wallets into
`total_wallet.txt`, which powers the **LIVE WALLET** display on the public
`index.html` page.

> ⚠️ This is a **demo / toy** project for automation and GitHub Actions.
> It does not magically generate real-world income by itself. You are responsible
> for what you connect it to.

---

## How It Works

### 1. Per-instance wallets

- The workflow defines a matrix of instances: `1..20`
- Each instance gets a separate wallet file: `wallet_1.txt`, `wallet_2.txt`, … `wallet_20.txt`
- On each run, `loop.py`:
  - reads that wallet file
  - adds **$0.05**
  - writes it back with 4 decimal places

```python
# loop.py (core idea)
w = load_wallet(f"wallet_{INSTANCE_ID}.txt")
w += Decimal("0.05")
save_wallet(..., w)
