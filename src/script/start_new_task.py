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
    response = config.post_notion_api("/task/", body)
    print(f"Created Notion task: {title}")
    print(response["data"])
    notion_page_url = response["data"]["url"]

    # Obsidianのデイリーノートにタスクを追加
    date_str = config.format_date_extended(start)
    obsidian_daily_note_path = f"{config.OBSIDIAN_DIR}/dailynote/{date_str}.md"
    print(f"Obsidian daily note path: {obsidian_daily_note_path}")
    datetime_str = config.format_time_extended(start)
    task_line = f"- [ ] ({datetime_str}開始) [{title}]({notion_page_url})\n"
    with open(obsidian_daily_note_path, "a", encoding="utf-8") as f:
        f.write(task_line)
