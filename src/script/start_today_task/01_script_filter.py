# "Argument Optional"を指定する
from __future__ import annotations

import os
import sys

sys.path.append(f"{os.environ['HOME']}/git/alfred_python/src/")

import json
from dataclasses import dataclass

import config

JSON_FILEPATH = f"{config.GIT_PROJECT_DIR}/start_today_task.json"


@dataclass(frozen=True)
class Task:
    task_id: str
    title: str

    def to_item(self) -> dict:
        return {
            "title": self.title,
            "arg": self.task_id,
        }


# APIからデータを取得する関数
def get_items_from_api() -> list[dict]:
    data: list[dict] = config.get_notion_api("/tasks/current")  # type: ignore
    tasks = [Task(task_id=task["id"], title=task["title"]) for task in data]
    items = [task.to_item() for task in tasks]
    save_cache_items(items)
    return items


def save_cache_items(items: list[dict]) -> None:
    result = {
        "expired_at": config.get_now().timestamp(),
        "items": items,
    }
    # resultをファイルに書き込む
    with open(JSON_FILEPATH, "w") as f:
        json.dump(result, f, ensure_ascii=False)


def read_cache_items() -> list[dict] | None:
    if not os.path.exists(JSON_FILEPATH):
        return None
    with open(JSON_FILEPATH) as f:
        data = json.load(f)
        expired_at = data["expired_at"]
        # 1分経過していない場合は、これを出力して終了
        if config.get_now().timestamp() - expired_at < 60:  # noqa: PLR2004
            return data["items"]
    return None


if __name__ == "__main__":
    # python3 -m src.script.start_today_task.01_script_filter
    search_query: str = sys.argv[1] if len(sys.argv) > 1 else ""
    items = read_cache_items() or get_items_from_api()
    items = config.filter_dict_list(items, "title", search_query)
    print(json.dumps({"items": items}))
