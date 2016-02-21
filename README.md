# subreddit-settings
A GitHub/reddit bot that automagically updates subreddit style and sidebar after GitHub commits.

## Required python packages:

Before using the bot, you will need to install the following packages (`pip install <package>`):
* `praw` - official reddit API python package
* `requests` - http requests made easy
* `gitpython` - interact with the GitHub API

## Configuring bot:

In order for your bot to function, you should create a file named `configure.json` in your local repository directory that contains the following:

```json
{
  "reddit_user": "BOT_USERNAME",
  "reddit_pass": "BOT_PASSWORD",
  "subreddit": "SUBREDDIT",
  "about_bot": "a simple statement telling reddit what your bot does",
  "github_owner": "YOUR_GITHUB_NAME",
  "github_repo": "FORKED_REPO_NAME",
  "stylesheet": "stylesheet.css",
  "sidebar": "sidebar.txt",
  "sleep_secs": 120
}
```

For example, your `configure.json` file might look like this:

```json
{
  "reddit_user": "me_on_reddit",
  "reddit_pass": "mypassword",
  "subreddit": "mysubreddit",
  "about_bot": "/r/mysubreddit subreddit updater by /u/me_on_reddit",
  "github_owner": "micro-machine",
  "github_repo": "subreddit-settings",
  "stylesheet": "stylesheet.css",
  "sidebar": "sidebar.txt",
  "sleep_secs": 120
}
```

The field `"sleep_secs"` tells the bot how many seconds to wait between each time that it checks GitHub for new commits. Note that the GitHub API limits unauthenticated API requests to 60 per hour. If you need your bot to check GitHub more frequently that once per minute, you will need to look into how to add authentication to your bot. You may also wish to look into GitHub API WebHooks.

## Running the bot:

After creating the `configure.json` file, simply run the code:

    python subreddit-updater.py
