# File that collects all the PR data from the projects in 'projects.json' that is used in the data analysis that is possible to 
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
def get_query(cursor):
  return """
  {{
    search(query: "user:salesforce repo:lwc is:pr Best has detected that there is a in:comments created:>=2019-07-29 sort:created-desc", type: ISSUE, first: 100{result}) {{
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
""".format(result = "" if cursor == "" else  ', after: "' + cursor + '"')

def get_prs(owner, repo, query, token):
  pull_requests = []
  final_cursor = ""

  while (len(pull_requests) % 100 == 0):
    query_result = run_query(get_query(final_cursor), token) # Execute the query
    edges = query_result["data"]["search"]["edges"]
    pull_requests.extend(edges)
    final_cursor = pull_requests[len(pull_requests) - 1]["cursor"]

  return pull_requests
