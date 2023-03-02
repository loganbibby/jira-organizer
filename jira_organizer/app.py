import os

from flask import Flask, g
from flask_caching import Cache

from .options import Data, DisplaySettings
from .jira.client import JiraClient


app = Flask(__name__)

##
### Config

app.config.from_object(os.environ.get("CONFIG_MODULE", default="jira_organizer.config.config"))

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

    view["display"] = DisplaySettings(
        view.get("display", {}),
        app.config["ISSUE_DEFAULT_DISPLAY_SETTINGS"]
    )

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
