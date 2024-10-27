import os
import praw
import openai
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables for Reddit and OpenAI
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Reddit and OpenAI clients
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD,
    user_agent="my_reddit_bot_v1"
)

openai.api_key = OPENAI_API_KEY

models = openai.Model.list()
print([model.id for model in models['data']])

# Function to generate ChatGPT response
def generate_response(comment_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Respond in a humble, neutral, and human-like manner."},
                {"role": "user", "content": comment_text}
            ],
            max_tokens=150,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print("Error generating response:", e)
        return None


# Bot function to reply to top 25 comments in specified subreddits
def run_bot(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    
    # Get top 25 hot posts
    for submission in subreddit.hot(limit=25):
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            if comment.author == reddit.user.me():
                # Avoid replying to yourself
                continue

            # Generate a response
            response_text = generate_response(comment.body)
            if response_text:
                try:
                    # Reply to the comment
                    comment.reply(response_text)
                    
                    # Pause to avoid hitting Reddit's rate limit
                    time.sleep(30)
                except Exception as e:
                    print("Error replying to comment:", e)
                finally:
                    # Short pause between each comment to prevent rate limiting
                    time.sleep(5)

# Main function to run the bot on specific subreddits
if __name__ == "__main__":
    subreddit_list = input("Enter the subreddit names separated by commas (e.g., cats, CatPictures): ")
    subreddits = [s.strip() for s in subreddit_list.split(",")]
    for subreddit_name in subreddits:
        print(f"Running bot on subreddit: {subreddit_name}")
        run_bot(subreddit_name)
