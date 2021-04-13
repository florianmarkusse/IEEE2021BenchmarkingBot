import datetime

from src.mining import collector, matcher
from utility import file_management
from utility import helpers

# Get projects to collect PR data for
projects = file_management.get_projects_to_mine()

# Get token for GitHub API
token = file_management.get_token()

# Get the GraphQL parameters, containing search parameters and description
graphql_parameters = file_management.get_graphql_parameters()

# Standard query to collect PR's
standard_query = "is:pr is:closed sort:created-asc"

for project in projects:
    owner = project.get("owner")
    repo = project.get("repo")
    bot_query = project.get("botQuery")
    start_date = project.get("startDate")
    bot_call_string = project.get("botCallString")

    print("Mining PR's from project {owner}/{repo}".format(owner=owner, repo=repo))

    bot_prs = collector.collect_and_enrich(owner, repo, standard_query + " " + bot_query, start_date,
                                           helpers.get_graphql_attributes(graphql_parameters), bot_call_string,
                                           "botPRs", token)
    all_prs = collector.collect_and_enrich(owner, repo, standard_query, start_date,
                                           helpers.get_graphql_attributes(graphql_parameters), bot_call_string,
                                           "allPRs", token)

    # Find Matchings.
    matcher.do_matchings(owner, repo, bot_prs, all_prs)

    # Now we have the following:
    #   - The PR's where the bot contributes
    #   - All the PR's
    #   - bot PR's one-to-one matched to
    #   - similar PR's
    #   - performance labeled bot PR's
    #   - performance labeled all PR's

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    print(f"Found {len(all_prs)} PR's in total from {start_date} to {current_date}")
    print(f"Found {len(bot_prs)} PR's with bot contribution in total from {start_date} to {current_date}")
