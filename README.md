# Jira Organizer

Simple drag-and-drop organizer for Jira issues.

![Screenshot](docs/screenshot.png)

## Installation

Note: it's recommended to use a Python virtual environment. (`python -m venv .venv`)

1. Clone this repo.
2. Install required libraries with `pip install -r requirements.txt`.
3. Copy `jira_organizer/config-sample.py` to `jira_organizer/config.py` and update.
4. Run with `flask --app jira_organizer:app run`
5. Access from <http://localhost:5000>.

## Configuration

Configuration is done through a Python module or environment variables. 

The Python module can be set by `CONFIG_MODULE` and defaults to `jira_organizer.config.config`. (Any config modules should include `from config.base import *`.)

Environment variables are the same as their names below. `dict` or `list` configurations are processed as JSON. 

Other environment variables available:
 * `DATA_DIR`: directory for data to be stored (defaults to `./data`)
 * `DATA_FILE`: data storage file (defaults to `data.json`)
 * `CACHE_DIR`: directory for the cache data (defaults to `./data/cache`)
 * `CACHE_TIMEOUT`: TTL for cache (defaults to `300` seconds)

### `AUTO_REFRESH`

Number of seconds between auto refresh. Set to `0` to disable.

Defaults to `60`.

### `JIRA_SUBDOMAIN`

The subdomain of your organizations Jira site.

For example `acmeinc` is the subdomain for `https://acmeinc.atlassian.net/`.

### `JIRA_USERNAME`

Your Atlassian account username -- usually your e-mail.

### `JIRA_API_KEY`

A Personal Access Token (PAT) created from [here](https://id.atlassian.com/manage-profile/security/api-tokens).

### `JIRA_URL`

API endpoint for Jira. Automatically set if not defined. 

### `GITHUB`

Settings for GitHub integration.

 * `jira_custom_field`: Name of the custom field for GitHub integration

### `ISSUE_DEFAULT_DISPLAY_SETTINGS`

These settings are the defaults for how the organizer displays issues. This same dictionary format is used for defining a view's `display` settings.

See Display Settings.

### `ISSUE_VIEWS`

Dictionary of views where the key is the name of the view (no spaces) and the value is a dictionary of the options below.

 * `jql`: JQL for the view
 * `title`: Title to be shown
 * `display`: See Display Settings
 * `allow_sorting`: Allows for sorting of issues (defaults to `True`)

If no default view is specified, a view will be added for open issues of the current user.

### `ISSUE_DEFAULT_VIEW`

Name of the default view.

Defaults to `default`.

## Issue Metadata

For each issue, the following metadata is extracted:
 * `status`: Status
 * `issue_type`: Issue type
 * `github`: GitHub pull request and build statuses
 * `reporter`: Name of the reporter
 * `project`: Project name
 * `assignee`: Name of the assignee
 * `priority`: Priority
 * `labels`: Comma separated list of labels
 * `parent`: Parent Jira information

## Display Settings

#### `flags`

List of flags for displaying components in the issue. Right now, these dictate the metadata shown in the issue template with the `show_<metadata>` flags.

#### `other_statuses`

List of sluggified status names to be shown in the Other column.

### Metadata

The following are available metadata from the Jira issue. Each item has its own key and can be independently configured. 

The keys in the item's configuration is the sluggified value. The following keys are allowed:
* `color`: Bootstrap color class
* `icon`: Font Awesome 5 Free icon class

There are two special keys:

`_` for item configuration and defaults:
 * `singular_name`: Display name in singular form
 * `plural_name`: Display name in plural form (defaults to `singular_name`)
 * `color`: Bootstrap color class
 * `icon`: Font Awesome 5 Free icon class
 * `show_in_small`: Show in the hidden and other columns

`_displays` for overriding the displays with the key is the value as it comes from Jira and the value is the overridden display.

## To Do

 * ~~Caching~~
 * ~~Move issue to top/bottom~~
 * ~~Export issues (for pasting into Slack)~~
 * Expanded view modal
 * ~~Expand display configuration~~
 * Dockerize

## Release History

* `0.8` - Refactor of display settings and display; UI tweaks
* `0.7` - Added new component displays; refactored display settings; minor UI tweaks
* `0.6` - Added auto refresh
* `0.5` - Added caching; refactored main view to use APIs
* `0.4` - Added multiple views; various cosmetic changes
* `0.3` - Added ability to hide issues; fixed issue with `Data` object; added priority display
* `0.2` - Added export view and ability to move issue to top/bottom
* `0.1` - Initial release
