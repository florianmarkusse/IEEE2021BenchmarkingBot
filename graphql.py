import requests
import json
import os 

# Makes the folder that stores the data for the PR's
def make_project_folder(path, owner, repo):
  if (not os.path.isdir(path + "/" + owner)):
    os.mkdir(path + "/" + owner)
  if (not os.path.isdir(path + "/" + owner + "/" + repo)):
    os.mkdir(path + "/" + owner + "/" + repo)

# Writes the PR data to the file in json format
def write_data(pull_requests, owner, repo, is_only_bot):
  path = "projects"
  make_project_folder(path, owner, repo)

  fileName = "botPRData" if is_only_bot else "allPRData"
  jsonData = json.dumps(pull_requests)

  file = open(path + "/" + owner + "/" + repo + "/" + fileName + ".json" , "w")
  file.write(jsonData)
  file.close()

def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.

  file = open("token.txt", "r")
  token = file.read()
  file.close()

  headers = {"Authorization": "token {token}".format(token = token)}

  request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
  if request.status_code == 200:
      return request.json()
  else:
      raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

        
# The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.      
def get_query(cursor = ""):
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


# Get projects to collect PR data for
file = open("projects.json", "r")
projects = json.loads(file.read())
file.close()

print(type(projects[0]))

for project in projects:
  # Get bot PR data
  # Write to file

  # Get all PR data
  # Write to file

  # Create README.md in folder

  

# pull_requests = []

# query_result = run_query(get_query()) # Execute the query
# edges = query_result["data"]["search"]["edges"]
# pull_requests.extend(edges)
# final_cursor = pull_requests[len(pull_requests) - 1]["cursor"]

# while (len(edges) == 100):
#   query_result = run_query(get_query(final_cursor)) # Execute the query
#   edges = query_result["data"]["search"]["edges"]
#   pull_requests.extend(edges)
#   final_cursor = pull_requests[len(pull_requests) - 1]["cursor"]

# jsonData = json.dumps(pull_requests)

# file = open("test.json", 'a')
# file.write(jsonData)
# file.close()

