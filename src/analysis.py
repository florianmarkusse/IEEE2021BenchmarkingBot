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

    prs = file_management.get_mined_PRs(owner, repo)

    print(len(prs.get("all_prs")))
    print(len(prs.get("bot_prs")))
    print(len(prs.get("similar_to_bot_prs")))

    # Create summarizing data.
    # Calculate fraction of bot contribution all-time and monthly basis

    all_prs_per_month = helpers.periodize_prs(prs.get("all_prs"), "%m-%y")
    all_bot_prs_per_month = helpers.periodize_prs(prs.get("bot_prs"), "%m-%y")

    period_summaries = []

    for period in all_prs_per_month:
        period_summary = {
            "period": period,
            "all_prs": len(all_prs_per_month[period]),
            "bot_prs": len(all_bot_prs_per_month[period]) if period in all_bot_prs_per_month else 0,
        }

        period_summary["fraction"] = period_summary["bot_prs"] / period_summary["all_prs"]

        period_summaries.append(period_summary)

    summary = {
        "totals": {
            "all_prs": len(prs.get("all_prs")),
            "bot_prs": len(prs.get("bot_prs")),
            "fraction": len(prs.get("bot_prs")) / len(prs.get("all_prs")),
            "similar_to_bot_prs": len(prs.get("similar_to_bot_prs"))
        },
        "periodized": period_summaries
    }

    print("{owner}/{repo}".format(owner=owner, repo=repo))
    print("period\tbot PR's\t non-bot PR's\tfraction\ttotal PR's")
    for period_summary in period_summaries:
        print("{period}\t{bot_prs}\t{non_bot_prs}\t{fraction}\t{all_prs}".format(
            period=period_summary["period"],
            bot_prs=period_summary["bot_prs"],
            non_bot_prs=period_summary["all_prs"]-period_summary["bot_prs"],
            fraction=period_summary["fraction"],
            all_prs=period_summary["all_prs"],
        ))

    file_management.write_data(summary, owner, repo, "summary")
