from datetime import timedelta
import os
import sys

sys.path.append(f"{os.environ['HOME']}/git/alfred_python/src/")

import config

if __name__ == "__main__":
    start = config.get_now()
    end = start + timedelta(minutes=25)
    query = sys.argv[1] if len(sys.argv) > 1 else "新しいタスク"
    body = {
        "title": query,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "status": "InProgress",
    }
    config.post_notion_api("/task/", body)
