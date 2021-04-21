import requests
import time
from src.utility import helpers

per_page_number = 30  # max 100 per GitHub API
error_message = "GitHub Commits API does not have the commits(s)."


def get_commits_open_pr_page(owner, repo, pull_number, created_date, page, token):
    headers = {
        'Authorization': "token " + token,
        'accept': 'application/vnd.github.v3+json'
    }

    payload = {
        'per_page': str(per_page_number),
        'page': str(page)
    }

    resp = requests.get('https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/commits'.format(
        owner=owner, repo=repo, pull_number=str(pull_number)), headers=headers, params=payload)

    page_commits_at_open = 0

    if resp.status_code == 200:
        for commit in resp.json():
            if commit is not None and "commit" in commit and commit["commit"] is not None and \
                    "author" in commit["commit"] and commit["commit"]["author"] is not None and \
                    "date" in commit["commit"]["author"] and commit["commit"]["author"]["date"] is not None:
                # Check if before pr Created
                if helpers.get_date_from_string(commit["commit"]["author"]["date"]) < created_date:
                    page_commits_at_open += 1
        return page_commits_at_open
    if resp.status_code == 403:
        print("Exceeded rate limit, waiting until window reset")
        sleep_period = int(resp.headers["X-RateLimit-Reset"]) - int(time.time()) + 10
        print("Sleeping for {sleep_period} second(s)".format(sleep_period=sleep_period))
        time.sleep(sleep_period)
        return get_commits_open_pr_page(owner, repo, pull_number, created_date, page, token)
    else:
        return 402


def get_commits_open_pr(owner, repo, pull_number, created_date, token):
    # Get possible caller in PR description.
    all_commits_at_open = 0

    # Get possible callers(s) in PR comments.
    page = 0
    while True:
        page += 1
        page_commits_at_open = get_commits_open_pr_page(owner, repo, pull_number, created_date, page, token)
        if page_commits_at_open == 402:
            return error_message
        all_commits_at_open += page_commits_at_open
        if page_commits_at_open < per_page_number:
            return all_commits_at_open


def get_commits_prs(owner, repo, prs, token):
    prs_completed = 0
    for pr in prs:
        pr["commitsAtOpen"] = get_commits_open_pr(owner, repo, pr.get("number"),
                                                  helpers.get_date_from_string(pr.get("createdAt")), token)

        if prs_completed % 100 == 0 and prs_completed > 0:
            print("currently found the commits at open for this many PR's: {size} out of {total_size}".format(
                size=prs_completed,
                total_size=len(prs)
            ))
        prs_completed += 1

    print("currently found the reviewers for this many PR's: {size}".format(size=prs_completed))
