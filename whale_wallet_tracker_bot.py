import time
import requests
from web3 import Web3  

# Telegram Bot API Token and Chat ID
TELEGRAM_API_TOKEN = '8090054164:AAGnzjvWs4t57Thh1Zlrxanq4JL3xlWpX9o'  # Replace with your bot's token
CHAT_ID = '1672023055'  # Replace with your chat ID

# Infura URL for Ethereum connection
INFURA_URL = 'https://mainnet.infura.io/v3/ceae07cef7b747b28fb71fb5ac76ef5c'  # Replace with your Infura project ID
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# List of whale wallet addresses to track
whale_wallets = [
    '0x9e927c02C9eadAE63f5EFb0Dd818943c7262Fb8e',
    '0x00000000219ab540356cBB839Cbe05303d7705Fa'
    # Replace with actual Ethereum wallet addresses
]    

# Function to get wallet balance in Ether
def get_wallet_balance(wallet_address):
    balance = web3.eth.get_balance(wallet_address)  # Get balance in Wei
    ether_balance = web3.from_wei(balance, 'ether')  # Convert Wei to Ether
    return ether_balance

# Function to check for transactions involving the wallet
def get_latest_transactions(wallet_address):
    latest_block = web3.eth.block_number
    for block_num in range(latest_block, latest_block - 10, -1):  # Check the last 10 blocks
        block = web3.eth.get_block(block_num, full_transactions=True)  # Correct code
        for tx in block.transactions:
            if tx['from'] == wallet_address or tx['to'] == wallet_address:
                message = f"Transaction detected in Block {block_num}:\n"
                message += f"From: {tx['from']} To: {tx['to']} Value: {web3.from_wei(tx['value'], 'ether')} ETH\n"
                message += f"Transaction Hash: {tx['hash'].hex()}"
                send_telegram_message(message)

# Function to send a message to Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage"
    params = {
        'chat_id': CHAT_ID,
        'text': message
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print(f"Message sent to Telegram: {message}")
    else:
        print(f"Failed to send message to Telegram. Status code: {response.status_code}")

# Function to track whale wallets
def track_wallets():
    while True:
        for wallet in whale_wallets:
            balance = get_wallet_balance(wallet)
            print(f"Wallet: {wallet} Balance: {balance} ETH")
            get_latest_transactions(wallet)
            print("-" * 50)  # Separator
        time.sleep(60)  # Wait for 1 minute before checking again

# Start the tracking process
if __name__ == '__main__':
    track_wallets()
