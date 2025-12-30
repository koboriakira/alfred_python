import os
import sys

sys.path.append(f"{os.environ['HOME']}/git/alfred_python/src/")
import config

def get_task_title(response: dict) -> str:
    if not response:
        return "UnknownTask"
    if "data" not in response:
        return "UnknownTask"
    task_data = response["data"]
    if "title" not in task_data:
        return "UnknownTask"
    return task_data["title"]


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: start_new_task.py <task_description>")
        sys.exit(1)
    task_id = sys.argv[1]

    path = f"/task/{task_id}/start/"
    start_response = config.post_notion_api(path, {})
    print(start_response)

    # Obsidianのデイリーノートにタスクを追加
    title = get_task_title(start_response)
    url = start_response["data"]["url"]
    now = config.get_now()
    date_str = config.format_date_extended(now)
    obsidian_daily_note_path = f"{config.OBSIDIAN_DIR}/dailynote/{date_str}.md"
    print(f"Obsidian daily note path: {obsidian_daily_note_path}")
    datetime_str = config.format_time_extended(now)
    task_line = f"({datetime_str}開始) [{title}]({url})\n"
    with open(obsidian_daily_note_path, "a", encoding="utf-8") as f:
        f.write(task_line)


    # 後続のスクリプトにタイトルを渡すために出力する
    print(title)
