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

# Bez nagłówków przeglądarki Cloudflare oddaje stronę HTML "Just a moment..."
# zamiast JSON-a, a wtedy .json() wywala się na "Expecting value: line 1 column 1".
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8",
    "Referer": "https://claude.ai/settings/usage",
}

session = requests.Session()
session.headers.update(HEADERS)
session.cookies.set("sessionKey", SESSION_KEY, domain="claude.ai")

current_percent = 0
current_tooltip = "Ladowanie..."


def fetch_usage():
    global current_percent, current_tooltip
    try:
        response = session.get(URL, timeout=10)

        if response.status_code in (401, 403):
            current_tooltip = (
                f"Blad {response.status_code}: token wygasl lub jest "
                "odrzucany - wklej swiezy sessionKey do config.json"
            )
            return
        response.raise_for_status()

        if "application/json" not in response.headers.get("content-type", ""):
            current_tooltip = "Blad: serwer zwrocil strone HTML zamiast danych"
            return

        data = response.json()

        session_percent = round(data["five_hour"]["utilization"])
        weekly_percent = round(data["seven_day"]["utilization"])

        current_percent = session_percent
        current_tooltip = f"Sesja: {session_percent}% | Tydzien: {weekly_percent}%"
    except Exception as e:
        current_tooltip = f"Blad: {e}"


def fit_font(draw, text, box=248, max_size=240):
    """Najwiekszy rozmiar czcionki, przy ktorym tekst miesci sie w ikonie."""
    for size in range(max_size, 23, -4):
        try:
            font = ImageFont.truetype("arialbd.ttf", size)
        except OSError:
            return ImageFont.load_default(), max(1, size // 70)
        stroke = max(1, size // 70)
        bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
        if bbox[2] - bbox[0] <= box and bbox[3] - bbox[1] <= box:
            return font, stroke
    return ImageFont.load_default(), 2


def make_icon(percent):
    img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if percent < 50:
        color = (46, 204, 113, 255)
    elif percent < 80:
        color = (241, 196, 15, 255)
    else:
        color = (231, 76, 60, 255)

    text = f"{percent}%"
    font, stroke = fit_font(draw, text)
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    x = (256 - (bbox[2] - bbox[0])) / 2 - bbox[0]
    y = (256 - (bbox[3] - bbox[1])) / 2 - bbox[1]

    draw.text(
        (x, y),
        text,
        fill=color,
        font=font,
        stroke_width=stroke,
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
