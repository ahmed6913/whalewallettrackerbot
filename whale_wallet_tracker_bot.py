# Your Imports
import time
import requests
from web3 import Web3  
import csv

# Telegram Bot API Token and Chat ID
TELEGRAM_API_TOKEN = '8090054164:AAGnzjvWs4t57Thh1Zlrxanq4JL3xlWpX9o'
CHAT_ID = '1672023055'

# Discord Webhook URL
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1365769923980296192/TKzL5RJOwV995vSo3mYBghZQhqQiqUJSXCtGQLLneffEmvruYFLaaABbWX6_qyD2gWKp'

# Infura URL for Ethereum connection
INFURA_URL = 'https://mainnet.infura.io/v3/ceae07cef7b747b28fb71fb5ac76ef5c'
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Whale Wallets
whale_wallets = ['0x9e927c02C9eadAE63f5EFb0Dd818943c7262Fb8e',
    '0x00000000219ab540356cBB839Cbe05303d7705Fa',
    '0x4838B106FCe9647Bdf1E7877BF73cE8B0BAD5f97']

# List to store detected whale transactions
detected_transactions = []

def save_transactions_csv(transactions, filename="whale_transactions.csv"):
    if not transactions:
        print("No transactions to save.")
        return
    keys = transactions[0].keys()
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(transactions)
    print(f"Saved {len(transactions)} transactions to {filename}")

# Send Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage"
    params = {
        'chat_id': CHAT_ID,
        'text': message
    }
    requests.post(url, data=params)

# Send Discord
def send_discord_message(message):
    if not DISCORD_WEBHOOK_URL:
        return
    payload = {'content': message}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload, headers=headers)

    if response.status_code != 204:
        print(f"Failed to send Discord message. Status code: {response.status_code}")
        print(f"Response: {response.text}")


# Check transactions
def get_latest_transactions(wallet_address):
    latest_block = web3.eth.block_number
    for block_num in range(latest_block, latest_block - 10, -1):
        block = web3.eth.get_block(block_num, full_transactions=True)
        for tx in block.transactions:
            if 'from' in tx and 'to' in tx and (tx['from'] == wallet_address or tx['to'] == wallet_address):
                message = f"🚨 **[Whale Alert]** 🚨\n\n"
                message += f"📦 Block: {block_num}\n"
                message += f"👤 From: `{tx['from']}`\n"
                message += f"👤 To: `{tx['to']}`\n"
                message += f"💰 Value: {web3.from_wei(tx['value'], 'ether')} ETH\n"
                message += f"🔗 [View Transaction](https://etherscan.io/tx/{tx['hash'].hex()})"

                send_telegram_message(message)
                send_discord_message(message)
                detected_transactions.append({
                    "block": block_num,
                    "from": tx['from'],
                    "to": tx['to'],
                    "value_eth": float(web3.from_wei(tx['value'], 'ether')),
                    "tx_hash": tx['hash'].hex()
                })

# Whale Tracker
def track_wallets():
    while True:
        for wallet in whale_wallets:
            balance = web3.eth.get_balance(wallet)
            ether_balance = web3.from_wei(balance, 'ether')
            print(f"Wallet: {wallet} Balance: {ether_balance} ETH")
            get_latest_transactions(wallet)
        save_transactions_csv(detected_transactions)
        time.sleep(60)

if __name__ == '__main__':
    track_wallets()
