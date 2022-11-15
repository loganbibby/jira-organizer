from flask import Flask, g
from flask_caching import Cache
from .options import Data
from .jira.client import JiraClient


app = Flask(__name__)

##
### Config

app.config.from_object("jira_organizer.config")

app.config["JIRA_URL"] = app.config.get(
    "JIRA_URL",
    f"https://{app.config['JIRA_SUBDOMAIN']}.atlassian.net/rest/api"
)

app.config["ISSUE_DEFAULT_VIEW"] = app.config.get("ISSUE_DEFAULT_VIEW", "default")

if app.config["ISSUE_DEFAULT_VIEW"] not in app.config["ISSUE_VIEWS"]:
    app.config["ISSUE_VIEWS"][app.config["ISSUE_DEFAULT_VIEW"]] = {
        "title": "My Open Issues",
        "jql": "assignee = currentUser() AND status not in (Done, Deferred)"
    }

for view_name in list(app.config["ISSUE_VIEWS"].keys()):
    view = app.config["ISSUE_VIEWS"][view_name]

    for key in ["display_flags", "other_statuses", "status_colors", "priority_colors"]:
        if key not in view:
            view[key] = app.config[f"ISSUE_DEFAULT_{key.upper()}"]

    app.config["ISSUE_VIEWS"][view_name] = view

###
##


@app.before_request
def init_request():
    g.cache = Cache(app)
    g.data = Data(app.config["DATA_FILE"])
    g.client = JiraClient(
        url=app.config["JIRA_URL"],
        username=app.config["JIRA_USERNAME"],
        api_key=app.config["JIRA_API_KEY"]
    )


from . import views
