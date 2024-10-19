# "with input as {query}"を指定すること
import os
import sys

sys.path.append(f"{os.environ['HOME']}/git/alfred_python/src/")
import config

if __name__ == "__main__":
    absolute_path = "{query}"

    # # VSCodeを開く
    config.run_process(["code", absolute_path], check=False)
