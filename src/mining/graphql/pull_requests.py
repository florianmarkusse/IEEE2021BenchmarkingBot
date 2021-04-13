# File that collects all the PR data from the projects that is used in the data analysis that is possible to
# be retrieved through the graphQL API from GitHub.

import time
import requests

from src.utility.helpers import get_date_from_string


# A simple function to use requests.post to make the API call. Note the json= section.
def run_query(query, token):
    """
    Function to send requests to GitHub's GraphQL API.

    Parameters
    ----------
    query : The query to send over.
    token : The Oauth token to be included.

    Returns
    -------
    The json that is returned by the request.
    """
    headers = {"Authorization": "token {token}".format(token=token)}

    request = requests.post('https://api.github.com/graphql',
                            json={'query': query}, headers=headers)

    wait_time = 2
    exponent = 0
    while request.status_code == 502:
        sleep_period = pow(wait_time, exponent)
        print("received 502, sleeping for {sleep_period} second(s)".format(sleep_period=sleep_period))
        time.sleep(sleep_period)
        request = requests.post('https://api.github.com/graphql',
                                json={'query': query}, headers=headers)
        exponent += 1

    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(
            request.status_code, query))


# The GraphQL query (with a few additional bits included) itself defined as a multi-line string.
def get_query(owner, repo, search_parameters, start_date, attributes, cursor):
    """
    Generate a valid GraphQL query to search for PR's on the repository.

    Parameters
    ----------
    owner : The owner of the repository.
    repo : The name of the repository.
    search_parameters : Which parameters to add to the query (e.g. "is:pr sort:created-desc")
    start_date : Which date to start searching.
    attributes : Which attributes to retrieve from the PR. (e.g. "additions")
    cursor : After which PR (cursor is used for pagination) to collect the next batch of PR's

    Returns
    -------
    A valid GraphQL query to search for PR's
    """
    return """
  {{
    search(query: "repo:{owner}/{repo} {search_parameters} created:>={start_date}", type: ISSUE, first: 100{cursor}) {{
      edges {{
      cursor
      node {{
        ... on PullRequest {{
          {attributes}
        }}
      }}
    }}
  }}
}}
""".format(owner=owner, repo=repo, search_parameters=search_parameters, start_date=start_date, attributes=attributes,
           cursor="" if cursor == "" else ', after: "' + cursor + '"')


def get_prs(owner, repo, search_parameters, start_date, attributes, token):
    """
    Gets all the PR's from the repository with the desired attributes.

    Parameters
    ----------
    owner : The owner of the repository.
    repo : The name of the repository.
    search_parameters : Which parameters to add to the query (e.g. "is:pr sort:created-desc")
    start_date : Which date to start searching.
    attributes : Which attributes to retrieve from the PR. (e.g. "additions")
    token : The Oauth token to be included.

    Returns
    -------
    All the PR's that are within the search parameters for this repository.
    """
    # Initial values
    results = []
    final_cursor = ""

    ##
    # Need to use boolean logic as it is only possible to know all were found when the query comes up empty twice in a
    # row. There is a maximum number of results for each query. However, this does not necessarily contain all the PR's
    # were requested. Therefore, if the query comes up empty first, the start date is moved to the last found PR to
    # create a new query that can return this maximum number of results again until all PR's are found.
    ##
    first_empty = False
    found_all = False

    while not found_all:
        query_result = run_query(
            get_query(owner, repo, search_parameters, start_date, attributes, final_cursor), token)  # Execute the query
        if len(query_result["data"]["search"]["edges"]) == 0:
            if first_empty:
                found_all = True
            first_empty = True

            start_date = get_new_start_date(results[len(results) - 1]["node"]["createdAt"])

            # Perform query to get new cursor for new set of results
            # Because cursor for result changes when query changes sadly and we do not want duplicates in final result
            temp_query_result = run_query(
                get_query(owner, repo, search_parameters, start_date, attributes, ""), token)

            final_cursor = get_updated_cursor(temp_query_result, results[len(results) - 1])
        else:
            first_empty = False
            edges = query_result["data"]["search"]["edges"]
            results.extend(edges)
            print("current size of PR's is {size}".format(size=len(results)))
            final_cursor = results[len(results) - 1]["cursor"]

    pull_requests = []

    # Throw away cursor, only needed for pagination while querying GraphQL database.
    for result in results:
        pull_requests.append(result.get("node"))

    # Remove "totalCount" extra depth for ease-of-use.
    for pr in pull_requests:
        pr["reviews"] = pr["reviews"]["totalCount"]
        pr["comments"] = pr["comments"]["totalCount"]
        pr["commits"] = pr["commits"]["totalCount"]

    return pull_requests


def get_new_start_date(created_at):
    """
    Helper function to get the new start date for the query. This will be the date for which the final PR, that is
    currently in the data set, was created.

    Parameters
    ----------
    created_at : At what time a resulting PR from the query was created.

    Returns
    -------
    The new start date for the GraphQL query.
    """
    return get_date_from_string(created_at).date()


def get_updated_cursor(temp_result, last_pr):
    """
    When the query's start date parameter changes, so does the cursor. Therefore, before continuing retrieving new PR's,
    update the cursor of the last found PR to avoid getting duplicated in the data set.

    Parameters
    ----------
    temp_result : The results of the first new query to find the updated cursor for the PR that was already collected.
    last_pr : The last PR that was collected from the previous query.

    Returns
    -------
    The new cursor of @last_pr.
    """
    # Get cursor of PR that has same "createdAt" value as last_pr
    prs = temp_result["data"]["search"]["edges"]

    for pr in prs:
        if pr["node"]["createdAt"] == last_pr["node"]["createdAt"]:
            return pr["cursor"]

    raise Exception("Could not get an updated cursor")
