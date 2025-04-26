# Your Imports
import time
import requests
from web3 import Web3  

# Telegram Bot API Token and Chat ID
TELEGRAM_API_TOKEN = '8090054164:AAGnzjvWs4t57Thh1Zlrxanq4JL3xlWpX9o'
CHAT_ID = '1672023055'

# Discord Webhook URL
DISCORD_WEBHOOK_URL = 'https://discordapp.com/api/webhooks/1365769923980296192/TKzL5RJOwV995vSo3mYBghZQhqQiqUJSXCtGQLLneffEmvruYFLaaABbWX6_qyD2gWKp'

# Infura URL for Ethereum connection
INFURA_URL = 'https://mainnet.infura.io/v3/ceae07cef7b747b28fb71fb5ac76ef5c'
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Whale Wallets
whale_wallets = ['0x9e927c02C9eadAE63f5EFb0Dd818943c7262Fb8e',
    '0x00000000219ab540356cBB839Cbe05303d7705Fa',
    '0x4838B106FCe9647Bdf1E7877BF73cE8B0BAD5f97']

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
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

# Check transactions
def get_latest_transactions(wallet_address):
    latest_block = web3.eth.block_number
    for block_num in range(latest_block, latest_block - 10, -1):
        block = web3.eth.get_block(block_num, full_transactions=True)
        for tx in block.transactions:
            if tx['from'] == wallet_address or tx['to'] == wallet_address:
               message = f"🚨 **[Whale Alert]** 🚨\n\n"
message += f"📦 Block: {block_num}\n"
message += f"👤 From: `{tx['from']}`\n"
message += f"👤 To: `{tx['to']}`\n"
message += f"💰 Value: {web3.from_wei(tx['value'], 'ether')} ETH\n"
message += f"🔗 [View Transaction](https://etherscan.io/tx/{tx['hash'].hex()})"

                send_telegram_message(message)
                send_discord_message(message)

# Whale Tracker
def track_wallets():
    while True:
        for wallet in whale_wallets:
            balance = web3.eth.get_balance(wallet)
            ether_balance = web3.from_wei(balance, 'ether')
            print(f"Wallet: {wallet} Balance: {ether_balance} ETH")
            get_latest_transactions(wallet)
        time.sleep(60)

if __name__ == '__main__':
    track_wallets()
