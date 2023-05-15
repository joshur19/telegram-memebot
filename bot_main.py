import praw
import telegram
import os
from telegram.ext import Updater

# Initialize Reddit API credentials
reddit = praw.Reddit(client_id='YOUR_CLIENT_ID',
                     client_secret='YOUR_CLIENT_SECRET',
                     username='YOUR_REDDIT_USERNAME',
                     password='YOUR_REDDIT_PASSWORD',
                     user_agent='YOUR_USER_AGENT')

# Initialize Telegram API credentials
bot = telegram.Bot(token='YOUR_TELEGRAM_BOT_TOKEN')

# Define the subreddits to be scraped
subreddits = ['funny', 'pics', 'aww', 'earthporn', 'itookapicture']

# Define a function to get the top two posts of the week from each subreddit
def get_top_posts():
    top_posts = []
    for subreddit in subreddits:
        for submission in reddit.subreddit(subreddit).top('week', limit=2):
            if not submission.over_18 and submission.is_reddit_media_domain and submission.media_only:
                top_posts.append(submission.url)
    return top_posts

# Define a function to send the curated list of images via Telegram
def send_images():
    images = get_top_posts()
    for image in images:
        bot.send_photo(chat_id='YOUR_TELEGRAM_CHAT_ID', photo=image)

# Create an Updater and schedule the send_images function to run weekly
updater = Updater(token='YOUR_TELEGRAM_BOT_TOKEN', use_context=True)
job = updater.job_queue
job.run_repeating(send_images, interval=604800, first=0)

# Start the bot
updater.start_polling()
updater.idle()
