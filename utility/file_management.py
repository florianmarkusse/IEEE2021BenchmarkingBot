import os 
import json

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

def get_token():
  file = open("token.txt", "r")
  token = file.read()
  file.close()
  return token

def get_projects_to_mine():
  file = open("projects.json", "r")
  projects = json.loads(file.read())
  file.close()
  return projects