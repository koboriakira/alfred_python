from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    """
    AlfredのItemオブジェクトを生成するためのクラス
    これを出力するとAlfredの選択肢が表示される
    """

    title: str
    arg: str

    def __dict__(self) -> dict:
        return {
            "title": self.title,
            "arg": self.arg,
        }
