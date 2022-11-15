from flask import g, request, jsonify, render_template
from .app import app
from .utils import *


def get_issue_cache_key(view_name):
    return f"issues_view_{view_name}"


def _get_issues(view_name, force=False):
    view = app.config["ISSUE_VIEWS"][view_name]

    issues = g.cache.get(get_issue_cache_key(view_name))

    if not issues or force:
        issues = g.client.do_search(jql=view.get("jql", ""))
        g.cache.set(get_issue_cache_key(view_name), issues)

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

        if slugify(issue.status) in app.config["ISSUE_DEFAULT_OTHER_STATUSES"]:
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
    new_issues = []

    for issue in issues:
        if issue.jira_id in sorted_ids:
            continue

        issue.is_new = True
        new_issues.append(issue)

    columns["main"] = new_issues + columns["main"]

    g.data.views[view_name] = data

    return {
        "issues": columns,
        "total_count": len(issues)
    }


@app.route("/")
def index():
    view_name = request.args.get("view", app.config["ISSUE_DEFAULT_VIEW"])

    return render_template(
        "organizer.html",
        view_name=view_name,
        view=app.config["ISSUE_VIEWS"][view_name]
    )


@app.route("/export")
def export_issues():
    view_name = request.args.get("view", app.config["ISSUE_DEFAULT_VIEW"])

    if view_name not in app.config["ISSUE_VIEWS"]:
        return f"View not found: {view_name}"

    limit = int(request.args.get("limit", 5))

    return render_template(
        "export.html",
        view_name=view_name,
        limit=limit
    )


@app.route("/api/issues/invalidate")
def invalidate_issues_cache():
    view_name = request.args.get("view")

    if not view_name:
        return jsonify({
            "error": "view_not_found",
            "msg": "Must pass view"
        }), 401

    g.cache.set(get_issue_cache_key(view_name), None)

    return jsonify({
        "success": True,
        "view": view_name
    })


@app.route("/api/issues")
def get_issues():
    view_name = request.args.get("view", app.config["ISSUE_DEFAULT_VIEW"])
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 0))
    column = request.args.get("column", "main")
    ret_format = request.args.get("format", "json")

    view = app.config["ISSUE_VIEWS"].get(view_name)

    if not view:
        return jsonify({
            "error": "view_not_found",
            "msg": f"View '{view_name}' not found"
        }), 404

    if "limit" in view and not limit:
        limit = view["limit"]

    data = _get_issues(view_name)

    if column not in data["issues"]:
        return jsonify({
            "error": "column_not_found",
            "msg": f"Column '{column}' not found in view '{view_name}'"
        }), 404

    issues = data["issues"][column]

    total = len(issues)

    if limit:
        issues = issues[offset:limit]

    if ret_format == "json":
        results = [i.to_dict() for i in issues]
    elif ret_format == "html":
        results = [
            render_template(
                "partials/issue.html",
                issue=issue,
                sm=False if column == "main" else True,
                hidden=False if column != "hidden" else True,
                **view
            ) for issue in issues
        ]
    else:
        return jsonify({
            "error": "invalid_format",
            "msg": f"Format '{ret_format}' is invalid; must be json or html"
        }), 404

    return jsonify({
        "view": view_name,
        "column": column,
        "limit": limit,
        "offset": offset,
        "total": total,
        "count": len(issues),
        "results": results
    })


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
