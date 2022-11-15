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
