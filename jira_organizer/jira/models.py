import re

from ..utils import slugify


__all__ = [
    "JiraIssue", "JiraStatus",
]


class JiraObject(object):
    field_mapping = {}

    def __init__(self, data):
        self.update(data)

    def update(self, payload=None):
        if payload:
            self._raw_data = payload

        data = {}

        def do_dotted(child, parent_key=None):
            for key, value in child.items():
                if parent_key:
                    child_key = f"{parent_key}.{key}"
                else:
                    child_key = key

                if isinstance(value, dict):
                    do_dotted(value, parent_key=child_key)
                else:
                    data[child_key] = value

        do_dotted(self._raw_data)

        for obj_attr, data_field in self.field_mapping.items():
            value = None

            if not data_field:
                key_method = f"get_{obj_attr}_key"
                data_method = f"get_{obj_attr}_data"

                if hasattr(self, key_method):
                    data_field = getattr(self, key_method)()
                elif hasattr(self, data_method):
                    value = getattr(self, data_method)(data)

            if not value and data_field not in data:
                continue

            if not value:
                value = data[data_field]

            update_method = f"update_{obj_attr}"

            if hasattr(self, update_method):
                value = getattr(self, update_method)(value)

            setattr(self, obj_attr, value)

    def to_dict(self):
        data = self.__dict__.copy()

        for key in ["field_mapping", "_raw_data"]:
            if key not in data:
                continue

            del data[key]

        for key in data.keys():
            if not isinstance(data[key], JiraObject):
                continue

            data[key] = data[key].to_dict()

        return data


class NestedJiraIssue(JiraObject):
    field_mapping = {
        "jira_id": "id",
        "id": "key",
        "priority": "fields.priority.name",
        "summary": "fields.summary",
        "status": "fields.status.name",
        "issue_type": "fields.issuetype.name",
    }


class JiraIssue(JiraObject):
    field_mapping = {
        "jira_id": "id",
        "id": "key",
        "priority": "fields.priority.name",
        "summary": "fields.summary",
        "status": "fields.status.name",
        "reporter": "fields.reporter.displayName",
        "issue_type": "fields.issuetype.name",
        "project": "fields.project.name",
        "assignee": "fields.assignee.displayName",
        "fix_versions": "fields.fixVersions",
        "labels": "fields.labels",
        "parent": "fields.parent",
        "github": None,
    }

    @property
    def status_slug(self):
        return slugify(self.status)

    @property
    def priority_slug(self):
        return slugify(self.priority)

    @property
    def issue_type_slug(self):
        return slugify(self.issue_type)

    def get_slug(self, type):
        slug_property = f"{type}_slug"
        if hasattr(self, slug_property):
            return getattr(self, slug_property)

    def should_display(self, key):
        return hasattr(self, key) and getattr(self, key) is not None

    def get_display(self, key):
        if not hasattr(self, key):
            return "<Not Available>"

        value = getattr(self, key)

        if isinstance(value, list):
            return ", ".join(value)

        if isinstance(value, dict) and "summary" in value:
            return value["summary"]

        return str(value)

    def update_fix_versions(self, value):
        return [d["name"] for d in value]

    def update_parent(self, value):
        return NestedJiraIssue(value)

    def get_github_key(self):
        from ..app import app
        github_config = app.config.get("GITHUB")
        if not github_config or "jira_custom_field" not in github_config:
            return None
        return f"fields.{github_config['jira_custom_field']}"

    def update_github(self, value):
        data = {
            "pull_request": None,
            "build": None
        }

        pr = re.search(r"pullrequest={([\w\d=, ]+)}", value)
        build = re.search(r"build={([\w\d=, ]+)}", value)

        def process_github_data(github_data):
            items = {}

            for item in github_data.split(", "):
                item_child = item.split("=")
                item_value = item_child[1]

                try:
                    item_value = int(item_value)
                except ValueError:
                    item_value = item_value

                items[item_child[0]] = item_value

            return items

        if pr:
            data["pull_request"] = process_github_data(pr.group(1))

        if build:
            data["build"] = process_github_data(build.group(1))

        return data


class JiraStatus(JiraObject):
    field_mapping = {
        "jira_id": "id",
        "name": "name",
        "description": "description",
        "color_name": "statusCategory.colorName"
    }
