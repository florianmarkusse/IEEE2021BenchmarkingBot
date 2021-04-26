from src.utility import file_management
from src.mining import collector, matcher
from src.mining.enhancement import enhancement
from src.mining.rest import changed_files, participants_bot_callers_comment_lengths, reviewers
from src.analysis.plotting import qq_plot
import os

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

    data = file_management.get_all_mined_prs(owner, repo)

    enhancement.add_comments_after_benchmarking_bot_contribution(owner, repo, data["bot_prs"])
    enhancement.add_comments_after_benchmarking_bot_contribution(owner, repo, data["non_bot_prs"])

    file_management.write_data(data["bot_prs"], owner, repo, "botPRs")
    file_management.write_data(data["non_bot_prs"], owner, repo, "nonBotPRs")

    matcher.do_matchings(owner, repo, data.get("bot_prs"), data.get("non_bot_prs"))
