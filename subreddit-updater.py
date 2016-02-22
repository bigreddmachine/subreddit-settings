from __future__ import print_function
import time
import hashlib
from datetime import datetime
import json
import praw
import requests
import requests.auth
from git import Repo

def main():
    printCurrentTime()
    
    # Load config file and set up credentials:
    with open('configure.json') as data_file:
        config = json.load(data_file)
    reddit = RedditBot(config)
    github = GithubRepo(config)
    r = getPraw(reddit)
        
    # Make sure subreddit is initially up-to-date with local files:
    github = checkRepoCommits(github, reddit, r)
    goToSleep(config["sleep_secs"])
    
    # Begin continuous loop checking for subreddit updates:
    while True:
        printCurrentTime()
        
        try:
            github = checkRepoCommits(github, reddit, r)
        except:
            logError('There was an error in "checkRepoCommits". Will try again in ' + str(config["sleep_secs"]) + ' seconds.')
        
        goToSleep(config["sleep_secs"])
        r = getPraw(reddit)

# Reddit user and subreddit configuration:
class RedditBot:
    def __init__(self, config):
        # Configure reddit settings:
        self.username  = config['reddit_user']
        self.password  = config['reddit_pass']
        self.subreddit = config['subreddit']
        self.about     = config['about_bot']
        self.id        = config['reddit_id']
        self.secret    = config['reddit_secret']
        self.uri       = config['redirect_uri']

# Github repository information and api config:
class GithubRepo:
    def __init__(self, config):
        self.owner      = config['github_owner']
        self.repo       = config['github_repo']
        self.stylesheet = config['stylesheet']
        self.sidebar    = config['sidebar']
        owner_plus_repo = self.owner + '/' + self.repo
        self.repo_api    = 'https://api.github.com/repos/' + owner_plus_repo
        self.repo_url    = 'https://github.com/' + owner_plus_repo
        self.last_commit = ''
        self.style_md5   = ''
        self.sidebar_md5 = ''

# get praw object with OAuth2 access credentials set
def getPraw(reddit):
    # you MUST provide custom User-Agent header in the request to play nicely with Reddit API guidelines
    r = praw.Reddit(user_agent = reddit.about,
        oauth_client_id = reddit.id,
        oauth_client_secret = reddit.secret,
        oauth_redirect_uri = reddit.uri)
    # this tells PRAW our authentication details
    scopes = "modconfig modwiki wikiread wikiedit"
    r.set_access_credentials(scopes, getAccessToken(reddit))
    return r
    
# obtain OAuth2 access token
def getAccessToken(reddit):
    response = requests.post("https://www.reddit.com/api/v1/access_token",
        # client id and client secret are obtained via your reddit account
        auth = requests.auth.HTTPBasicAuth(reddit.id, reddit.secret),
        # provide your reddit user id and password
        data = {"grant_type": "password", "username": reddit.username, "password": reddit.password},
        # you MUST provide custom User-Agent header in the request to play nicely with Reddit API guidelines
        headers = {"User-Agent": reddit.about})
    response = dict(response.json())
    return response["access_token"]

# Check github & update subreddit if necessary:
def checkRepoCommits(github, reddit, r):
    # Get newest github repo commit hash:
    url = github.repo_api + '/commits'
    try:
        resp = requests.get(url)
        output = resp.json()
        newest = output[0]['sha']
    except:
        logError('There was an error checking the Github API.')
        return github
    
    # Update repo if new commit(s) & update subreddit:
    if (newest != github.last_commit):
        # pull newest repo commits:
        github = checkGithubRepo(github, newest)
    else:
        logStatus('No new GitHub commits.')
    
    # check stylesheet and update if necessary:
    github = checkSubredditStylesheet(github, reddit, r)
    
    # check sidebar and update if necessary:
    github = checkSubredditSidebar(github, reddit, r)
    
    return github

# Sync local repo with github:
def checkGithubRepo(github, newest):
    try:
        logStatus('Syncing local repo to GitHub.')
        repo = Repo('.')
        o = repo.remotes.origin
        o.pull()
        github.last_commit = newest
    except:
        logError('There was an error pulling from github.')
    return github

# Sync subreddit with local stylesheet file:
def checkSubredditStylesheet(github, reddit, r):
    try:
        newest_style = md5checksum(github.stylesheet)
        if (newest_style != github.style_md5):
            logStatus('Updating subreddit stylesheet.')
            updateSubredditCSS(github, reddit, r)
            github.style_md5 = newest_style
        else:
            logStatus('Stylesheet is up to date. Do not update.')
    except:
        logError('There was an error updating the stylesheet.')
    return github

# Sync subreddit with local sidebar file:
def checkSubredditSidebar(github, reddit, r):
    try:
        newest_sidebar = md5checksum(github.sidebar)
        if (newest_sidebar != github.sidebar_md5):
            logStatus('Updating subreddit sidebar.')
            updateSubredditSidebar(github, reddit, r)
            github.sidebar_md5 = newest_sidebar
        else:
            logStatus('Sidebar is up to date. Do not update.')
    except:
        logError('There was an error updating the sidebar file.')
    return github

# Update subreddit stylesheet:
def updateSubredditCSS(github, reddit, r):
    stylesheet = getFile(github.stylesheet)
    r.set_stylesheet(reddit.subreddit, stylesheet)

# Update subreddit sidebar contents:
def updateSubredditSidebar(github, reddit, r):
    sidebar_contents = getFile(github.sidebar)
    subreddit = r.get_subreddit(reddit.subreddit)
    r.edit_wiki_page(subreddit, 'config/sidebar', sidebar_contents, reason='')
    # r.update_settings(subreddit, description=sidebar_contents)

# Log into reddit:
def redditLogin(reddit):
    r = praw.Reddit(reddit.about)
    r.login(reddit.username, reddit.password)
    return r

# Get MD5 checksum of file:
def md5checksum(filename):
	hasher = hashlib.md5()
	hasher.update(getFile(filename))
	return hasher.hexdigest()

# Get contents of file:
def getFile(filename):
    # Reads a file and returns contents
    with open(filename) as f:
        return f.read()

# Prints the current time in easy-to-read format:
def printCurrentTime():
     logStatus(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
     
# Sleep for X seconds:
def goToSleep(X):
    logStatus('Going to sleep for ' + str(X) + ' seconds.\n')
    time.sleep(X)

# Log message to console:
def logStatus(message):
    print(message)

# Log error message to console:
def logError(message):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ', '
    print('ERROR: ' + current_time +  message)

if __name__ == "__main__":
    main()
