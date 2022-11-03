# Jira Organizer

Simple drag-and-drop organizer for Jira issues.

## Installation

Note: it's recommended to use a Python virtual environment. (`python -m venv .venv`)

1. Clone this repo.
2. Install required libraries with `pip install -r requirements.txt`.
3. Copy `data/sample-config.json` to `data/config.json` and update.
4. Run with `flask --app jira_organizer:app run`
5. Access from <http://localhost:5000>.

## Configuration

All configuration is stored as JSON in `data/config.json`.

_If you change any configuration, make sure you restart the server._

### `jira_subdomain`

The subdomain of your organizations Jira site.

For example `acmeinc` is the subdomain for `https://acmeinc.atlassian.net/`.

### `jira_username`

Your Atlassian account username -- usually your e-mail.

### `jira_api_key`

A Personal Access Token (PAT) created from [here](https://id.atlassian.com/manage-profile/security/api-tokens).

### `issue_jql`

By default, issues shows are assigned to the active user and exclude `Done` and `Deferred` statuses. 

You can define your own JQL for the search with this option. 

### `status_colors`

Dictionary of colors for each status where the key is sluggified status name and the value is the color. 

(To view sluggified status names, go to `/api/statuses` and look at the `key`.)

### `other_statuses`

List of sluggified status names to be shown in the Other column.

### `issue_display`

Dictionary of display flags where the key is an option from below and the value is a boolean.

 * `show_status`: Shows the issue's status
 * `show_reporter`: Shows the name of the report (only on the main column)
 * `show_project`: Shows the project name (only on the main column)
 * `show_assignee`: Shows the assignee name (only on the main column)

## To Do

 * Caching
 * Add note to issue
 * ~~Move issue to top/bottom~~
 * ~~Export issues (for pasting into Slack)~~
 * Expanded view modal

## Release History
 
 * `0.3` - Added ability to hide issues; fixed issue with `Data` object
 * `0.2` - Added export view and ability to move issue to top/bottom
 * `0.1` - Initial release
