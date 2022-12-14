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

ISSUE_VIEWS = {}

ISSUE_DEFAULT_DISPLAY_FLAGS = [
    "show_status",
    "show_reporter",
    "show_priority"
]

ISSUE_DEFAULT_OTHER_STATUSES = []

#
# Display

ISSUE_DEFAULT_STATUS_COLORS = {}

ISSUE_DEFAULT_PRIORITY_COLORS = {
    "high": "danger",
    "very_high": "danger",
    "medium": "warning",
    "low": "primary",
    "lowest": "primary",
}
