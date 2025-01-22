import os

DB_DEFAULT_FILENAME = "tapedata.sqlite"
ATTACHMENT_DEFAULT_DIR = "attachments"


def is_debug_mode():
    return os.environ.get("TAPEAGENTS_DEBUG", None) == "1"


def sqlite_db_path():
    return os.environ.get("TAPEAGENTS_SQLITE_DB", DB_DEFAULT_FILENAME)
