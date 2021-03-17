from utility import file_management

from src.mining.rest import bot_caller

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

    prs = file_management.get_mined_prs(owner, repo)
    bot_prs = prs.get("bot_prs")

    has_caller = [bot_pr for bot_pr in bot_prs if len(bot_pr["callers"]) > 0]
    print(len(has_caller))
