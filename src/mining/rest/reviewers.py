import requests
import time

per_page_number = 30  # max 100 per GitHub API
error_message = "GitHub Comments API does not have the review(s)."


def get_reviewers_pr_page(owner, repo, pull_number, page, token):
    headers = {
        'Authorization': "token " + token,
        'accept': 'application/vnd.github.v3+json'
    }

    payload = {
        'per_page': str(per_page_number),
        'page': str(page)
    }

    resp = requests.get('https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/reviews'.format(
        owner=owner, repo=repo, pull_number=str(pull_number)), headers=headers, params=payload)

    page_reviewers = []

    if len(resp.json()) == 0:
        return 999

    if resp.status_code == 200:
        for reviews in resp.json():
            if reviews is not None and "user" in reviews and reviews["user"] is not None and \
                    "login" in reviews["user"] and reviews["user"]["login"] is not None and \
                    reviews["user"]["login"] not in page_reviewers:
                page_reviewers.append(reviews["user"]["login"])
        return page_reviewers
    if resp.status_code == 403:
        print("Exceeded rate limit, waiting until window reset")
        sleep_period = int(resp.headers["X-RateLimit-Reset"]) - int(time.time()) + 10
        print("Sleeping for {sleep_period} second(s)".format(sleep_period=sleep_period))
        time.sleep(sleep_period)
        return get_reviewers_pr_page(owner, repo, pull_number, page, token)
    else:
        return 402


def get_reviewers_pr(owner, repo, pull_number, token):
    # Get possible caller in PR description.
    all_reviewers = []

    # Get possible callers(s) in PR comments.
    page = 0
    while True:
        page += 1
        page_reviewers = get_reviewers_pr_page(owner, repo, pull_number, page, token)
        if page_reviewers == 402:
            return error_message
        if page_reviewers == 999:
            return all_reviewers
        all_reviewers.extend(page_reviewers)
        all_reviewers = list(set(page_reviewers))


def get_reviewers_prs(owner, repo, prs, token):
    prs_completed = 0
    for pr in prs:
        pr["reviewers"] = get_reviewers_pr(owner, repo, pr.get("number"), token)

        if prs_completed % 100 == 0 and prs_completed > 0:
            print("currently found the reviewers for this many PR's: {size} out of {total_size}".format(
                size=prs_completed,
                total_size=len(prs)
            ))
        prs_completed += 1

    print("currently found the reviewers for this many PR's: {size}".format(size=prs_completed))
