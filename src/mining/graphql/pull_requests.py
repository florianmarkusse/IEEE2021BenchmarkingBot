# File that collects all the PR data from the projects that is used in the data analysis that is possible to
# be retrieved through the graphQL API from GitHub.

import datetime
import time
import requests

from src.utility.helpers import get_date_from_string


# A simple function to use requests.post to make the API call. Note the json= section.
def run_query(query, token):
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
    # Initial values
    results = []
    final_cursor = ""

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

    # Throw away cursor, only needed for pagination while querying GrapgQL database.
    for result in results:
        pull_requests.append(result.get("node"))

    return pull_requests


def get_new_start_date(created_at):
    return get_date_from_string(created_at).date()


def get_updated_cursor(temp_result, last_pr):
    # Get cursor of PR that has same "createdAt" value as last_pr
    prs = temp_result["data"]["search"]["edges"]

    for pr in prs:
        if pr["node"]["createdAt"] == last_pr["node"]["createdAt"]:
            return pr["cursor"]

    raise Exception("Could not get an updated cursor")
