import time
import requests
from flask_cors import CORS  # <-- Add this import

from web3 import Web3  
from datetime import datetime
from flask import Flask, jsonify, send_from_directory
import threading
import os

# === Setup ===
TELEGRAM_API_TOKEN = '8090054164:AAGnzjvWs4t57Thh1Zlrxanq4JL3xlWpX9o'
CHAT_ID = '1672023055'
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1365769923980296192/TKzL5RJOwV995vSo3mYBghZQhqQiqUJSXCtGQLLneffEmvruYFLaaABbWX6_qyD2gWKp'
INFURA_URL = 'https://mainnet.infura.io/v3/ceae07cef7b747b28fb71fb5ac76ef5c'
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

whale_wallets = [
    '0x9e927c02C9eadAE63f5EFb0Dd818943c7262Fb8e',
    '0x00000000219ab540356cBB839Cbe05303d7705Fa',
    '0x4838B106FCe9647Bdf1E7877BF73cE8B0BAD5f97'
]

# === Shared Whale Activity Feed ===
recent_activity = []

# === Bot Alerts ===
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage"
    params = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=params)

def send_discord_message(message):
    if not DISCORD_WEBHOOK_URL:
        return
    payload = {'content': message}
    headers = {'Content-Type': 'application/json'}
    requests.post(DISCORD_WEBHOOK_URL, json=payload, headers=headers)

# === Whale Tracker Logic ===
def get_latest_transactions(wallet_address):
    latest_block = web3.eth.block_number
    for block_num in range(latest_block, latest_block - 10, -1):
        block = web3.eth.get_block(block_num, full_transactions=True)
        for tx in block.transactions:
            if tx['from'] == wallet_address or tx['to'] == wallet_address:
                eth_value = web3.from_wei(tx['value'], 'ether')
                tx_link = f"https://etherscan.io/tx/{tx['hash'].hex()}"

                # Save to recent activity
                event = {
                    'from': tx['from'],
                    'to': tx['to'],
                    'value': float(eth_value),
                    'hash': tx['hash'].hex(),
                    'timestamp': datetime.utcnow().isoformat()
                }
                recent_activity.append(event)
                if len(recent_activity) > 100:
                    recent_activity.pop(0)

                # Alert
                message = (
                    f"🚨 [Whale Alert] 🚨\n"
                    f"📦 Block: {block_num}\n"
                    f"👤 From: {tx['from']}\n"
                    f"👤 To: {tx['to']}\n"
                    f"💰 Value: {eth_value} ETH\n"
                    f"🔗 {tx_link}"
                )
                send_telegram_message(message)
                send_discord_message(message)

def track_wallets():
    while True:
        for wallet in whale_wallets:
            balance = web3.eth.get_balance(wallet)
            ether_balance = web3.from_wei(balance, 'ether')
            print(f"Wallet: {wallet} Balance: {ether_balance} ETH")
            get_latest_transactions(wallet)
        time.sleep(60)

# === Flask Web Server ===
app = Flask(__name__)
CORS(app)  # <-- add this line to enable CORS on all routes


@app.route('/api/activity')
def get_activity():
    return jsonify(recent_activity[::-1])  # newest first

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

def run_web_server():
    app.run(host='0.0.0.0', port=5000)

# === Start Everything ===
if __name__ == '__main__':
    threading.Thread(target=run_web_server).start()
    track_wallets()
