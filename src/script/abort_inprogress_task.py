import os
import sys

sys.path.append(f"{os.environ['HOME']}/git/alfred_python/src/")
import config


if __name__ == "__main__":
    inprogress_path = f"/task/inprogress/"

    # InProgressなタスクを1件取得(最新のもの)
    inprogress_response = config.get_notion_api(inprogress_path)
    print(inprogress_response)

    id = inprogress_response["id"]
    title = inprogress_response["title"]
    url = inprogress_response["url"]

    abort_path = f"/task/{id}/abort/"
    abort_response = config.post_notion_api(abort_path, {})
    print(abort_response)

    # # Obsidianのデイリーノートにタスクを追加
    now = config.get_now()
    date_str = config.format_date_extended(now)
    obsidian_daily_note_path = f"{config.OBSIDIAN_DIR}/dailynote/{date_str}.md"
    print(f"Obsidian daily note path: {obsidian_daily_note_path}")
    datetime_str = config.format_time_extended(now)
    task_line = f"({datetime_str}中断) [{title}]({url})\n"
    with open(obsidian_daily_note_path, "a", encoding="utf-8") as f:
        f.write(task_line)
