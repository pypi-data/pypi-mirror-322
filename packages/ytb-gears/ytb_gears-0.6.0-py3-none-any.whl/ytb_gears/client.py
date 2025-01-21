import argparse
import logging

import google_auth_oauthlib.flow
import googleapiclient.discovery
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

logger = logging.getLogger(__name__)


def sign_in(client_secret_file: str, credentials_file: str):
    """
    通过 OAuth2 登录

    :param client_secret_file: 客户端密钥文件路径
    :param credentials_file: 凭证文件路径
    """
    logger.info("通过 OAuth2 登录")

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secret_file,
        scopes=[
            "https://www.googleapis.com/auth/youtube.readonly",
            "https://www.googleapis.com/auth/youtube.upload",
        ],
    )

    credentials = flow.run_local_server(port=0)

    with open(credentials_file, "w", encoding="utf-8") as f:
        f.write(credentials.to_json())

    logger.info(f"登录成功, 凭证文件: {credentials_file}")


def get_youtube(credentials_file: str):
    """
    获取 YouTube 客户端对象

    :param credentials_file: 凭证文件路径
    :return: YouTube 客户端对象
    """
    logger.info("通过凭证文件登录")

    credentials = Credentials.from_authorized_user_file(credentials_file)

    if credentials and credentials.token is not None:
        if credentials.expired:
            credentials.refresh(Request())
            logger.info("更新 token")

            with open(credentials_file, "w", encoding="utf-8") as f:
                f.write(credentials.to_json())

    youtube = googleapiclient.discovery.build(
        "youtube",
        "v3",
        credentials=credentials,
    )

    return youtube


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("client_secret", help="客户端密钥文件路径")
    parser.add_argument("credentials", help="凭证文件路径")
    args = parser.parse_args()
    sign_in(args.client_secret, args.credentials)
