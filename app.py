import os
from flask import Flask, request
from dotenv import load_dotenv
from utils.twitter import post_tweet
from utils.template import render_alert

load_dotenv()
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        print("[Webhook] Received:", data)

        events = data.get("events", [])
        if not events:
            return "No event", 400

        message = events[0].get("message", {})
        if message.get("type") != "text":
            return "Not text", 200

        text = message.get("text", "").strip()
        lines = text.splitlines()

        if len(lines) < 4:
            print(f"[Error] Invalid format: {lines}")
            return "Invalid format", 400

        keyword = lines[0].strip()
        date_str = lines[1].strip()
        location = lines[2].strip()
        url_or_note = lines[3].strip()
        extra = lines[4].strip() if len(lines) > 4 else ""

        tweet = render_alert(
            keyword=keyword,
            date_str=date_str,
            location=location,
            url_or_note=url_or_note,
            extra=extra
        )

        result = post_tweet(tweet)
        if result["code"] == 200:
            return "OK", 200
        else:
            return result["error"], result["code"]

    except Exception as e:
        print(f"[Exception] {type(e).__name__}: {e}")
        return f"Server error: {e}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)