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

    path = f"../data/projects/{owner}/{repo}"

    all_prs_full_path = path + f"/allPRs.json"
    non_bot_full_path = path + f"/botPRs.json"

    all_prs_file = open(all_prs_full_path, "r")
    non_bot_prs_file = open(non_bot_full_path, "r")

    all_prs = json.loads(all_prs_file.read())
    all_prs_numbers = [pr["number"] for pr in all_prs]
    bot_prs = json.loads(non_bot_prs_file.read())
    bot_prs_numbers = [pr["number"] for pr in bot_prs]

    all_prs_file.close()
    non_bot_prs_file.close()

    enhancement.add_benchmark_bot_free_participants_member(owner, repo, all_prs)
    enhancement.add_human_comments_member(owner, repo, all_prs)
    file_management.write_data(all_prs, owner, repo, "allPRs")

    enhancement.add_benchmark_bot_free_participants_member(owner, repo, bot_prs)
    enhancement.add_human_comments_member(owner, repo, bot_prs)
    file_management.write_data(bot_prs, owner, repo, "botPRs")

    # Create non bot PR's.
    matcher.create_non_bot_prs(owner, repo)

    data = file_management.get_all_mined_prs(owner, repo)
    matcher.do_matchings(owner, repo, data.get("bot_prs"), data.get("non_bot_prs"))

