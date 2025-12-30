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

    # 後続のスクリプトにタイトルを渡すために出力する
    title = get_task_title(start_response)
    print(title)
