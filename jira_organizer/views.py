from flask import g, render_template, request, jsonify
from .app import app
from .utils import *


def get_issues(view_name):
    view = g.conf.views[view_name]

    issues = g.client.do_search(jql=view.get("jql", ""))

    columns = {
        "main": [],
        "other": [],
        "hidden": [],
    }

    data = g.data.views.get(view_name, {
        "hidden": [],
        "sorted": []
    })

    sorted_ids = []

    # Move issues into other columns
    for issue in issues:
        if issue.jira_id in data["hidden"]:
            columns["hidden"].append(issue)
            sorted_ids.append(issue.jira_id)
            continue

        if slugify(issue.status) in g.conf.other_statuses:
            columns["other"].append(issue)
            sorted_ids.append(issue.jira_id)
            continue

    # Sort issues
    for issue_id in data["sorted"]:
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

    g.data.views[view_name] = data

    return columns


@app.route("/")
def index():
    view_name = request.args.get("view", g.conf.default_view)

    if view_name not in g.conf.views:
        return f"View not found: {view_name}"

    columns = get_issues(view_name)

    return render_template(
        "organizer.html",
        issue_count=len(columns["main"]) + len(columns["other"]) + len(columns["hidden"]),
        columns=columns,
        jira_subdomain=g.conf.jira_subdomain,
        statuses=get_statuses(),
        issue_display=g.conf.issue_display,
        view_name=view_name,
        view=g.conf.views[view_name]
    )


@app.route("/export")
def export_issues():
    view_name = request.args.get("view", g.conf.default_view)

    if view_name not in g.conf.views:
        return f"View not found: {view_name}"

    issues = get_issues(view_name)["main"]
    limit = int(request.args.get("limit", 5))

    return render_template(
        "export.html",
        issue_count=limit,
        issues=issues[0:limit],
        jira_subdomain=g.conf.jira_subdomain,
    )

@app.route("/api/update_order", methods=["POST"])
def update_order():
    data = request.get_json()

    g.data.views[data["view_name"]]["sorted"] = data["issues"]
    g.data.dump()

    return jsonify({
        "success": True
    })


@app.route("/api/hide/<issue_id>", methods=["POST"])
def hide_issue(issue_id):
    data = request.get_json()

    if issue_id in g.data.views[data["view_name"]]["hidden"]:
        g.data.views[data["view_name"]]["hidden"].remove(issue_id)
        g.data.dump()
        return jsonify({"hidden": False})

    g.data.views[data["view_name"]]["hidden"].append(issue_id)
    g.data.dump()
    return jsonify({"hidden": True})


@app.route("/api/statuses")
def show_statuses():
    return jsonify(get_statuses())
