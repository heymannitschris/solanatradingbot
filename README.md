# Solana Trading Bot

This project is a Python-based bot designed to automate the process of analyzing tokens listed on Pump.fun and trading signals from Twitter. The bot scrapes the latest tokens from Pump.fun, analyzes the sentiment of tweets from a specified Twitter list, and sends trade signals to a Telegram bot.

Features

	•	Token Scraping: The bot scrapes the latest tokens from Pump.fun and fetches details like token names, symbols, mint addresses, and social media links.
	•	Twitter Sentiment Analysis: The bot fetches tweets from a predefined Twitter list and performs sentiment analysis using TextBlob.
	•	Contract Security Check: The bot verifies the contract security of tokens using the RugCheck API.
	•	Telegram Integration: The bot interacts with Telegram bots to send notifications, including buy signals and token details.
	•	Data Logging: Saves token data, sentiment analysis results, and trading actions to CSV files.

Installation

Follow these steps to install and run the bot:

# 1. Clone the Repository
git clone https://github.com/yourusername/solanatradingbot.git
cd solanatradingbot

# 2. Create and Activate a Virtual Environment
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# 3. Install Dependencies
pip install -r requirements.txt

The required dependencies are:
	•	requests: For making HTTP requests.
	•	selenium: For scraping data from the Pump.fun website.
	•	tweepy: For interacting with the Twitter API.
	•	textblob: For sentiment analysis on tweets.
	•	wordcloud: For generating word clouds.
	•	nltk: For natural language processing (tokenization and stop word removal).
	•	matplotlib: For visualizing the sentiment analysis.
	•	pandas: For handling CSV file exports.
	•	webdriver-manager: For managing ChromeDriver for Selenium.
	•	python-dotenv: For managing environment variables securely.

# 4. Set Up Environment Variables
Create a .env file in the project directory and include your API keys and Telegram bot credentials:

# .env file

# Telegram Bot credentials
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-chat-id
TOXI_SOLANA_BOT_ID=your-bot-id

# RugCheck API credentials
RUGCHECK_API_KEY=your-rugcheck-api-key

# TweetScout API credentials
TWEETSCOUT_API_KEY=your-tweetscout-api-key

# Twitter API credentials
TWITTER_API_KEY=your-twitter-api-key
TWITTER_API_SECRET_KEY=your-twitter-api-secret-key
TWITTER_ACCESS_TOKEN=your-twitter-access-token
TWITTER_ACCESS_TOKEN_SECRET=your-twitter-access-token-secret

# 5. Run the Bot
Run the bot by executing the following command:

python script.py

How It Works

	1.	Pump.fun Token Scraping: The bot scrapes tokens listed on Pump.fun, fetching details like token name, symbol, and social media links.
	2.	Twitter Sentiment Analysis: It fetches tweets from a Twitter list and performs sentiment analysis on them.
	3.	Contract Security: The bot verifies the contract security of tokens using RugCheck to ensure that they are safe to buy.
	4.	Buy Signal: If a token passes the sentiment analysis and contract security check, the bot sends a buy signal to a Telegram bot.

Data Files

	•	tokens.csv: Contains the list of tokens fetched from Pump.fun.
	•	buy_signals.csv: Logs the buy signals sent by the bot.
	•	tweets_analysis.csv: Contains the tweets analyzed for sentiment.
	•	wordcloud_tokens.csv: Contains the tokens used to generate the word cloud.

Troubleshooting

Common Issues:

	1.	Bot Can’t Click the ‘I’m Ready to Pump’ Button:
	•	Ensure that the XPath for the button is correctly matched and that the page loads fully before the script interacts with it.
	2.	WebDriver Version Mismatch:
	•	Make sure ChromeDriver matches the installed version of Google Chrome.

Contributing

Feel free to fork this repository and submit a pull request to improve the bot! Contributions are always welcome.
