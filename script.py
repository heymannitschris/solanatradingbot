import requests
import pandas as pd
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from telegram import Bot
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import time

# Load environment variables from .env file
load_dotenv()

# Telegram Bot credentials
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TOXI_SOLANA_BOT_ID = "@toxi_solana_bot"  # Bot username (ensure the bot's username is correct)

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

# Setup Twitter API access
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

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

# Fetch and parse the Pump.fun board page
def fetch_board_page():
    url = 'https://pump.fun/board'
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
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
    return tokens

# Check contract security using RugCheck API
def check_contract_security(mint_address):
    headers = {'Authorization': f'Bearer {RUGCHECK_API_KEY}'}
    response = requests.get(f'{RUGCHECK_API_URL}check/{mint_address}', headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get('status') == 'good', data.get('top_holder_percentage', 0)
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
    # Compose the message to send to the bot
    buy_command = f"/buy {mint_address}"
    sol_amount = "1"  # Replace with the Sol amount you want to buy
    # You may also need to add a price check or other logic here
    
    # Construct the message to send to the bot
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TOXI_SOLANA_BOT_ID,
        "text": buy_command
    }
    # Send the Buy command to the Toxi Solana Bot
    response = requests.post(url, data=payload)
    
    # If the bot responds with success, we can follow up by sending the Sol amount
    if response.status_code == 200:
        print(f"Buy signal for {mint_address} sent successfully!")
        # Send the Sol amount next (replace this with actual logic for inputting the Sol amount)
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

    # Create and display the word cloud
    print("Generating word cloud...")
    create_wordcloud(all_tokens)

    # Return the sentiment for use in decision-making
    return avg_sentiment

# Main function that integrates everything
def main():
    html = fetch_board_page()
    if html:
        tokens = parse_board_page(html)
        for token in tokens:
            if token['mint_address'] and token['social_media_links']:
                # Perform analysis on token's social media narrative
                avg_sentiment = analyze_twitter_list(LIST_ID)
                
                # Check contract security with RugCheck
                is_good, top_holder_percentage = check_contract_security(token['mint_address'])
                
                # Check if Tweet