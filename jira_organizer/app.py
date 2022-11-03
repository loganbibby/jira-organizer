from pathlib import Path
from flask import Flask, g
from .options import Config, Data
from .jira.client import JiraClient


app = Flask(__name__)


@app.before_request
def init_request():
    data_dir = Path(__file__).parent.parent.resolve() / "data"

    g.conf = Config(data_dir / "config.json")
    g.data = Data(data_dir / "data.json")
    g.client = JiraClient(
        url=g.conf.jira_url,
        username=g.conf.jira_username,
        api_key=g.conf.jira_api_key
    )


from . import views
