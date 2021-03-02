# File to get all the changed files from a specific PR, returned in list type

import requests
import json

per_page_number = 30 # max 100 per GitHub API
error_message = "GitHub REST API does not have the file changed."

def get_changed_files_page(owner, repo, pull_number, page):

    file = open("token.txt", "r")
    token = file.read()
    file.close()

    headers = {
        'Authorization': "token " + token,
        'accept': 'application/vnd.github.v3+json'
    }

    payload = {
        'per_page': str(per_page_number),
        'page': str(page)
    }

    resp = requests.get('https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/files'.format(owner=owner, repo=repo, pull_number=str(pull_number)), headers=headers, params=payload)

    files = []

    if resp.status_code == 200:
        for file_change in resp.json():
            files.append(file_change.get("filename"))
    else:
        return 402

    return files

def get_all_changed_files(owner, repo, pull_number):

    all_changed_files = []
    files = []
    page = 0

    while len(all_changed_files) % 30 == 0:
        page += 1
        files = get_changed_files_page(owner, repo, pull_number, page)
        if files == 402:
            return error_message
        all_changed_files.extend(files)

    return all_changed_files
