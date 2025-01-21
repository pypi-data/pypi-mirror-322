import logging
from datetime import datetime, timezone
from typing import Callable, Literal, Optional

from googleapiclient.http import HttpRequest, MediaFileUpload

from .client import get_youtube

logger = logging.getLogger(__name__)


def list_videos(credentials_file: str, max_results: int = 10):
    """
    列出视频

    :param credentials_file: 凭证文件路径
    :param max_results: 最大结果数
    :return: 视频列表
    """
    youtube = get_youtube(credentials_file)

    request = youtube.search().list(
        part="snippet", forMine=True, maxResults=max_results, order="date", type="video"
    )
    response = request.execute()
    items = response.get("items", [])

    if not isinstance(items, list):
        return []
    else:
        return items


def today_already_uploaded(credentials_file: str) -> bool:
    """
    检查今天是否已经上传过视频

    :param credentials_file: 凭证文件路径
    :return: 是否已经上传过视频
    """
    items = list_videos(credentials_file, max_results=1)

    if len(items) == 0:
        logger.warning("没有找到视频")
        return False

    video = items[0]
    upload_date = datetime.strptime(
        video["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"
    ).replace(tzinfo=timezone.utc)

    today = datetime.now(timezone.utc)

    is_today = (
        upload_date.year == today.year
        and upload_date.month == today.month
        and upload_date.day == today.day
    )

    if is_today:
        logger.info(f"今天已经上传过视频: {video['snippet']['title']}")
        logger.info(f"上传时间: {upload_date}")

    return is_today


def upload(
    video_path: str,
    credentials_file: str,
    title: str,
    thumbnail_path: Optional[str] = None,
    description: str = "",
    tags: list[str] = [],
    category_id: str = "22",
    privacy_status: Literal["public", "unlisted", "private"] = "public",
    progress_callback: Optional[Callable[[float], None]] = None,
):
    """
    上传视频

    :param video_path: 视频文件路径
    :param credentials_file: 凭证文件路径
    :param title: 视频标题
    :param thumbnail_path: 缩略图文件路径
    :param description: 视频简介
    :param tags: 视频关键字
    :param category_id: 视频分类
    :param privacy_status: 隐私权限, public-公开 unlisted-未公开 private-私有
    :param progress_callback: 上传进度回调函数
    """
    body = dict(
        snippet=dict(
            title=title,
            description=description,
            tags=tags,
            categoryId=category_id,
        ),
        status=dict(privacyStatus=privacy_status),
    )

    media = MediaFileUpload(
        video_path,
        chunksize=4 * 1024 * 1024,
        resumable=True,
    )

    youtube = get_youtube(credentials_file)

    insert_request: HttpRequest = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=media,
    )

    insert_response = None

    while insert_response is None:
        status, insert_response = insert_request.next_chunk()

        if status and progress_callback:
            progress_callback(status.progress())

    if progress_callback:
        progress_callback(1.0)

    logger.info(f"上传视频成功: {insert_response}")

    if thumbnail_path:
        set_request = youtube.thumbnails().set(
            videoId=insert_response["id"],
            media_body=MediaFileUpload(thumbnail_path),
        )

        set_response = set_request.execute()

        logger.info(f"设置缩略图成功: {set_response}")

        return (insert_response, set_response)
    else:
        return (insert_response,)
