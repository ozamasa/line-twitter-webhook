import os
import tweepy

def post_tweet(text, media_path=None):
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

    if not all([consumer_key, consumer_secret, access_token, access_token_secret, bearer_token]):
        print("[Error] Twitter API credentials are missing.")
        return False

    # v1.1 用 (media upload)
    auth_v1 = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret, access_token, access_token_secret
    )
    api_v1 = tweepy.API(auth_v1)

    # v2 用 (tweet post)
    client_v2 = tweepy.Client(
        bearer_token=bearer_token,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    media_id = None
    if media_path:
        try:
            media = api_v1.media_upload(media_path)
            media_id = media.media_id
            print("[Media] Uploaded:", media_path)
        except Exception as e:
            print("[Media] Upload failed:", e)
            return False

    try:
        if media_id:
            response = client_v2.create_tweet(text=text, media_ids=[media_id])
        else:
            response = client_v2.create_tweet(text=text)
        print("[Tweet] Posted successfully:", response)
        return True
    except Exception as e:
        print("[Tweet] Failed to post:", e)
        return False