import os
from re import sub
import sys

sys.path.append(f"{os.environ['HOME']}/git/alfred_python/src/")

import config

if __name__ == "__main__":
    text = sys.argv[1]

    # Slackのinboxチャンネルに投稿
    # config.post_to_inbox(text)

    # obsidianのinboxに追記
    config.create_obsidian_markdown(
        title=text, content="", subdir="00_Inbox"
    )
