from flask import g, render_template, request, jsonify
from .app import app
from .utils import *


def get_issues():
    jql = ""

    if hasattr(g.conf, "issue_jql"):
        jql = g.conf.issue_jql

    issues = g.client.do_search(jql=jql)

    columns = {
        "main": [],
        "other": [],
    }

    sorted_ids = []

    # Move issues into other column
    for issue in issues:
        if slugify(issue.status) not in g.conf.other_statuses:
            continue

        columns["other"].append(issue)
        sorted_ids.append(issue.jira_id)

    # Sort issues
    for issue_id in g.data.issues_sorted:
        if issue_id in sorted_ids:
            continue

        for issue in issues:
            if issue.jira_id != issue_id:
                continue

            columns["main"].append(issue)
            sorted_ids.append(issue_id)
            break

    # Add the rest
    for issue in issues:
        if issue.jira_id in sorted_ids:
            continue

        columns["main"].append(issue)

    return columns


@app.route("/")
def index():
    columns = get_issues()

    return render_template(
        "organizer.html",
        issue_count=len(columns["main"]) + len(columns["other"]),
        columns=columns,
        jira_subdomain=g.conf.jira_subdomain,
        statuses=get_statuses(),
        issue_display=g.conf.issue_display
    )


@app.route("/export")
def export_issues():
    issues = get_issues()["main"]
    limit = int(request.args.get("limit", 5))

    return render_template(
        "export.html",
        issue_count=limit,
        issues=issues[0:limit],
        jira_subdomain=g.conf.jira_subdomain,
    )

@app.route("/api/update_order", methods=["POST"])
def update_order():
    g.data.issues_sorted = request.get_json()["issues"]
    g.data.dump()

    return jsonify({
        "success": True,
        "issues": g.data.issues_sorted
    })


@app.route("/api/statuses")
def show_statuses():
    return jsonify(get_statuses())
