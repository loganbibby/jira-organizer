from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.resolve() / "data"

CONFIG_FILE = DATA_DIR / "config.json"
DATA_FILE = DATA_DIR / "data.json"

CACHE_TYPE = "FileSystemCache"
CACHE_DIR = DATA_DIR / "cache"
CACHE_DEFAULT_TIMEOUT = 300

DEBUG = False

#
# Jira

JIRA_SUBDOMAIN = "your-subdomain"
JIRA_USERNAME = "your-username"
JIRA_API_KEY = "your-api-key"

#
# Organizer

AUTO_REFRESH = 60

ISSUE_VIEWS = {}

ISSUE_DEFAULT_DISPLAY_SETTINGS = {
    "flags": [
        "show_status",
        "show_reporter",
        "show_priority"
    ],
    "other_statuses": [],
    "priorities": {
        "high": {
            "color": "danger",
        },
        "very_high": {
            "color": "danger",
        },
        "medium": {
            "color": "warning",
        },
        "low": {
            "color": "primary",
        },
        "lowest": {
            "color": "primary",
        },
    }
}

