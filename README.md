Ethereum Whale Wallet Tracker Bot 

This bot tracks Ethereum whale wallets and sends real-time notifications about wallet balances and transactions via Telegram. The bot is designed to monitor a set of Ethereum wallets for any transactions and provides detailed updates including transaction value, sender, recipient, and transaction hash.

Features

Monitors Ethereum whale wallets for transaction activity.

Tracks the balance of monitored wallets in Ether.

Sends notifications to a Telegram chat for any relevant transactions.

Tracks the last 10 Ethereum blocks for wallet transactions.

Prerequisites

Before using this bot, make sure you have the following:

Python 3.x installed.

Web3.py library installed.

Telegram Bot API Token and Chat ID.

Infura Project ID for connecting to the Ethereum network.

Install Dependencies
You can install the required Python libraries by running:

bash
Copy
pip install requests web3
Setup Instructions
Create a Telegram Bot:

Go to BotFather on Telegram and create a new bot.

Note down the API token provided by BotFather.

Get Your Chat ID:

Start a chat with your bot on Telegram.

Use the following URL to get your chat ID:

bash
Copy
https://api.telegram.org/bot<your_bot_token>/getUpdates
Look for the "chat" object in the response and extract your chat_id.

Create an Infura Account:

Go to Infura and create an account.

Create a new Ethereum project and get the project ID for connecting to the Ethereum network.

Update Configuration:

Open whale_wallet_tracker_bot.py and replace the following variables:

TELEGRAM_API_TOKEN: Your Telegram bot API token.

CHAT_ID: Your Telegram chat ID.

INFURA_URL: Your Infura project URL (https://mainnet.infura.io/v3/<your_project_id>).

Running the Bot
Clone the Repository:

Clone the repository to your local machine:

bash
Copy
git clone https://github.com/your-username/whale-wallet-tracker-bot.git
cd whale-wallet-tracker-bot
Start the Bot:

Run the bot using the following command:

bash
Copy
python whale_wallet_tracker_bot.py
The bot will start tracking the whale wallet addresses and will send notifications to your Telegram chat when any relevant transactions are detected.

How It Works
The bot monitors a list of whale wallet addresses.

It fetches the wallet balance and checks the last 10 blocks for transactions related to the tracked wallets.

If any transaction involves one of the whale wallets, the bot sends a message to the specified Telegram chat with details of the transaction:

From Address

To Address

Transaction Value (in Ether)

Transaction Hash

Example Telegram Message:
text
Copy
Transaction detected in Block 12989959:
From: 0x1234...abcd To: 0x5678...efgh Value: 10.5 ETH
Transaction Hash: 0xabcdef1234567890
Customization
You can add or remove Ethereum wallet addresses to the whale_wallets list to track specific wallets.

The bot currently checks the latest 10 blocks for transactions involving the whale wallets. You can modify this number to increase or decrease the block range.

Troubleshooting
Infura Connection Issues: Ensure that your Infura project ID is correct and that you have an active connection to the Ethereum network.

Telegram Messages Not Sent: Verify your Telegram bot token and chat ID. Ensure that the bot has permissions to send messages to your chat.

Missing Transactions: The bot only checks the latest 10 blocks for transactions. If you need real-time tracking, consider implementing a different method for detecting transactions.

License
This project is licensed under the MIT License - see the LICENSE file for details.# whalewallettrackerbot
