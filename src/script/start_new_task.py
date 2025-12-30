"""新しいタスクを開始し、Notionに登録するスクリプト。

Obsidianのデイリーノートにタスクを追加し、
NotionのタスクAPIに新しいタスクを作成します。
"""
import os
import sys

sys.path.append(f"{os.environ['HOME']}/git/alfred_python/src/")

import config


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: start_new_task.py <task_description>")
        sys.exit(1)
    title = sys.argv[1]
    jsonl_filepath = sys.argv[2] if len(sys.argv) > 2 else None
    start = config.get_now()
    print(f"title: {title}, start: {start}, jsonl_filepath: {jsonl_filepath}")

    # Notionにタスクを作成
    body = {
        "title": title,
        "start_date": start.isoformat(),
        "status": "InProgress",
    }
    config.post_notion_api("/task/", body)
    print(f"Created Notion task: {title}")
