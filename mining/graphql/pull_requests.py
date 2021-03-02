# File that collects all the PR data from the projects that is used in the data analysis that is possible to 
# be retrieved through the graphQL API from GitHub.

import requests
import json


def run_query(query, token): # A simple function to use requests.post to make the API call. Note the json= section.

  headers = {"Authorization": "token {token}".format(token=token)}

  request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
  if request.status_code == 200:
      return request.json()
  else:
      raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

        
# The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.      
def get_query(owner, repo, query, cursor):
  return """
  {{
    search(query: "user:{owner} repo:{repo} {query}", type: ISSUE, first: 100{cursor}) {{
      edges {{
      cursor
      node {{
        ... on PullRequest {{
          title
          createdAt
          merged
          mergedAt
          closed
          closedAt
          number
          participants {{
            totalCount
          }}
          reviews {{
            totalCount
          }}
          comments {{
            totalCount
          }}
          author {{
            login
          }}
          commits {{
            totalCount
          }}
          additions
          deletions
        }}
      }}
    }}
  }}
}}
""".format(owner=owner, repo=repo, query=query, cursor="" if cursor == "" else  ', after: "' + cursor + '"')

def get_prs(owner, repo, query, token):
  results = []
  final_cursor = ""

  while (len(results) % 100 == 0):
    query_result = run_query(get_query(owner, repo, query, final_cursor), token) # Execute the query
    edges = query_result["data"]["search"]["edges"]
    results.extend(edges)
    final_cursor = results[len(results) - 1]["cursor"]

  pull_requests = []

  # Throw away cursor, only needed for pagination while querying GrapgQL database.
  for result in results:
    pull_requests.append(result.get("node"))

  return pull_requests
