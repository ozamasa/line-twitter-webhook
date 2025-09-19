import os
import tweepy

def post_tweet(text, media_path=None):
    # 環境変数からトークン取得（v1.1用）
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        print("[Error] Twitter API credentials are missing.")
        return False

    # OAuth1 認証（v1.1）
    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret, access_token, access_token_secret
    )
    api = tweepy.API(auth)

    try:
        if media_path:
            media = api.media_upload(media_path)
            response = api.update_status(status=text, media_ids=[media.media_id])
        else:
            response = api.update_status(status=text)
        print("[Tweet] Posted successfully:", response)
        return True
    except Exception as e:
        print("[Tweet] Failed to post:", e)
        return False