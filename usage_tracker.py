import json
import threading
import time
from pathlib import Path

import requests
import pystray
from PIL import Image, ImageDraw, ImageFont

CONFIG_PATH = Path(__file__).parent / "config.json"

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

SESSION_KEY = config["session_key"]
ORG_ID = config["org_id"]
REFRESH_SECONDS = config.get("refresh_seconds", 60)

URL = f"https://claude.ai/api/organizations/{ORG_ID}/usage"

session = requests.Session()
session.cookies.set("sessionKey", SESSION_KEY, domain="claude.ai")

current_percent = 0
current_tooltip = "Ladowanie..."


def fetch_usage():
    global current_percent, current_tooltip
    try:
        response = session.get(URL, timeout=10)
        data = response.json()

        session_percent = data["five_hour"]["utilization"]
        weekly_percent = data["seven_day"]["utilization"]

        current_percent = int(session_percent)
        current_tooltip = f"Sesja: {session_percent}% | Tydzien: {weekly_percent}%"
    except Exception as e:
        current_tooltip = f"Blad: {e}"


def make_icon(percent):
    img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if percent < 50:
        color = (46, 204, 113, 255)
    elif percent < 80:
        color = (241, 196, 15, 255)
    else:
        color = (231, 76, 60, 255)

    try:
        font = ImageFont.truetype("arialbd.ttf", 240)
    except Exception:
        font = ImageFont.load_default()

    text = str(percent)
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(
        ((256 - w) / 2, (256 - h) / 2 - bbox[1]),
        text,
        fill=color,
        font=font,
        stroke_width=6,
        stroke_fill=(0, 0, 0, 255),
    )

    return img


def update_loop(icon):
    while True:
        fetch_usage()
        icon.icon = make_icon(current_percent)
        icon.title = current_tooltip
        time.sleep(REFRESH_SECONDS)


def on_quit(icon, item):
    icon.stop()


icon = pystray.Icon(
    "claude_usage",
    make_icon(0),
    "Claude Usage",
    menu=pystray.Menu(pystray.MenuItem("Zamknij", on_quit)),
)

threading.Thread(target=update_loop, args=(icon,), daemon=True).start()
icon.run()
