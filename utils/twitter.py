import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

CONSUMER_KEY        = os.getenv("TWITTER_CONSUMER_KEY")
CONSUMER_SECRET     = os.getenv("TWITTER_CONSUMER_SECRET")
ACCESS_TOKEN        = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

auth = tweepy.OAuth1UserHandler(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)
api_v1 = tweepy.API(auth)

client_v2 = tweepy.Client(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

def post_tweet(text: str):
    try:
        response = client_v2.create_tweet(text=text)
        print(f"[Tweet OK] id={response.data.get('id')}")
        return {"code": 200, "tweet_id": response.data.get("id")}
    except tweepy.TweepyException as e:
        print(f"[Tweet Error] {e.response.status_code} {e.response.text}")
        return {"code": e.response.status_code, "error": e.response.text}
    except Exception as e:
        print(f"[Tweet Error] {type(e).__name__}: {e}")
        return {"code": 500, "error": str(e)}