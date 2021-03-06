from utility import file_management
from utility import helpers
from mining.graphql import pull_requests
from mining.rest import changed_files

# Get projects to collect PR data for
projects = file_management.get_projects_to_mine()

# Get token for GitHub API
token = file_management.get_token()

# Get the GraphQL parameters, containing seach parameters and description
graphql_parameters = file_management.get_graphql_parameters()

for project in projects:

    owner = project.get("owner")
    repo = project.get("repo")
    botQuery = project.get("botQuery")
    allQuery = project.get("allQuery")
    start_date = project.get("startDate")

    print("Collecting all bot_prs")
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
    print("Collecting bot_prs changed files")
    for bot_pr in bot_prs:

        bot_pr["changedFiles"] = changed_files.get_all_changed_files(
            owner, repo, bot_pr.get("number")
        )
        if isinstance(bot_pr.get("changedFiles"), list):
            bot_pr["changedSourceFiles"] = helpers.get_only_files_with_extensions(
                bot_pr.get("changedFiles"),
                file_management.get_extensions()
            )
            number_source_files_changed.append(
                len(
                    bot_pr.get("changedSourceFiles")
                )
            )

        additions.append(bot_pr.get("additions"))
        deletions.append(bot_pr.get("deletions"))

    min_max_source_files_changed = (min(number_source_files_changed), max(number_source_files_changed))
    min_max_additions = (min(additions), max(additions))
    min_max_deletions = (min(deletions), max(deletions))


    # Collect all PR's
    print("Collecting all all_prs")
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
    print("Collecting all_prs changed files")
    for pr in all_prs:

        pr["changedFiles"] = changed_files.get_all_changed_files(
            owner, repo, pr.get("number")
        )
        if isinstance(pr.get("changedFiles"), list):
            pr["changedSourceFiles"] = helpers.get_only_files_with_extensions(
                pr.get("changedFiles"),
                file_management.get_extensions()
            )
            number_source_files_changed.append(
                len(
                    pr.get("changedSourceFiles")
                )
            )


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
    print(len(all_prs))
    print(len(bot_prs))
    print(len(similar_to_bot_prs))




