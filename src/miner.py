import datetime

from src.mining.graphql import pull_requests
from src.mining.rest import changed_files
from utility import file_management
from utility import helpers

# Get projects to collect PR data for
projects = file_management.get_projects_to_mine()

# Get token for GitHub API
token = file_management.get_token()

# Get the GraphQL parameters, containing search parameters and description
graphql_parameters = file_management.get_graphql_parameters()

for project in projects:

    owner = project.get("owner")
    repo = project.get("repo")
    botQuery = project.get("botQuery")
    allQuery = project.get("allQuery")
    start_date = project.get("startDate")

    print("Collecting PR's with bot contribution")
    bot_prs = pull_requests.get_prs(
        owner,
        repo,
        botQuery,
        start_date,
        helpers.get_graphql_attributes(graphql_parameters),
        token
    )

    number_source_files_changed = []
    additions = []
    deletions = []

    # Add which files were changed in this PR.
    # In GraphQL it is only possible to get the number of files changed which includes documentation files
    # which is undesirable to get like to like comparison of PRs with bot usage and without bot usage.
    print("Collecting PR's with bot contribution changed files")
    changes = changed_files.get_changes(owner, repo, bot_prs, token)

    min_max_source_files_changed = (min(changes["source_files_changed"]), max(changes["source_files_changed"]))
    min_max_additions = (min(changes["additions"]), max(changes["additions"]))
    min_max_deletions = (min(changes["deletions"]), max(changes["deletions"]))

    # Collect all PR's
    print("Collecting all PR's")
    all_prs = pull_requests.get_prs(
        owner,
        repo,
        allQuery,
        start_date,
        helpers.get_graphql_attributes(graphql_parameters),
        token
    )

    # Add which files were changed in this PR.
    # In GraphQL it is only possible to get the number of files changed which includes documentation files
    # which is undesirable to get like to like comparison of PRs with bot usage and without bot usage.
    print("Collecting all PR's changed files")
    changed_files.get_changes(owner, repo, all_prs, token)

    # A subset of all the pr's that have similar source file amount changed and additions / deletions
    similar_to_bot_prs = []

    for pr in all_prs:
        if helpers.is_similar(pr, min_max_source_files_changed, min_max_additions, min_max_deletions):
            if not helpers.has_bot(pr, bot_prs):
                similar_to_bot_prs.append(pr)

    # Now have 3 datasets
    #   - The PR's where the bot contributes
    #   - All the PR's
    #   - The PR's that are similar to the bot PR's without bot contribution

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    print("found {size} PR's in total from {start_date} to {current_date}".format(
        size=len(all_prs),
        start_date=start_date,
        current_date=current_date)
    )
    print("found {size} PR's with bot contribution in total from {start_date} to {current_date}".format(
        size=len(bot_prs),
        start_date=start_date,
        current_date=current_date)
    )
    print("found {size} PR's similar to bot contribution in total from {start_date} to {current_date}".format(
        size=len(similar_to_bot_prs),
        start_date=start_date,
        current_date=current_date)
    )

    file_management.write_data(all_prs, owner, repo, "allPRs")
    file_management.write_data(bot_prs, owner, repo, "botPRs")
    file_management.write_data(similar_to_bot_prs, owner, repo, "similarToBotPRs")
