import asyncio
import os
from typing import List

import aiohttp
from yandex_music import Client
from dotenv import load_dotenv
from app.models.music_platform import MusicPlatform
load_dotenv()

YANDEX_TOKEN = os.getenv("YANDEX_TOKEN")
API_URL = os.getenv("API_URL") + '/tracks/'
API_KEY = os.getenv("API_ADMIN_TOKEN")


def load_chart_tracks() -> List[dict]:
    client = Client(token=YANDEX_TOKEN).init()
    chart = client.chart("world").chart

    tracks: List[dict] = []

    for track_short in chart.tracks:
        track = track_short.track

        artists = ", ".join(artist.name for artist in track.artists)

        album_id = track.albums[0].id if track.albums else None
        link = (
            f"https://music.yandex.ru/album/{album_id}/track/{track.id}"
            if album_id
            else None
        )

        tracks.append(
            {
                "title": track.title,
                "author": artists,
                "platform": (
                    MusicPlatform.YANDEX.value
                    if hasattr(MusicPlatform.YANDEX, "value")
                    else str(MusicPlatform.YANDEX)
                ),
                "external_link": link,
            }
        )

    return tracks


async def send_tracks(tracks: List[dict]) -> None:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    async with aiohttp.ClientSession() as session:
        for track in tracks:
            async with session.post(
                API_URL,
                headers=headers,
                json=track,
            ) as response:
                if response.status in (200, 201):
                    print(f"✔ Сохранён: {track['title']}")
                else:
                    print("❌ Ошибка:")
                    print(await response.text())
                    return
            await asyncio.sleep(0.3)


async def main():
    tracks = await asyncio.to_thread(load_chart_tracks)
    await send_tracks(tracks)


if __name__ == "__main__":
    asyncio.run(main())
