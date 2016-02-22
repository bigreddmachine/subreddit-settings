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
  "github_owner": "YOUR_GITHUB_NAME",
  "github_repo": "FORKED_REPO_NAME",
  "reddit_user": "BOT_USERNAME",
  "reddit_pass": "BOT_PASSWORD",
  "reddit_id": "BOT_APP_ID",
  "reddit_secret": "BOT_APP_SECRET",
  "subreddit": "SUBREDDIT",
  "about_bot": "a simple statement telling reddit what your bot does",
  "redirect_uri": "BOT_REDIRECT_URI",
  "stylesheet": "stylesheet.css",
  "sidebar": "sidebar.txt",
  "sleep_secs": 120
}
```

For example, your `configure.json` file might look like this:

```json
{
  "github_owner": "micro-machine",
  "github_repo": "subreddit-settings",
  "reddit_user": "me_on_reddit",
  "reddit_pass": "mypassword",
  "reddit_id": "myredditappid",
  "reddit_secret": "myredditappsecret",
  "subreddit": "mysubreddit",
  "about_bot": "/r/mysubreddit subreddit updater by /u/me_on_reddit",
  "redirect_uri": "http://127.0.0.1:65010/authorize_callback",
  "stylesheet": "stylesheet.css",
  "sidebar": "sidebar.txt",
  "sleep_secs": 120
}
```

The field `"sleep_secs"` tells the bot how many seconds to wait between each time that it checks GitHub for new commits. Note that the GitHub API limits unauthenticated API requests to 60 per hour. If you need your bot to check GitHub more frequently that once per minute, you will need to look into how to add authentication to your bot. You may also wish to look into GitHub API WebHooks.

## How to set up a reddit app with OAuth2:

Reddit bot login with username and password is deprecated and set to be phased out in 2016. In order to set up this bot, you will need to set up a reddit account for use with OAuth2. I recommend that you set up this bot with a different reddit account than you use for posting, but you can use the same account if you would like. Whichever account you use will need Admin privileges on the subreddit it is updating.

For step by step instructions on getting the bot's reddit account set up for use, follow Step 1 of [Praw and OAuth](http://praw.readthedocs.org/en/stable/pages/oauth.html#step-1-create-an-application) on the reddit API docs. You will need to input you bot's `client_id`, `client_secret`, and `redirect_uri` into the `configure.json` file explained above.

## Running the bot:

After creating the `configure.json` file, simply run the code:

    python subreddit-updater.py
