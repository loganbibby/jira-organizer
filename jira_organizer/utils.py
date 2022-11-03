import re
from flask import g


__all__ = [
    "slugify", "get_statuses",
]


def slugify(value, repl="_"):
    value = value.lower()
    value = re.sub(r"\W+", repl, value)

    if value.endswith(repl):
        value = value[:-1]

    return value


def get_statuses():
    statuses = {}
    colors = g.conf.status_colors

    for status in g.client.get_statuses():
        key = slugify(status.name)

        statuses[status.name] = {
            "key": key,
            "color": colors.get(key, status.color_name),
            "name": status.name,
            "description": status.description
        }

        if statuses[status.name]["color"] == "blue-gray":
            statuses[status.name]["color"] = "gray"

    return statuses
