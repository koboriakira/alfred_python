# "with input as {query}"を指定すること

import os
import sys

sys.path.append(f"{os.environ['HOME']}/git/alfred_python/src/")
import config

if __name__ == "__main__":
    task_id = "{query}"
    path = "/task/start/" + task_id
    config.post_slack_concierge_api(path)
