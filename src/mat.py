import datetime

from src.mining import collector, matcher
from src.mining.enhancement import enhancement
from utility import file_management
from utility import helpers

# Get projects to collect PR data for
projects = file_management.get_projects_to_mine()

for project in projects:
    owner = project.get("owner")
    repo = project.get("repo")
    bot_query = project.get("botQuery")
    start_date = project.get("startDate")
    bot_call_string = project.get("botCallString")

    mined_prs = file_management.get_all_mined_prs(owner, repo)

    # Find Matchings.
    matcher.do_matchings(owner, repo, mined_prs.get("bot_prs"), mined_prs.get("non_bot_prs"))