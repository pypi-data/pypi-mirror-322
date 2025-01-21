#!/usr/bin/env python3

# 安装依赖
# pip3 install tqdm ytb-gears

import logging
import os

import tqdm

from ytb_gears import uploader

# 代理设置
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"


def main():
    # 设置日志级别
    logging.basicConfig(level=logging.WARNING)
    logging.getLogger("ytb_gears").setLevel(logging.INFO)

    # 凭证文件路径
    credentials_file = "credentials.json"
    # 待上传的视频文件
    video_path = "test.mp4"
    # 封面图片文件，如果使用默认图片，可以设置为 None
    thumbnail_path = None

    # 列出已上传的视频，最多列出 10 个
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
            # 上传视频的标题
            "YouTube Gears Test Video",
            thumbnail_path,
            # 上传视频的描述
            "Uploaded by YouTube Gears",
            # 上传视频的标签
            ["ytb-gears", "test"],
            # 上传视频的类别
            "22",
            # 上传视频的隐私设置
            "public",
            progress_callback=update_progress,
        )


main()
