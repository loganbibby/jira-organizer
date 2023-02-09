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


class ComponentDisplay(object):
    def __init__(self, slug, display, show_in_main=True, color=None, icon=None):
        self.display = display
        self.slug = slug
        self.show_in_main = show_in_main
        self.options = {}
        self.defaults = {
            "color": color,
            "icon": icon
        }

    def __call__(self, slug):
        if slug in self.options:
            return self.options[slug]

        return self.set(slug)

    def set(self, slug, override=True, **options):
        for key, value in self.defaults.items():
            if key not in options:
                options[key] = value

        if not override and slug in self.options:
            return self.options[slug]

        self.options[slug] = options

        return self.options[slug]

    def build_options(self, view, defaults):
        for key, options in view.get(self.slug, {}).items():
            self.set(key, **options)

        for key, options in defaults.get(self.slug, {}).items():
            self.set(key, override=False, **options)


class DisplaySettings(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        defaults = (
            ("flags", []),
            ("other_statuses", []),
        )

        for key, default in defaults:
            if key not in self:
                self[key] = default

    def add_component(self, component):
        self[component.slug] = component

    def add_flag(self, flag):
        self["flags"].append(flag)

    def add_other_status(self, slug):
        self["other_statuses"].append(slug)
