import requests
import time

per_page_number = 30  # max 100 per GitHub API
error_message = "GitHub Comments API does not have the comments."

def get_bot_caller_participants_commenters_in_pr_page(owner, repo, pull_number, bot_call_string, page, token):
    headers = {
        'Authorization': "token " + token,
        'accept': 'application/vnd.github.v3+json'
    }

    payload = {
        'per_page': str(per_page_number),
        'page': str(page)
    }

    resp = requests.get('https://api.github.com/repos/{owner}/{repo}/issues/{pull_number}/comments'.format(
        owner=owner, repo=repo, pull_number=str(pull_number)), headers=headers, params=payload)

    page_results = {
        "callers": [],
        "participants": [],
        "commenterAndLengths": []
    }

    if len(resp.json()) == 0:
        return 999

    if resp.status_code == 200:
        for comments in resp.json():
            if comments["body"] is None:
                page_results["participants"].append(comments["user"]["login"])
                page_results["commenterAndLengths"].append((comments["user"]["login"], 0))
            else:
                if bot_call_string in comments["body"] and comments["user"]["login"] not in page_results["callers"]:
                    page_results["callers"].append(comments["user"]["login"])

                if comments["user"]["login"] not in page_results["participants"]:
                    page_results["participants"].append(comments["user"]["login"])

                page_results["commenterAndLengths"].append((comments["user"]["login"], len(comments["body"])))
        return page_results
    if resp.status_code == 403:
        print("Exceeded rate limit, waiting until window reset")
        sleep_period = int(resp.headers["X-RateLimit-Reset"]) - int(time.time()) + 10
        print("Sleeping for {sleep_period} second(s)".format(sleep_period=sleep_period))
        time.sleep(sleep_period)
        return get_bot_caller_participants_commenters_in_pr_page(owner, repo, pull_number, bot_call_string, page, token)
    else:
        return 402


def get_author_data(owner, repo, pull_number, bot_call_string, token):
    headers = {
        'Authorization': "token " + token,
        'accept': 'application/vnd.github.v3+json'
    }

    resp = requests.get('https://api.github.com/repos/{owner}/{repo}/issues/{pull_number}'.format(
        owner=owner, repo=repo, pull_number=str(pull_number)), headers=headers)

    if resp.status_code == 200:
        description = resp.json()
        if description["body"] is None:
            return {
                "callers": [],
                "participants": [description["user"]["login"]],
                "commenterAndLengths": [(description["user"]["login"], 0)]
            }
        if bot_call_string in description["body"]:
            return {
                "callers": [description["user"]["login"]],
                "participants": [description["user"]["login"]],
                "commenterAndLengths": [(description["user"]["login"], len(description["body"]))]
            }
        else:
            return {
                "callers": [],
                "participants": [description["user"]["login"]],
                "commenterAndLengths": [(description["user"]["login"], len(description["body"]))]
            }
    if resp.status_code == 403:
        print("Exceeded rate limit, waiting until window reset")
        sleep_period = int(resp.headers["X-RateLimit-Reset"]) - int(time.time()) + 10
        print("Sleeping for {sleep_period} second(s)".format(sleep_period=sleep_period))
        time.sleep(sleep_period)
        return get_author_data(owner, repo, pull_number, bot_call_string, token)
    else:
        return 402


def get_bot_caller_participants_commenters_in_pr(owner, repo, pull_number, bot_call_string, token):
    results = {
        "callers": [],
        "participants": [],
        "commenterAndLengths": []
    }

    # Get results from PR author.
    author_result = get_author_data(owner, repo, pull_number, bot_call_string, token)

    results["callers"].extend(author_result["callers"])
    results["participants"].extend(author_result["participants"])
    results["commenterAndLengths"].extend(author_result["commenterAndLengths"])

    # Get results from PR comments.
    page = 0
    while True:
        page += 1
        page_results = get_bot_caller_participants_commenters_in_pr_page(owner, repo, pull_number, bot_call_string, page, token)
        if page_results == 402:
            return error_message
        if page_results == 999:
            return results
        results["callers"].extend(page_results["callers"])
        results["callers"] = list(set(results["callers"]))

        results["participants"].extend(page_results["participants"])
        results["participants"] = list(set(results["participants"]))

        results["commenterAndLengths"].extend(page_results["commenterAndLengths"])


def get_bot_caller_participants_commenters_in_prs(owner, repo, prs, bot_call_string, token):
    prs_completed = 0
    for pr in prs:
        results = get_bot_caller_participants_commenters_in_pr(owner, repo, pr.get("number"), bot_call_string, token)

        pr["callers"] = results["callers"]
        pr["participants"] = results["participants"]
        pr["commenterAndLengths"] = results["commenterAndLengths"]

        if prs_completed % 100 == 0 and prs_completed > 0:
            print(
                f"currently found the bot callers/participants/commenters for this many PR's: {prs_completed} out of {len(prs)}")
        prs_completed += 1

    print(f"currently found the bot callers/participants/commenters for this many PR's: {prs_completed}")
