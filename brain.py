# this is script is made for learning the basics of praw
import praw


reddit_instance = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     username=username,
                     password=password,
                     user_agent="test_bot")

subreddit = reddit_instance.subreddit("testingground4bots")

#commenting 
submission = reddit_instance.submission("1gcropi")
comments =submission.comments

for comment in comments:
    if "You" in comment.body:
        comment.reply("Iam bot sorry for spamming Hello there! I noticed your comment.")
    
# posting
#subreddit.submit(title="test post", selftext=" hello world! testing .... test")

# getting top posts
# top25_posts = subreddit.hot(limit=25,time_filter="all")
# #top25 = subreddit.hot(limit=25,time_filter="week")

# for submission in top25:
#     print(f"Title: {submission.title}")