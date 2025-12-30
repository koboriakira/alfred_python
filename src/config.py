# よく利用される準備をまとめて行う

import os
import subprocess
from datetime import date, datetime, timedelta, timezone
from difflib import SequenceMatcher
from pathlib import Path

import requests
from dotenv import load_dotenv
from slack_sdk import WebClient

HOME = str(Path.home())
JST = timezone(timedelta(hours=+9), "JST")

# 1. dotenvの読み込み
load_dotenv(f"{HOME}/git/alfred_python/.env")

# 2. グローバルな変数の宣言
LAMBDA_SLACK_CONCIERGE_API_DOMAIN = os.environ.get("LAMBDA_SLACK_CONCIERGE_API_DOMAIN", "")
LAMBDA_GOOGLE_CALENDAR_API_DOMAIN = os.environ.get("LAMBDA_GOOGLE_CALENDAR_API_DOMAIN", "")
LAMBDA_NOTION_API_DOMAIN = os.environ.get("LAMBDA_NOTION_API_DOMAIN", "")
LAMBDA_SPOTIFY_API_DOMAIN = os.environ.get("LAMBDA_SPOTIFY_API_DOMAIN", "")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET", "")
LAMBDA_TWITTER_API_DOMAIN = os.environ.get("LAMBDA_TWITTER_API_DOMAIN", "")
NOTION_SECRET = os.environ.get("NOTION_SECRET", "")
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "")
SLACK_USER_TOKEN = os.environ.get("SLACK_USER_TOKEN", "")

INBOX_CHANNEL = "C05GUTE35RU"  # inboxのチャンネルID
GIT_PROJECT_DIR = f"{HOME}/git/alfred_python"
BLOG_DIR = f"{HOME}/git/blog"
OBSIDIAN_DIR = f"{HOME}/Library/Mobile Documents/iCloud~md~obsidian/Documents/my-vault"

# 3. ライブラリを利用した汎用メソッドの定義


def post_notion_api(
    path: str,
    body: dict,
) -> None:
    headers = {
        "access-token": NOTION_SECRET,
    }
    url = LAMBDA_NOTION_API_DOMAIN + path
    requests.post(url, json=body, timeout=10, headers=headers)


def get_notion_api(
    path: str,
    params: dict = {},
):
    headers = {
        "access-token": NOTION_SECRET,
    }
    url = LAMBDA_NOTION_API_DOMAIN + path
    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        raise Exception("APIからデータを取得できませんでした")
    response_json = response.json()
    return response_json["data"]


def post_slack_concierge_api(path: str):
    url = LAMBDA_SLACK_CONCIERGE_API_DOMAIN + path
    requests.post(url, timeout=10)


def post_to_inbox(query: str) -> None:
    client = WebClient(token=SLACK_USER_TOKEN)
    client.chat_postMessage(channel=INBOX_CHANNEL, text=query)


def get_now() -> datetime:
    return datetime.now(JST)


def get_today() -> date:
    """
    今日の日付を取得する
    ただし、翌日の2時までは今日とする
    """
    now = get_now()
    today = now - timedelta(days=1) if now.hour < 2 else now  # noqa: PLR2004
    return today.date()


def run_process(command: list[str], check: bool = False) -> None:
    subprocess.run(command, check=check)


def filter_dict_list(items: list[dict], key: str, search_query: str) -> list[dict]:
    """
    dictのリストから、指定のキーに検索クエリが含まれる要素のみをフィルタリングする

    Args:
        items (list[dict]): フィルタリング対象のdictのリスト
        key (str): フィルタリング対象のキー
        search_query (str): 検索クエリ

    Returns:
        list[dict]: フィルタリング後のdictのリスト
    """
    if search_query and search_query != "":
        items = [item for item in items if search_query in item[key]]
        # itemsが複数ある場合は、類似度が高い順にソート
        items.sort(
            key=lambda item: SequenceMatcher(None, search_query, item[key]).ratio(),
            reverse=True,
        )
    return items


def create_obsidian_markdown(
    title: str,
    content: str,
    subdir: str = "",
) -> Path:
    """
    OBSIDIAN_DIR以下に新規マークダウンファイルを作成する

    Args:
        title (str): ファイルタイトル（拡張子なし）
        content (str): ファイルに書き込むテキスト内容
        subdir (str): OBSIDIAN_DIR以下のサブディレクトリパス（オプション、デフォルトは空文字列）

    Returns:
        Path: 作成したファイルのパス

    Raises:
        ValueError: titleが空の場合
    """
    if not title:
        raise ValueError("タイトルは空にできません")

    # ファイル名にマークダウン拡張子を追加
    filename = f"{title}.md"

    # 保存先ディレクトリを決定
    target_dir = Path(OBSIDIAN_DIR)
    if subdir:
        target_dir = target_dir / subdir

    # ディレクトリが存在しない場合は作成
    target_dir.mkdir(parents=True, exist_ok=True)

    # ファイルパスを作成
    file_path = target_dir / filename

    # ファイルに書き込み
    file_path.write_text(content, encoding="utf-8")

    return file_path
