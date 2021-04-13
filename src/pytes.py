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
        "allPRs"
    ]

    for data_set_name in data_set_names:

        file = open(f"../data/projects/{owner}/{repo}/{data_set_name}.json", 'r')

        prs = json.loads(file.read())

        for pr in prs:
            if "comment_lengths" in pr:
                pr.pop("comment_lengths")


        file.close()

        print(f"Collecting {data_set_name} participants/bot callers/comment lengths")
        participants_bot_callers_comment_lengths.get_bot_caller_participants_commenters_in_prs(owner, repo, prs,
                                                                                               bot_call_string, token)
        file_management.write_data(prs, owner, repo, data_set_name)

        print(f"Collecting {data_set_name} reviewers")
        reviewers.get_bot_callers_prs(owner, repo, prs, token)
        file_management.write_data(prs, owner, repo, data_set_name)

        print(f"Enriching {data_set_name} with human comments")
        enhancement.add_human_comments_member(prs)
        file_management.write_data(prs, owner, repo, data_set_name)

        print(f"Enriching {data_set_name} with benchmark bot free participants")
        enhancement.add_benchmark_bot_free_participants_member(prs)
        file_management.write_data(prs, owner, repo, data_set_name)

        file_management.write_data(prs, owner, repo, data_set_name)


