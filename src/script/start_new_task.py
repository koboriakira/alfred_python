from datetime import timedelta
import os
import sys
from pathlib import Path
import re

sys.path.append(f"{os.environ['HOME']}/git/alfred_python/src/")

import config

def append_to_obsidian_daily_note(query: str) -> None:
    """
    Append the query text to the end of today's Obsidian daily note.
    If the file doesn't exist, this function silently does nothing.

    Args:
        query: The text to append to the daily note
    """
    today = config.get_today().strftime("%Y-%m-%d")
    obsidian_dir = os.environ.get("OBSIDIAN_DIR")

    if not obsidian_dir:
        return  # OBSIDIAN_DIR environment variable not set

    daily_note_path = Path(f"{obsidian_dir}/my-vault/dailynote/{today}.md")

    # Skip if the file doesn't exist
    if not daily_note_path.exists():
        return

    # Check if the last line is empty
    with open(daily_note_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Determine if we need to add a newline before the content
    if content and not content.endswith('\n'):
        prefix = '\n'
    elif content and re.search(r'\n$', content):
        # Last line is empty (ends with newline)
        prefix = ''
    else:
        # Empty file
        prefix = ''

    # Append the query to the end of the file
    with open(daily_note_path, "a", encoding="utf-8") as file:
        file.write(f"{prefix}- [ ] {query}\n")

if __name__ == "__main__":
    start = config.get_now()
    end = start + timedelta(minutes=25)
    query = sys.argv[1] if len(sys.argv) > 1 else "新しいタスク"
    # body = {
    #     "title": query,
    #     "start_date": start.isoformat(),
    #     "end_date": end.isoformat(),
    #     "status": "InProgress",
    # }
    # config.post_notion_api("/task/", body)

    # Add the query to the Obsidian daily note
    append_to_obsidian_daily_note(query)
