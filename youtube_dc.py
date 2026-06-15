import feedparser
import requests
import os

CHANNEL_ID = "UCnQIqXNe5QSs3fzFxXII7Rg"

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

LAST_VIDEO_FILE = "last_video.txt"

def get_latest_video():
feed = feedparser.parse(
f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
)

if not feed.entries:
    return None

video = feed.entries[0]

return {
    "id": video.yt_videoid,
    "title": video.title,
    "url": video.link
}

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

latest_video = get_latest_video()

if latest_video is None:
print("Video bulunamadı.")
raise SystemExit()

if not os.path.exists(LAST_VIDEO_FILE):
with open(LAST_VIDEO_FILE, "w", encoding="utf8") as f:
f.write(latest_video["id"])

print("İlk kurulum tamamlandı.")
raise SystemExit()

with open(LAST_VIDEO_FILE, "r", encoding="utf8") as f:
last_video_id = f.read().strip()

if latest_video["id"] != last_video_id:

send_to_discord(latest_video)

with open(LAST_VIDEO_FILE, "w", encoding="utf8") as f:
    f.write(latest_video["id"])

print("Yeni video gönderildi.")

else:
print("Yeni video yok.")
