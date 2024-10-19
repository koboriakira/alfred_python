import os
import sys

sys.path.append(f"{os.environ['HOME']}/git/alfred_python/src/")
import config


def unpack_price() -> int:
    packed_values = sys.argv[1].split(",")
    price = packed_values[0]
    if not price.isnumeric():
        raise ValueError("price must be numeric")
    return int(price)


def unpack_title() -> str:
    packed_values = sys.argv[1].split(",")
    title = packed_values[1] if len(packed_values) == 2 else ""
    return title


if __name__ == "__main__":
    # /usr/bin/python3 src/script/add_account_book.py "100,テスト"
    body = {
        "title": unpack_title(),
        "price": unpack_price(),
    }
    config.post_notion_api("/account_book/", body)
