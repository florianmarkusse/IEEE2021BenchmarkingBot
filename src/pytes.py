from src.utility import file_management
import os

# Get projects to collect PR data for
projects = file_management.get_projects_to_mine()

# Get token for GitHub API
# token = file_management.get_token()

for project in projects:
    owner = project.get("owner")
    repo = project.get("repo")
    bot_query = project.get("botQuery")
    start_date = project.get("startDate")
    bot_call_string = project.get("botCallString")

    data_set_pairs = file_management.get_data_set_pairs(owner, repo)

    for data_set_pair in data_set_pairs:
        print(data_set_pair["name"])
        print(data_set_pair["bot_prs_name"])
        print(data_set_pair["non_bot_prs_name"])
        print(len(data_set_pair["bot_prs"]))
        print(len(data_set_pair["non_bot_prs"]))
