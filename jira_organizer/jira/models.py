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
            if data_field not in data:
                continue

            setattr(self, obj_attr, data[data_field])

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

    def update(self, payload=None):
        super().update(payload)

        self.fix_versions = [d["name"] for d in self.fix_versions]

        if hasattr(self, "parent"):
            self.parent = NestedJiraIssue(self.parent)


class JiraStatus(JiraObject):
    field_mapping = {
        "jira_id": "id",
        "name": "name",
        "description": "description",
        "color_name": "statusCategory.colorName"
    }
