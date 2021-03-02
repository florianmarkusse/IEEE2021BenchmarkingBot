from utility import file_management
from mining.graphql import pull_requests
from mining.rest import changedFiles

# Get projects to collect PR data for
projects = file_management.get_projects_to_mine()

# Get token for GitHub API
token = file_management.get_token()

for project in projects:

  owner = project.get("owner")
  repo = project.get("repo")
  botQuery = project.get("botQuery")
  allQuery = project.get("allQuery")

  bot_prs = pull_requests.get_prs(owner, repo, botQuery, token)

  number_source_files_changed = []
  additions = []
  deletions = []

  # Add which files were changed in this PR.
  # In GraphQL it is only possible to get the number of files changed which includes documentation files 
  # which is undesirable to get like to like comparison of PRs with bot usage and without bot usage.
  for bot_pr in bot_prs:
    all_changed_files = changedFiles.get_all_changed_files(owner, repo, bot_pr.get("number"))
    if isinstance(all_changed_files, list):
      all_changed_source_files = file_management.get_only_source_files(all_changed_files)
      number_source_files_changed.append(len(all_changed_files))

    additions.append(bot_pr.get("additions"))
    deletions.append(bot_pr.get("deletions"))

  print(additions)
  print(len(additions))

  print(deletions)
  print(len(deletions))

  print(number_source_files_changed)
  print(len(number_source_files_changed))

  print(bot_prs[0].get("number"))

  print(len(bot_prs))
