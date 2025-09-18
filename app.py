from flask import Flask, request, abort
from datetime import datetime
from template_loader import build_tweet
from tweet import post_tweet
import os
import requests

app = Flask(__name__)
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_json()
    try:
        event = body["events"][0]
        if event["type"] != "message" or event["message"]["type"] != "text":
            return "Ignored", 200

        msg = event["message"]["text"]
        parsed = parse_message(msg)
        tweet_text = build_tweet(parsed)

        result = post_tweet(tweet_text)
        if result.get("code") == 200:
            reply_to_line(event["replyToken"], "✅ Twitterに投稿しました")
        else:
            reply_to_line(event["replyToken"], f"⚠️ 投稿失敗: {result.get('error')}")
    except Exception as e:
        print(f"[Error] {type(e).__name__}: {e}")
        abort(400)

    return "OK", 200

def parse_message(message: str):
    lines = message.strip().split('\n')
    if len(lines) < 4:
        raise ValueError("メッセージには最低4行必要")

    keyword = lines[0]
    date_str = lines[1]
    location = lines[2]
    link = lines[3]
    extra = lines[4] if len(lines) >= 5 else ""

    dt = datetime.strptime(date_str, "%Y%m%d%H%M")
    dt_jp = dt.strftime("%Y年%m月%d日%H時%M分")

    return {
        "keyword": keyword,
        "datetime": dt_jp,
        "location": location,
        "link": link,
        "extra": extra
    }

def reply_to_line(reply_token: str, text: str):
    headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": text}]
    }
    r = requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=payload)
    print("[LINE reply status]", r.status_code, r.text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))