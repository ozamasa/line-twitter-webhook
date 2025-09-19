import re
import requests
from urllib.parse import urlparse, parse_qs

def resolve_redirect(url):
    """短縮URLを実URLに変換"""
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.url
    except Exception as e:
        print(f"[Error] Failed to resolve URL: {e}")
        return url  # 失敗しても元のURLを返す

def extract_lat_lng_from_url(url):
    """URLから緯度経度を抽出"""
    parsed = urlparse(url)

    # 形式1: ?q=35.6,137.9 や ?ll=35.6,137.9
    query = parse_qs(parsed.query)
    latlng = query.get("q") or query.get("ll")
    if latlng and "," in latlng[0]:
        lat, lng = latlng[0].split(",")
        return lat, lng

    # 形式2: @35.9677247,137.816759 のようなURL
    match = re.search(r"@(-?\d+\.\d+),(-?\d+\.\d+)", url)
    if match:
        lat, lng = match.groups()
        return lat, lng

    return "", ""

def determine_time_period(date_str):
    """10桁の日時文字列から午前・午後・夜を判定"""
    try:
        hour = int(date_str[8:10])
        if 5 <= hour < 12:
            return "午前"
        elif 12 <= hour < 18:
            return "午後"
        else:
            return "夜"
    except Exception:
        return ""