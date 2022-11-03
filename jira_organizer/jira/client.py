import requests
from requests.auth import HTTPBasicAuth
from .models import *


class JiraClient(object):
    def __init__(self, url, username, api_key, **kwargs):
        self.url = url
        self.auth = HTTPBasicAuth(
            username,
            api_key
        )
        self.extra_kwargs = kwargs

    def execute(self, method, url, **kwargs):
        request_kwargs = self.extra_kwargs.copy()
        request_kwargs.update(kwargs)

        if "auth" not in request_kwargs:
            request_kwargs["auth"] = self.auth

        self.last_response = getattr(requests, method)(
            self.url + url,
            **request_kwargs
        )

        if not self.last_response.ok:
            self.last_response.raise_for_status()

        return self.last_response.json()

    def do_search(self, jql=None):
        issues = []

        while True:
            r = self.execute(
                "get",
                "/2/search",
                params={
                    "jql": jql
                }
            )

            issues += [JiraIssue(issue) for issue in r["issues"]]

            if len(issues) <= r["total"]:
                break

        return issues

    def get_statuses(self):
        r = self.execute(
            "get",
            "/2/status"
        )

        return [JiraStatus(status) for status in r]
