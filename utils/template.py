import yaml
from datetime import datetime
from pathlib import Path
from jinja2 import Template

TEMPLATE_FILE = Path("templates/templates.yml")

def render_alert(keyword, date_str, location, url_or_note, extra=""):
    try:
        templates = yaml.safe_load(TEMPLATE_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[YAML Error] {type(e).__name__}: {e}")
        return f"【{keyword}】\n{date_str} に {location} で情報あり"

    template_data = templates.get(keyword, templates.get("未定義"))
    template_text = template_data["template"]

    dt = datetime.strptime(date_str, "%Y%m%d%H%M")
    dt_str = dt.strftime("%Y年%m月%d日%H時%M分ごろ")

    return Template(template_text).render(
        keyword=keyword,
        date_str=date_str,
        datetime=dt_str,
        location=location,
        map_url=url_or_note,
        url_or_note=url_or_note,
        extra=extra
    )