# 指示書

Alfredのワークフロー内で利用されるPythonスクリプトを作成するための指示書です。

## 全体的な指示

- やりとりは日本語で行います

## 開発について

開発物は`src/script`に作成してください。
複数のスクリプトを利用してワークフローが動く場合は、ディレクトリを作成し、その中に連番(`01_foo.py`, `02_bar.py`)でスクリプトを作成してください。

## テンプレート

下記のコードをテンプレートとして、必要な処理を追記してください。

```python
import os
import sys

sys.path.append(f"{os.environ['HOME']}/git/alfred_python/src/")
from slack_sdk import WebClient

import config

if __name__ == "__main__":
    query = sys.argv[1]
    # 任意の記述
```
