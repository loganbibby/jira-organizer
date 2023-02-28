import json


__all__ = [
    "Data",
]


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


class DisplaySettings(object):
    def __init__(self, view_settings, default_settings):
        self.data = {
            "flags": [],
            "other_statuses": [],
            "issue_id": {
                "_": {
                    "singular_name": "Issue ID",
                    "plural_name": "Issue IDs",
                    "show_in_small": True,
                }
            },
            "assignee": {
                "_": {
                    "singular_name": "Current Assignee",
                    "icon": "fas fa-user-ninja",
                },
            },
            "project": {
                "_": {
                    "singular_name": "Project",
                    "plural_name": "Projects",
                    "icon": "fas fa-bookmark"
                },
            },
            "version": {
                "_": {
                    "singular_name": "Version",
                    "plural_name": "Versions",
                    "icon": "fas fa-code-branch"
                },
            },
            "parent": {
                "_": {
                    "singular_name": "Parent",
                    "plural_name": "Parents",
                    "icon": "fas fa-sitemap"
                },
            },
            "labels": {
                "_": {
                    "singular_name": "Labels",
                    "icon": "fas fa-tags"
                },
            },
            "reporter": {
                "_": {
                    "singular_name": "Reporter",
                    "plural_name": "Reporters",
                    "icon": "fas fa-user",
                }
            },
            "status": {
                "_": {
                    "singular_name": "Status",
                    "plural_name": "Statuses",
                    "show_in_small": True,
                    "icon": "far fa-bell",
                }
            },
            "priority": {
                "_": {
                    "singular_name": "Priority",
                    "plural_name": "Priorities",
                    "icon": "fas fa-exclamation-triangle"
                }
            },
            "issue_type": {
                "_": {
                    "singular_name": "Issue Type",
                    "plural_name": "Issue Types",
                    "icon": "fas fa-dot-circle",
                    "show_in_small": True,
                },
            },
        }

        def update_data(settings):
            for key, value in settings.items():
                if key not in self.data or not isinstance(value, dict):
                    self.data[key] = value
                    continue

                for child_key, child_value in value.items():
                    if child_key not in self.data[key]:
                        self.data[key][child_key] = child_value
                        continue

                    self.data[key][child_key].update(child_value)

        update_data(default_settings)
        update_data(view_settings)

    def has_flag(self, flag):
        return flag in self.data["flags"]

    def show_in_other(self, slug):
        return slug in self.data["other_statuses"]

    def get_type_settings(self, type_name):
        return self.data.get(type_name, {})

    def get_type_default_settings(self, type_name):
        return self.get_type_settings(type_name).get("_", {})

    def get_type_default_setting(self, type_name, key, default=None):
        return self.get_type_default_settings(type_name).get(key, default)

    def get_name(self, type_name):
        return self.get_type_default_setting(type_name, "singular_name")

    def get_plural_name(self, type_name):
        return self.get_type_default_setting(
            type_name, "plural_name",
            self.get_name(type_name)
        )

    def get_settings_for_slug(self, type_name, slug):
        return self.get_type_settings(type_name).get(slug, {})

    def get_color(self, type_name, slug):
        return self.get_settings_for_slug(type_name, slug).get(
            "color",
            self.get_type_default_setting(type_name, "color")
        )

    def get_icon(self, type_name, slug):
        return self.get_settings_for_slug(type_name, slug).get(
            "icon",
            self.get_type_default_setting(type_name, "icon")
        )

    def show_in_small(self, type_name):
        return self.get_type_default_setting(type_name, "show_in_small", False)

    def show_type(self, type_name):
        return type_name == "issue_id" or self.has_flag(f"show_{type_name}")
