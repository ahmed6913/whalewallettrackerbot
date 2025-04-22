# 🐋 Ethereum Whale Wallet Tracker Bot

This bot tracks Ethereum whale wallets and sends **real-time notifications** about wallet balances and transactions via **Telegram**. It's perfect for crypto enthusiasts, analysts, and anyone interested in monitoring large-scale Ethereum movements.

---

## 🚀 Features

- 🔍 Monitors specified Ethereum whale wallets for **incoming and outgoing transactions**
- 💰 Tracks current **ETH balance** of each monitored wallet
- 📲 Sends **real-time Telegram alerts** for every transaction
- 📦 Scans the **latest 10 Ethereum blocks** for wallet activity
- 🔗 Includes **transaction hash, sender, recipient, and value** in alerts

---

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
1.git clone https://github.com/yourusername/whalewallettrackerbot.git
2.cd whalewallettrackerbot
3.pip install python-telegram-bot requests web3
4.python whale_wallet_tracker_bot.py


🚨 Whale Transaction Detected 🚨

💸 From: 0xabc...def  
💼 To: 0x123...456  
💰 Value: 1,250 ETH  
🔗 Tx Hash: https://etherscan.io/tx/0x...

New Balance of From Wallet: 3,000 ETH


