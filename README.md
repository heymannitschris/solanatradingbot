Solana Trading Bot

This project is a Python-based trading bot for interacting with the Solana blockchain, specifically designed to fetch data, interact with Telegram bots, and scrape data from Telegram Mini Apps. It uses the Telegram Bot API, Selenium, and Solana Web3 to automate actions and provide real-time insights.

Features

	•	Telegram Bot Interaction: Send and receive messages using the Telegram Bot API.
	•	Data Extraction: Scrape data from Telegram Mini Apps (Web-based bots) using Selenium.
	•	Solana Blockchain Interaction: Connect to the Solana blockchain and fetch wallet details.
	•	Twitter Sentiment Analysis: Fetch and analyze tweets from specific Twitter lists.
	•	Automated Trading: The bot sends buy signals based on analysis from multiple sources (Twitter sentiment, RugCheck, etc.).
	•	Data Logging: Save the results (buy signals, sentiment analysis, and token details) to CSV files for record-keeping.

Installation

To get started with the bot, follow the instructions below:

1. Clone the repository
git clone https://github.com/yourusername/solanatradingbot.git
cd solanatradingbot

2. Create and activate a virtual environment
If you’re using venv for Python environment management:
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install required dependencies
pip install -r requirements.txt

Make sure you have all the necessary dependencies installed:
	•	requests: For HTTP requests to APIs.
	•	selenium: For scraping and automating interactions with Telegram Mini Apps.
	•	tweepy: For interacting with the Twitter API.
	•	textblob: For sentiment analysis.
	•	wordcloud: To generate word clouds from Twitter data.
	•	matplotlib: For plotting sentiment analysis results.
	•	nltk: For text processing and tokenization.
	•	pandas: To handle data and save results in CSV files.
	•	webdriver-manager: For managing the WebDriver (used in Selenium).
	•	python-dotenv: To manage environment variables securely.

4. Set up environment variables

Create a .env file in the project directory and add your necessary credentials:

# .env file

# Telegram Bot
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-chat-id
TOXI_SOLANA_BOT_ID=your-bot-id

# Solana
SOLANA_PRIVATE_KEY=your-private-key-in-base64

# RugCheck
RUGCHECK_API_KEY=your-rugcheck-api-key

# TweetScout
TWEETSCOUT_API_KEY=your-tweetscout-api-key

# Twitter API
TWITTER_API_KEY=your-twitter-api-key
TWITTER_API_SECRET_KEY=your-twitter-api-secret-key
TWITTER_ACCESS_TOKEN=your-twitter-access-token
TWITTER_ACCESS_TOKEN_SECRET=your-twitter-access-token-secret

5. Start the bot

Run the script to start the bot:
python script.py

Usage

Once the bot is running, it will:
	1.	Fetch the list of Solana tokens from the Pump.fun board.
	2.	Interact with the Telegram bot to fetch and process data.
	3.	Analyze the sentiment of tweets from the defined Twitter list.
	4.	Check the contract security using the RugCheck API.
	5.	If certain conditions are met (e.g., good contract security, high sentiment score), the bot will send a buy signal to the Toxi Solana bot.

Features in Detail

	•	Twitter Sentiment Analysis: The bot fetches tweets from a specific Twitter list and analyzes the sentiment using TextBlob. Positive sentiment leads to the bot sending a buy signal.
	•	Pump.fun Token Scraping: The bot scrapes the latest tokens from Pump.fun, checks their contract security via RugCheck API, and monitors sentiment using Twitter analysis.
	•	Telegram Integration: The bot sends updates and buy signals via a Telegram Bot to notify you of any trading opportunities.

Files

	•	script.py: The main script that runs the bot and handles all the interactions and analysis.
	•	requirements.txt: A file that lists all the Python dependencies.
	•	.env: The environment variables file containing API keys and tokens.
	•	tokens.csv: CSV file that logs the details of the tokens fetched from Pump.fun.
	•	buy_signals.csv: CSV file that logs the details of the buy signals sent by the bot.
	•	tweets_analysis.csv: CSV file containing the tweets and their sentiment analysis.

Troubleshooting

If you encounter issues, make sure the following:
	•	You have the correct versions of Chrome and ChromeDriver installed and they match.
	•	The Telegram bot has proper permissions and the Telegram chat ID is correctly set.
	•	You have the necessary API keys for RugCheck, TweetScout, and Twitter API.

Contributing

If you’d like to contribute to this project, feel free to submit a pull request or open an issue. All contributions are welcome!