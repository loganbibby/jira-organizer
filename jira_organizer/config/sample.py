from .base import *


DEBUG = env.bool(
    "DEBUG",
    False
)

#
# Jira

JIRA_SUBDOMAIN = env("JIRA_SUBDOMAIN")
JIRA_USERNAME = env("JIRA_USERNAME")
JIRA_API_KEY = env("JIRA_API_KEY")

GITHUB = env.json(
    "GITHUB",
    "{'jira_custom_field': 'customfield_10000'}"
)

#
# Organizer

AUTO_REFRESH = env.int(
    "AUTO_REFRESH",
    60
)

ISSUE_VIEWS = env.json(
    "ISSUE_VIEWS",
    "{}"
)

ISSUE_DEFAULT_DISPLAY_SETTINGS = env.json("ISSUE_DEFAULT_DISPLAY_SETTINGS", "")

if ISSUE_DEFAULT_DISPLAY_SETTINGS is "":
    ISSUE_DEFAULT_DISPLAY_SETTINGS = {
        "flags": env("DISPLAY_FlAGS", "").split(","),
        "other_statuses": env("OTHER_STATUSES", "").split(","),
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
