
import os
import yaml
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
from utils.twitter import post_tweet_with_media
from utils.parser import parse_message

app = Flask(__name__)

LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

if LINE_CHANNEL_SECRET is None or LINE_CHANNEL_ACCESS_TOKEN is None:
    print("[Error] LINE environment variables not set.")
    exit(1)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

with open("templates.yaml", encoding="utf-8") as f:
    templates = yaml.safe_load(f)

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    print("[Webhook] Received:", body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    data = parse_message(event.message.text)
    if data is None:
        print("[Error] Failed to parse message.")
        return

    keyword = data["keyword"]
    datetime_str = data["datetime"]
    location = data["location"]
    url = data["url"]
    extra = data["extra"]

    template_info = templates.get(keyword, templates.get("未定義"))
    template = template_info["template"]

    tweet_text = template.format(
        keyword=keyword,
        datetime=datetime_str,
        location=location,
        url=url,
        extra=extra
    )

    result = post_tweet_with_media(tweet_text, None)
    print("[Result]", result)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
