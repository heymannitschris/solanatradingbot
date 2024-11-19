import os
import requests
import base64
import time
import tweepy
from dotenv import load_dotenv
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from solana.keypair import Keypair
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Telegram Bot credentials
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TOXI_SOLANA_BOT_ID = os.getenv('TOXI_SOLANA_BOT_ID')  # Bot username (ensure the bot's username is correct)

# RugCheck API credentials
RUGCHECK_API_KEY = os.getenv('RUGCHECK_API_KEY')
RUGCHECK_API_URL = 'https://api.rugcheck.xyz/v1/'

# TweetScout API credentials
TWEETSCOUT_API_KEY = os.getenv('TWEETSCOUT_API_KEY')
TWEETSCOUT_API_URL = 'https://api.tweetscout.io/'

# Twitter API credentials
API_KEY = os.getenv('TWITTER_API_KEY')
API_SECRET_KEY = os.getenv('TWITTER_API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# Solana private key (base64 encoded) from .env file
SOLANA_PRIVATE_KEY_BASE64 = os.getenv('SOLANA_PRIVATE_KEY')

# Setup Twitter API access
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Initialize Solana keypair from the private key
if SOLANA_PRIVATE_KEY_BASE64:
    solana_private_key = base64.b64decode(SOLANA_PRIVATE_KEY_BASE64)
    keypair = Keypair.from_secret_key(solana_private_key)
    print("Solana keypair loaded successfully!")
else:
    print("Solana private key not found in .env file!")

# Define the list ID for the Twitter list you want to analyze
LIST_ID = '1544277446526222336'

# Function to fetch user IDs from the Twitter list
def get_list_members(list_id):
    members = []
    for member in tweepy.Cursor(api.get_list_members, list_id=list_id).items():
        members.append(member.screen_name)
    return members

# Function to fetch recent tweets from a list of user IDs
def get_recent_tweets(usernames, count=100):
    tweets = []
    for username in usernames:
        try:
            for tweet in tweepy.Cursor(api.user_timeline, screen_name=username, count=count, tweet_mode='extended').items():
                tweets.append(tweet.full_text)
        except tweepy.TweepError as e:
            print(f"Error fetching tweets for {username}: {e}")
    return tweets

# Tokenization and cleaning of tweet text
def clean_text(text):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower())
    clean_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
    return clean_tokens

# Analyze sentiment of tweets
def analyze_sentiment(tweets):
    sentiment_scores = []
    for tweet in tweets:
        analysis = TextBlob(tweet)
        sentiment_scores.append(analysis.sentiment.polarity)
    return sentiment_scores

# Create word cloud from tokenized tweets
def create_wordcloud(tokens):
    word_freq = Counter(tokens)
    wordcloud = WordCloud(width=800, height=400).generate_from_frequencies(word_freq)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# Function to fetch the board page with Selenium (and click "I'm ready to pump")
def fetch_board_page_with_selenium():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://pump.fun/")

    try:
        # Wait for the "I'm ready to pump" button and click it
        print("Waiting for 'I'm ready to pump' button to appear...")
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'I\'m ready to pump')]"))).click()
        print("Clicked the 'I'm ready to pump' button successfully.")

        # Wait for the sort button (to sort by creation time)
        print("Waiting for 'sort: featured' button to appear...")
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'sort: featured')]"))).click()
        print("Clicked the 'sort: featured' button successfully.")

        # Wait for the creation time sort option and click it
        print("Waiting for 'sort: creation time' button to appear...")
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'sort: creation time')]"))).click()
        print("Clicked the 'sort: creation time' button successfully.")

        # Wait for the page to load after sorting
        print("Waiting for page to load...")
        time.sleep(5)  # Adjust time as necessary

        # Fetch the page source
        page_source = driver.page_source
        return page_source

    except Exception as e:
        print(f"Error occurred while fetching the board page: {e}")
        driver.quit()
        return None

# Function to parse the board page and extract token details
def parse_board_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    tokens = []

    token_section = soup.find('div', {'class': 'board'})
    if token_section:
        for token_div in token_section.find_all('div', {'class': 'token-entry'}):
            token = {}
            name_tag = token_div.find('span', {'class': 'token-name'})
            if name_tag:
                token['name'] = name_tag.text.strip()

            symbol_tag = token_div.find('span', {'class': 'token-symbol'})
            if symbol_tag:
                token['symbol'] = symbol_tag.text.strip()

            mint_tag = token_div.find('span', {'class': 'token-mint'})
            if mint_tag:
                token['mint_address'] = mint_tag.text.strip()

            social_links = [link.get('href') for link in token_div.find_all('a', {'class': 'social-link'})]
            token['social_media_links'] = social_links
            tokens.append(token)
    
    # Save tokens to CSV
    pd.DataFrame(tokens).to_csv("tokens.csv", index=False)
    
    return tokens

# Check contract security using RugCheck API with Solana signed message
def authenticate_with_rugcheck(message):
    signature = keypair.sign(message.encode('utf-8'))  # Encoding the message to bytes before signing
    signed_message = base64.b64encode(signature).decode('utf-8')  # Base64 encoding the signed message
    
    headers = {
        'Authorization': f'Bearer {RUGCHECK_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'message': message,
        'signature': signed_message
    }
    
    # Send the request to RugCheck API for authentication
    response = requests.post(f'{RUGCHECK_API_URL}auth/login/solana', headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()  # Returns the authenticated response
    else:
        print(f"Failed to authenticate with RugCheck: {response.status_code}")
        return None

# Check contract security using RugCheck API
def check_contract_security(mint_address):
    message = f"Check security for {mint_address}"
    response_data = authenticate_with_rugcheck(message)
    
    if response_data:
        return response_data.get('status') == 'good', response_data.get('top_holder_percentage', 0)
    return False, 0

# Check if the TweetScout score is over 20
def check_tweet_scout_score(twitter_handle):
    headers = {'Authorization': f'Bearer {TWEETSCOUT_API_KEY}'}
    params = {'handle': twitter_handle}
    response = requests.get(f'{TWEETSCOUT_API_URL}check-audience-quality', headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        score = data.get('score', 0)
        return score > 20
    return False

# Send Buy Signal to Toxi Solana Bot
def send_buy_signal_to_toxi_bot(mint_address):
    buy_command = f"/buy {mint_address}"
    sol_amount = "1"  # Replace with the Sol amount you want to buy
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TOXI_SOLANA_BOT_ID,
        "text": buy_command
    }
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print(f"Buy signal for {mint_address} sent successfully!")
        sol_amount_message = f"Amount: {sol_amount} SOL"
        payload_sol = {
            "chat_id": TOXI_SOLANA_BOT_ID,
            "text": sol_amount_message
        }
        response = requests.post(url, data=payload_sol)
        if response.status_code == 200:
            print(f"Sent {sol_amount} SOL for purchase.")
        else:
            print(f"Failed to send Sol amount. Status code: {response.status_code}")
    else:
        print(f"Failed to send buy signal. Status code: {response.status_code}")

# Send message to your Telegram bot
def send_message_to_telegram_bot(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print(f"Message sent to your Telegram bot: {message}")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")

# Main analysis workflow
def analyze_twitter_list(list_id):
    print("Fetching list members...")
    members = get_list_members(list_id)
    print(f"Found {len(members)} members in the list.")

    print("Fetching recent tweets...")
    tweets = get_recent_tweets(members)
    print(f"Fetched {len(tweets)} tweets.")

    # Clean and tokenize the tweets
    all_tokens = []
    for tweet in tweets:
        clean_tokens = clean_text(tweet)
        all_tokens.extend(clean_tokens)

    # Analyze sentiment
    sentiment_scores = analyze_sentiment(tweets)
    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
    print(f"Average Sentiment: {avg_sentiment}")

    # Save tweets and sentiment analysis to CSV
    tweet_data = pd.DataFrame({
        'Tweet': tweets,
        'Sentiment': sentiment_scores
    })
    tweet_data.to_csv("tweets_analysis.csv", index=False)

    # Create and display the word cloud
    print("Generating word cloud...")
    create_wordcloud(all_tokens)

    # Save word cloud tokens to CSV
    wordcloud_data = pd.DataFrame({'Tokens': all_tokens})
    wordcloud_data.to_csv("wordcloud_tokens.csv", index=False)

    # Return the sentiment for use in decision-making
    return avg_sentiment

# Main function that integrates everything
def main():
    # Fetch the Pump.fun board page
    html = fetch_board_page_with_selenium()
    if html:
        # Parse the board page for tokens
        tokens = parse_board_page(html)
        for token in tokens:
            if token['mint_address'] and token['social_media_links']:
                # Analyze token's social media narrative
                avg_sentiment = analyze_twitter_list(LIST_ID)
                
                # Check the contract security with RugCheck
                is_good, top_holder_percentage = check_contract_security(token['mint_address'])
                
                # Check if TweetScout score is over 20 and the contract is secure
                if is_good and check_tweet_scout_score(token['social_media_links'][0]) and top_holder_percentage < 10:
                    # Send Buy signal to Toxi Solana Bot
                    send_buy_signal_to_toxi_bot(token['mint_address'])

                    # Send a message to your own Telegram bot to notify you
                    message = f"New Token Buy Signal Sent!\nToken Name: {token['name']}\nMint Address: {token['mint_address']}\nSymbol: {token['symbol']}"
                    send_message_to_telegram_bot(message)

                    print(f"Sent Buy signal for {token['name']} to Toxi Solana Bot.")
                    
                    # Save buy signal details to CSV
                    buy_signal_data = pd.DataFrame([{
                        'Token Name': token['name'],
                        'Mint Address': token['mint_address'],
                        'Symbol': token['symbol'],
                        'Sentiment Score': avg_sentiment
                    }])
                    buy_signal_data.to_csv("buy_signals.csv", mode='a', header=not os.path.exists("buy_signals.csv"), index=False)
                else:
                    print(f"Token {token['name']} does not meet criteria.")
    else:
        print("Failed to retrieve the board page.")

# Run the main function periodically
if __name__ == '__main__':
    while True:
        main()
        time.sleep(1800)  # Run every 30 minutes