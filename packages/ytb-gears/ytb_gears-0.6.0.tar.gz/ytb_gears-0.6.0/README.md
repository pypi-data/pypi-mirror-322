# YouTube Gears

A Python package for uploading videos to YouTube.

## Service Setup

- <https://console.cloud.google.com/apis/library>
  - YouTube Data API v3
- <https://console.cloud.google.com/apis/credentials>
  - OAuth 2.0 Client ID
    - Application type: Desktop App
    - Download the client secret file (JSON)

## Example

```python
import logging

import tqdm

from ytb_gears import uploader


def main():
    logging.basicConfig(level=logging.WARNING)
    logging.getLogger("ytb_gears").setLevel(logging.INFO)

    credentials_file = "credentials.json"
    video_path = "test.mp4"
    thumbnail_path = "thumbnail.jpg"

    videos = uploader.list_videos(credentials_file, max_results=10)
    for video in videos:
        print(f"id: {video['id']['videoId']}")
        print(f"title: {video['snippet']['title']}")
        print(f"date: {video['snippet']['publishedAt']}")
        print(f"description: {video['snippet']['description']}")
        print("-" * 40)

    if uploader.today_already_uploaded(credentials_file):
        return

    print(f"即将上传视频: {video_path}")

    with tqdm.tqdm(total=100) as pbar:

        def update_progress(progress: float):
            pbar.update(int(progress * 100) - pbar.n)

        uploader.upload(
            video_path,
            credentials_file,
            "YouTube Gears Test Video",
            thumbnail_path,
            "Uploaded by YouTube Gears",
            ["ytb-gears", "test"],
            "22",
            "unlisted",
            progress_callback=update_progress,
        )


main()
```

## Proxy

```python
import os

os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"
```
