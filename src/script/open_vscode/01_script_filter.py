# "Argument Optional"を指定する
import os
import sys

sys.path.append(f"{os.environ['HOME']}/git/alfred_python/src/")
import json
import sys
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path


@dataclass(frozen=True)
class ProjectDir:
    name: str  # プロジェクト名
    absolute_path: str  # プロジェクトの絶対パス

    def to_item(self) -> dict:
        return {
            "title": self.name,
            "arg": self.absolute_path,
        }


# APIからデータを取得する関数
def fetch_dev_dir_projects(search_query) -> list[ProjectDir]:
    # 指定ディレクトリ内のディレクトリ名一覧を取得
    projects = []
    for dir in ["Dev", "git"]:
        try:
            dev_dir = Path.home() / dir
            projects += [p for p in dev_dir.iterdir() if p.is_dir()]
        except FileNotFoundError:
            pass
    # 検索クエリがある場合はフィルタリング
    if search_query:
        projects = [p for p in projects if search_query in p.name]
        # projectsが複数ある場合は、類似度が高い順にソート
        projects.sort(
            key=lambda p: SequenceMatcher(None, search_query, p.name).ratio(),
            reverse=True,
        )
    return [ProjectDir(name=p.name, absolute_path=str(p)) for p in projects]


# メインの処理


def main() -> None:
    # search_query = "{query}"
    search_query = sys.argv[1] if len(sys.argv) > 1 else None

    # APIからデータを取得
    project_dirs = fetch_dev_dir_projects(search_query)

    # データがNoneでない場合は処理を続行
    if project_dirs:
        items = [p.to_item() for p in project_dirs]
        # JSONで出力
        print(json.dumps({"items": items}))


if __name__ == "__main__":
    main()
