import json
import os


def make_project_folder(path, owner, repo):
    """
    Makes the folder that stores the data for the PR's
    """
    if not os.path.isdir(path + "/" + owner):
        os.mkdir(path + "/" + owner)
    if not os.path.isdir(path + "/" + owner + "/" + repo):
        os.mkdir(path + "/" + owner + "/" + repo)


def write_data(pull_requests, owner, repo, file_name):
    """
    Writes the PR data to the file in json format
    """
    path = "../data/projects"
    make_project_folder(path, owner, repo)

    json_data = json.dumps(pull_requests)

    file = open(path + "/" + owner + "/" + repo +
                "/" + file_name + ".json", "w")
    file.write(json_data)
    file.close()


def get_token():
    """
    Gets the GitHub authorization token.
    """
    file = open("../token.txt", "r")
    token = file.read()
    file.close()
    return token


def get_projects_to_mine():
    """
    Gets all the projects to mine from along with the queries to get the correct PR's
    """
    file = open("../settings/projects.json", "r")
    projects = json.loads(file.read())
    file.close()
    return projects


def get_extensions():
    """
    Gets all the extensions that are considered source files
    """
    file = open("../settings/programming_file_extensions.json", "r")
    extensions = json.loads(file.read())
    file.close()
    return extensions


def get_graphql_parameters():
    """
    Gets the parameters to collect on the PR's in the GraphQL query and their description.
    """
    file = open("../settings/graphql_attributes_to_collect.json", "r")
    attributes = json.loads(file.read())
    file.close()
    return attributes


def get_mined_PRs(owner, repo):
    prs = {}

    path = "../data/projects/{owner}/{repo}".format(owner=owner, repo=repo)

    files = [
        ("allPRs", "all_prs"),
        ("botPRs", "bot_prs"),
        ("similarToBotPRs", "similar_to_bot_prs"),
    ]

    for file in files:
        full_path = path + "/{file_name}.json".format(file_name=file[0])

        name = file[1]

        file = open(full_path, "r")

        prs[name] = json.loads(file.read())
        file.close()

    return prs
