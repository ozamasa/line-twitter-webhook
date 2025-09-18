from datetime import datetime

def parse_message(text):
    lines = text.strip().split("\n")
    if len(lines) < 4:
        return None

    keyword = lines[0].strip()
    date_str = lines[1].strip()
    location = lines[2].strip()
    url = lines[3].strip()
    extra = lines[4].strip() if len(lines) >= 5 else ""

    try:
        dt = datetime.strptime(date_str, "%Y%m%d%H%M")
        datetime_str = dt.strftime("%Y年%m月%d日%H時%M分")
    except ValueError:
        datetime_str = date_str

    return {
        "keyword": keyword,
        "datetime": datetime_str,
        "location": location,
        "url": url,
        "extra": extra
    }
