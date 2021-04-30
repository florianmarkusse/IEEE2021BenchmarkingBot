from src.utility import file_management
from src.mining import collector, matcher
from src.mining.enhancement import enhancement
from src.mining.rest import changed_files, participants_bot_callers_comment_lengths, reviewers
from src.analysis.plotting import qq_plot
import os, json

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

    path = f"../data/projects/{owner}/{repo}/allPRs.json"

    all_prs_file = open(path, "r")

    file_name = "allPRs"

    all_prs = json.loads(all_prs_file.read())

    print(f"Collecting {file_name} reviewers")
    reviewers.get_reviewers_prs(owner, repo, all_prs, token)
    file_management.write_data(all_prs, owner, repo, file_name)

    print(f"Enriching {file_name} with human comments")
    enhancement.add_human_comments_member(all_prs)
    file_management.write_data(all_prs, owner, repo, file_name)

    print(f"Enriching {file_name} with benchmark bot free participants")
    enhancement.add_benchmark_bot_free_participants_member(owner, repo, all_prs)
    file_management.write_data(all_prs, owner, repo, file_name)

    print(f"Enriching {file_name} with comments after benchmarking bot contribution")
    enhancement.add_comments_after_benchmarking_bot_contribution(owner, repo, all_prs)
    file_management.write_data(all_prs, owner, repo, file_name)

