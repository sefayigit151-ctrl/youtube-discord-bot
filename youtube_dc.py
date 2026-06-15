import feedparser
import requests
import time
import os
import datetime

# ==========================
# AYARLAR
# ==========================

CHANNEL_ID = "UCnQIqXNe5QSs3fzFxXII7Rg"

import os

WEBHOOK_URL = os.getenv("https://discord.com/api/webhooks/1516130110179119145/_Qw0nxVEMLRQfnOJdDfh1Da9JRyYHX_jM5uEjytYLO1I5KWvXML3Adl_ZiSasQ3tt-a-")

LAST_VIDEO_FILE = "last_video.txt"

CHECK_INTERVAL = 60

# ==========================
# YOUTUBE
# ==========================

def get_latest_video():
    feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"

    feed = feedparser.parse(feed_url)

    if not feed.entries:
        return None

    video = feed.entries[0]

    return {
        "id": video.yt_videoid,
        "title": video.title,
        "url": video.link
    }

# ==========================
# DISCORD
# ==========================

def send_to_discord(video):

    thumbnail = f"https://i.ytimg.com/vi/{video['id']}/maxresdefault.jpg"

    embed = {
        "title": video["title"],
        "url": video["url"],
        "description": "🎬 Yeni video yayında!",
        "image": {
            "url": thumbnail
        },
        "footer": {
            "text": "Sefa Yiğit YouTube"
        }
    }

    requests.post(
        WEBHOOK_URL,
        json={
            "content": "@everyone",
            "embeds": [embed]
        }
    )

# ==========================
# BOT
# ==========================

print("Bot başlatildi.")

while True:

    try:

        latest_video = get_latest_video()

        if latest_video is None:
            time.sleep(CHECK_INTERVAL)
            continue

        if not os.path.exists(LAST_VIDEO_FILE):

            with open(LAST_VIDEO_FILE, "w", encoding="utf8") as f:
                f.write(latest_video["id"])

            print("İlk kurulum tamamlandi.")
            time.sleep(CHECK_INTERVAL)
            continue

        with open(LAST_VIDEO_FILE, "r", encoding="utf8") as f:
            last_video_id = f.read().strip()

        if latest_video["id"] != last_video_id:

            send_to_discord(latest_video)

            with open(LAST_VIDEO_FILE, "w", encoding="utf8") as f:
                f.write(latest_video["id"])

            print(f"Yeni video gönderildi: {latest_video['title']}")

        else:
            print("Yeni video yok.")

    except Exception as e:

        print("HATA:", e)

        with open("error.log", "a", encoding="utf8") as log:
            log.write(
                f"{datetime.datetime.now()} - {str(e)}\n"
            )

    time.sleep(CHECK_INTERVAL)
