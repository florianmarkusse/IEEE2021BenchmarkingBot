from src.utility import file_management
from src.mining import collector, matcher
from src.mining.enhancement import enhancement
from src.mining.rest import changed_files, participants_bot_callers_comment_lengths, reviewers
from src.analysis.plotting import qq_plot
import os, json
import random

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

    data_set_pairs = file_management.get_data_set_pairs(owner, repo)

    interesting_data_set = "PRsChangedSourceFilesAtLeast8"

    for pairs in data_set_pairs:
        sample_bot_prs = random.sample(pairs["bot_prs"], 10)
        sample_non_bot_prs = random.sample(pairs["non_bot_prs"], 10)

        file_management.write_data(sample_bot_prs, owner, repo, f"sample{pairs['name']}")
        file_management.write_data(sample_non_bot_prs, owner, repo, f"sampleNon{pairs['name']}")





