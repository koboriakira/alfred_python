import os
import sys

sys.path.append(f"{os.environ['HOME']}/git/alfred_python/src/")

import config

if __name__ == "__main__":
    query = sys.argv[1]
    body = {
        "task_name": query,
    }
    config.post_notion_api("/tasks/new", body)
