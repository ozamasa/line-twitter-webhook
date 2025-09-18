import os
import yaml
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
from utils.twitter import post_tweet
from datetime import datetime

app = Flask(__name__)

# 環境変数
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

if LINE_CHANNEL_SECRET is None or LINE_CHANNEL_ACCESS_TOKEN is None:
    print("[Error] LINE environment variables not set.")
    exit(1)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# テンプレート読み込み
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
    text = event.message.text.strip()
    lines = text.split("\n")
    if len(lines) < 4:
        print("[Error] Invalid format.")
        return

    keyword = lines[0].strip()
    date_str = lines[1].strip()
    location = lines[2].strip()
    url = lines[3].strip()
    extra = lines[4].strip() if len(lines) >= 5 else ""

    try:
        dt = datetime.strptime(date_str, "%Y%m%d%H%M")
        datetime_str = dt.strftime("%Y年%m月%d日%H時%M分ごろ")
    except ValueError:
        datetime_str = date_str

    # テンプレート取得（定義なければ未定義を使用）
    template_info = templates.get(keyword, templates.get("未定義"))
    template = template_info["template"]

    tweet_text = template.format(
        keyword=keyword,
        datetime=datetime_str,
        location=location,
        url=url,
        extra=extra
    )

    print(f"[Tweet] Text: {tweet_text}")
    result = post_tweet(tweet_text)
    print("[Result]", result)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))