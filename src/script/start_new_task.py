"""新しいタスクを開始し、Notionに登録するスクリプト。

Obsidianのデイリーノートにタスクを追加し、
NotionのタスクAPIに新しいタスクを作成します。
"""
from datetime import timedelta
import os
import sys
from pathlib import Path
import re

sys.path.append(f"{os.environ['HOME']}/git/alfred_python/src/")

import config

def append_to_obsidian_daily_note(title: str) -> None:
    """タイトルテキストを今日のObsidianデイリーノートの末尾に追加する。

    ファイルが存在しない場合、この関数は何もせずに終了します。

    Args:
        title (str): デイリーノートに追加するテキスト
    """
    today = config.get_today().strftime("%Y-%m-%d")
    daily_note_path = Path(f"{config.OBSIDIAN_DIR}/dailynote/{today}.md")

    # Skip if the file doesn't exist
    if not daily_note_path.exists():
        return

    # Check if the last line is empty
    with open(daily_note_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Determine if we need to add a newline before the content
    if content and not content.endswith('\n'):
        prefix = '\n'
    elif content and re.search(r'\n$', content):
        # Last line is empty (ends with newline)
        prefix = ''
    else:
        # Empty file
        prefix = ''

    # Append the link to the end of the file
    with open(daily_note_path, "a", encoding="utf-8") as file:
        task_filename = f"task_{title}"
        task_link = f"[[{task_filename}|{title}]]"
        file.write(f"{prefix}- [ ] {task_link}\n")

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: start_new_task.py <task_description>")
        sys.exit(1)
    title = sys.argv[1]
    start = config.get_now()

    # Notionにタスクを作成
    body = {
        "title": title,
        "start_date": start.isoformat(),
        "status": "InProgress",
    }
    config.post_notion_api("/task/", body)

    #`screenocr split "title"`コマンドを実行する
    screenocr_result = config.run_process(
        ["screenocr", "split", f"\"{title}\""],
    )
    # screenocr_resultの1行目をJSONLファイルパスとして取得
    jsonl_file_path = Path(screenocr_result.strip().splitlines()[0])

    # Obsidianにタスクを作成
    config.create_obsidian_markdown(
        title=f"task_{title}",
        content="",
        subdir="00_Task",
        frontmatter={
            "screenocr_jsonl": str(jsonl_file_path),
        },
    )
    append_to_obsidian_daily_note(title)
