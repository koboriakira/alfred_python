# FIXME: Slack上に作成されたテンプレートをダウンロードして自動で設置、開きたい

import os
import sys

sys.path.append(f"{os.environ['HOME']}/git/alfred_python/src/")

import config

today = config.get_today()

BLOG_TEMPLATE = f"""---
title:
date: {today.strftime('%Y-%m-%d')}
tags: []
---


"""


blog_filepath = f"{config.BLOG_DIR}/content/{today.strftime('%Y/%m/%d')}.md"

# ファイルがない場合は作成
if not os.path.exists(blog_filepath):
    os.makedirs(os.path.dirname(blog_filepath), exist_ok=True)
    with open(blog_filepath, "w") as f:
        f.write(BLOG_TEMPLATE)

# VSCodeを開く
config.run_process(["code", blog_filepath], check=False)
