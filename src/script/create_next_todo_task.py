import os
import sys

sys.path.append(f"{os.environ['HOME']}/git/alfred_python/src/")
import config

if __name__ == "__main__":
    # python src/script/create_next_todo_task.py "テスト"
    body = {
        "title": sys.argv[1],
        "task_kind": "次にとるべき行動リスト",
        "start_date": config.get_now().date().isoformat(),
    }

    response = config.post_notion_api("/task/", body)
