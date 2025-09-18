import yaml
from jinja2 import Template

def load_templates(path="tweet_templates.yml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

TEMPLATES = load_templates()

def build_tweet(parsed: dict) -> str:
    keyword = parsed.get("keyword")
    if keyword not in TEMPLATES:
        keyword = "未定義"

    template_str = TEMPLATES[keyword]["template"]
    template = Template(template_str)
    return template.render(**parsed)
