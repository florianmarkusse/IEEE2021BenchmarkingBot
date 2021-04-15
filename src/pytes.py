from utility import file_management, helpers
import json
from src.mining.enhancement import enhancement
from src.mining.rest import changed_files, participants_bot_callers_comment_lengths, reviewers

# Get projects to collect PR data for
projects = file_management.get_projects_to_mine()

# Get token for GitHub API
token = file_management.get_token()

for project in projects:
    owner = project.get("owner")
    repo = project.get("repo")
    bot_query = project.get("botQuery")
    start_date = project.get("startDate")
    bot_call_string = project.get("botCallString")

    data_set_names = [
        "allPRs",
        "botPRs",
    ]

    for data_set_name in data_set_names:

        file = open(f"../data/projects/{owner}/{repo}/{data_set_name}.json", 'r')

        prs = json.loads(file.read())

        file.close()

        print(f"Enriching {data_set_name} with human comments")
        enhancement.add_human_comments_member(prs)
        file_management.write_data(prs, owner, repo, data_set_name)

        print(f"Enriching {data_set_name} with benchmark bot free participants")
        enhancement.add_benchmark_bot_free_participants_member(owner, repo, prs)
        file_management.write_data(prs, owner, repo, data_set_name)


