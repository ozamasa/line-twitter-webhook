
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

def post_tweet_with_media(text: str, media_path: str):
    print(f"[Tweet] Text: {text[:30]}... Media: {media_path}")

    try:
        media_id = None
        if media_path:
            media = api_v1.media_upload(media_path)
            media_id = media.media_id
    except Exception as e:
        print(f"[Upload Error] {type(e).__name__}: {e}")
        return {"code": 500, "error": f"Upload failed: {e}"}

    try:
        response = client_v2.create_tweet(text=text, media_ids=[media_id] if media_id else None)
        print(f"[Tweet OK] id={response.data.get('id')}")
        return {"code": 200, "tweet_id": response.data.get("id")}
    except tweepy.TweepyException as e:
        print(f"[Tweet Error] {e.response.status_code} {e.response.text}")
        return {"code": e.response.status_code, "error": e.response.text}
    except Exception as e:
        print(f"[Tweet Error] {type(e).__name__}: {e}")
        return {"code": 500, "error": f"Tweet failed: {e}"}
