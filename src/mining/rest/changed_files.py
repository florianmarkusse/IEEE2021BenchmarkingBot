# File to get all the changed files from a specific PR, returned in list type

import requests
import time

from src.utility.helpers import get_only_files_with_extensions
from src.utility.file_management import get_extensions

per_page_number = 30  # max 100 per GitHub API
error_message = "GitHub REST API does not have the file(s) changed."


def get_changed_files_pull_page(owner, repo, pull_number, page, token):
    headers = {
        'Authorization': "token " + token,
        'accept': 'application/vnd.github.v3+json'
    }

    payload = {
        'per_page': str(per_page_number),
        'page': str(page)
    }

    res = {}
    try:
        resp = requests.get('https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/files'.format(
        owner=owner, repo=repo, pull_number=str(pull_number)), headers=headers, params=payload)
    except:
        print("Error")
        print("Sleeping for 60 second(s)")
        time.sleep(60)
        return get_changed_files_pull_page(owner, repo, pull_number, page, token)
    files = []

    if resp.status_code == 200:
        for file_change in resp.json():
            files.append(file_change.get("filename"))
        return files
    if resp.status_code == 403:
        print("Exceeded rate limit, waiting until window reset")
        sleep_period = int(resp.headers["X-RateLimit-Reset"]) - int(time.time()) + 10
        print("Sleeping for {sleep_period} second(s)".format(sleep_period=sleep_period))
        time.sleep(sleep_period)
        return get_changed_files_pull_page(owner, repo, pull_number, page, token)
    else:
        return 402


def get_all_changed_files_pull(owner, repo, pull_number, token):
    all_changed_files = []
    page = 0

    empty_page = False

    while not empty_page:
        page += 1
        files = get_changed_files_pull_page(owner, repo, pull_number, page, token)
        if files == 402:
            return error_message
        if len(files) == 0:
            empty_page = True
        all_changed_files.extend(files)

    return all_changed_files


def get_changes(owner, repo, prs, token):
    changes = {
        "source_files_changed": [],
        "additions": [],
        "deletions": []
    }

    changes_found = 0
    for pr in prs:
        pr["changedFiles"] = get_all_changed_files_pull(
            owner, repo, pr.get("number"), token
        )
        if isinstance(pr.get("changedFiles"), list):
            pr["changedSourceFiles"] = get_only_files_with_extensions(
                pr.get("changedFiles"),
                get_extensions()
            )
            changes["source_files_changed"].append(
                len(
                    pr.get("changedSourceFiles")
                )
            )

        changes["additions"].append(pr.get("additions"))
        changes["deletions"].append(pr.get("deletions"))

        if changes_found % 100 == 0 and changes_found > 0:
            print("currently found the changes for this many PR's: {size} out of {total_size}".format(
                size=changes_found,
                total_size=len(prs)
            ))
        changes_found += 1

    print("currently found the changes for this many PR's: {size}".format(size=changes_found))

    return changes
