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

        return data


class JiraIssue(JiraObject):
    field_mapping = {
        "jira_id": "id",
        "id": "key",
        "priority": "priority.name",
        "summary": "fields.summary",
        "status": "fields.status.name",
        "reporter": "fields.reporter.displayName",
        "issue_type": "fields.issuetype.name",
        "project": "fields.project.name",
        "assignee": "fields.assignee.displayName",
    }


class JiraStatus(JiraObject):
    field_mapping = {
        "jira_id": "id",
        "name": "name",
        "description": "description",
        "color_name": "statusCategory.colorName"
    }
