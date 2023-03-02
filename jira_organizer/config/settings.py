from pathlib import Path
import environ

env = environ.Env()

DATA_DIR = environ.Path(Path(__file__).parent.parent.parent.resolve())

DATA_FILE = DATA_DIR.path("data.json")

CACHE_TYPE = "FileSystemCache"
CACHE_DIR = DATA_DIR.path("cache")
CACHE_DEFAULT_TIMEOUT = 300

#
# Jira

JIRA_SUBDOMAIN = env("JIRA_SUBDOMAIN")
JIRA_USERNAME = env("JIRA_USERNAME")
JIRA_API_KEY = env("JIRA_API_KEY")

GITHUB = {
    "jira_custom_field": "customfield_10000"
}

#
# Organizer

AUTO_REFRESH = 60

ISSUE_VIEWS = {}

ISSUE_DEFAULT_DISPLAY_SETTINGS = {
    "flags": [
        "show_status",
        "show_reporter",
        "show_priority",
        "show_labels",
        "show_parent",
        "show_issue_type",
        "show_github_pr",
    ],
    "other_statuses": [
        "done"
    ],
    "priority": {
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
    },
    "status": {
        "in_progress": {
            "color": "primary",
        },
        "blocked": {
            "color": "danger",
        },
        "done": {
            "color": "success",
        },
        "reopened": {
            "color": "danger",
        },
    },
    "issue_type": {
        "bug": {
            "icon": "fas fa-bug",
            "color": "danger",
        },
        "task": {
            "icon": "fas fa-tasks",
            "color": "info",
        },
        "sub_task": {
            "icon": "fas fa-tasks",
            "color": "info",
        },
        "story": {
            "icon": "fas fa-book",
            "color": "success"
        },
    },
}
