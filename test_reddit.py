# test_reddit.py
import praw
from dotenv import load_dotenv
import os

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT')
)

try:
    # Tenta acessar um subreddit público
    for post in reddit.subreddit('news').hot(limit=1):
        print(f"Conexão bem sucedida! Post encontrado: {post.title}")
except Exception as e:
    print(f"Erro na conexão: {e}")