import json


__all__ = [
    "Config", "Data",
]


class Config(object):
    views = {}
    default_view = "default"
    status_colors = {}
    priority_colors = {
        "high": "danger",
        "very_high": "danger",
        "medium": "warning",
        "low": "primary",
        "lowest": "primary",
    }
    other_statuses = []
    issue_display = []

    def __init__(self, filename):
        with open(filename, "r+", encoding="utf-8") as fh:
            for key, value in json.load(fh).items():
                setattr(self, key, value)

        if "default" not in self.views:
            self.views["default"] = {
                "title": "My Open Issues",
                "jql": "assignee = currentUser() AND status not in (Done, Deferred)"
            }

        self.jira_url = f"https://{self.jira_subdomain}.atlassian.net/rest/api"


class Data(object):
    def __init__(self, filename):
        self.filename = filename

        self.views = {}

        self.load()

    def load(self):
        with open(self.filename, "r+", encoding="utf-8") as fh:
            for key, value in json.load(fh).items():
                setattr(self, key, value)

            for view_name in self.views.keys():
                for key in ["hidden", "sorted"]:
                    if key in self.views[view_name]:
                        continue

                    self.views[view_name][key] = []

    def dump(self):
        payload = self.__dict__.copy()
        print(payload)
        del payload["filename"]

        with open(self.filename, "w+", encoding="utf-8") as fh:
            json.dump(payload, fh)
