import requests
import time

per_page_number = 30  # max 100 per GitHub API
error_message = "GitHub Comments API does not have the comments."


def get_bot_callers_pull_page(owner, repo, pull_number, bot_call_string, page, token):
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

    callers = []

    if len(resp.json()) == 0:
        return 999

    if resp.status_code == 200:
        for comments in resp.json():
            if bot_call_string in comments["body"]:
                callers.append(comments["user"]["login"])
        return callers
    if resp.status_code == 403:
        print("Exceeded rate limit, waiting until window reset")
        sleep_period = int(resp.headers["X-RateLimit-Reset"]) - int(time.time()) + 10
        print("Sleeping for {sleep_period} second(s)".format(sleep_period=sleep_period))
        time.sleep(sleep_period)
        return get_bot_callers_pull_page(owner, repo, pull_number, page, token)
    else:
        return 402


def get_bot_callers_pr(owner, repo, pull_number, bot_call_string, token):
    all_bot_callers = []
    page = 0

    while True:
        page += 1
        callers = get_bot_callers_pull_page(owner, repo, pull_number, bot_call_string, page, token)
        if callers == 402:
            return error_message
        if callers == 999:
            return all_bot_callers
        all_bot_callers.extend(callers)


def get_bot_callers_prs(owner, repo, prs, bot_call_string, token):
    bot_callers_per_pr_found = 0
    for pr in prs:
        pr["callers"] = get_bot_callers_pr(owner, repo, pr.get("number"), bot_call_string, token)

        if bot_callers_per_pr_found % 100 == 0 and bot_callers_per_pr_found > 0:
            print("currently found the bot callers for this many PR's: {size} out of {total_size}".format(
                size=bot_callers_per_pr_found,
                total_size=len(prs)
            ))
        bot_callers_per_pr_found += 1

    print("currently found the bot callers for this many PR's: {size}".format(size=bot_callers_per_pr_found))
