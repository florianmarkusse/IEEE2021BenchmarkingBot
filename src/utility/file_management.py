import json
import os


def make_project_folder(path, owner, repo):
    """
    Makes the folder that stores the data for the PR's
    """
    make_folder(path + "/" + owner)
    make_folder(path + "/" + owner + "/" + repo)
    make_folder(path + "/" + owner + "/" + repo + "/" + "images")
    make_folder(path + "/" + owner + "/" + repo + "/" + "images" + "/" + "examples")
    make_folder(path + "/" + owner + "/" + repo + "/" + "images" + "/" + "graphs")
    make_folder(path + "/" + owner + "/" + repo + "/" + "images" + "/" + "graphs" + "/" + "scatter")
    make_folder(path + "/" + owner + "/" + repo + "/" + "images" + "/" + "graphs" + "/" + "combo")
    make_folder(path + "/" + owner + "/" + repo + "/" + "images" + "/" + "graphs" + "/" + "frequency")
    make_folder(path + "/" + owner + "/" + repo + "/" + "images" + "/" + "graphs" + "/" + "pie")
    make_folder(path + "/" + owner + "/" + repo + "/" + "images" + "/" + "graphs" + "/" + "boxplot")
    make_folder(path + "/" + owner + "/" + repo + "/" + "images" + "/" + "graphs" + "/" + "top_ten")
    make_folder(path + "/" + owner + "/" + repo + "/" + "images" + "/" + "graphs" + "/" + "qq")


def make_folder(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def write_data(pull_requests, owner, repo, file_name):
    """
    Writes the PR data to the file in json format
    """
    path = "data/projects"
    make_project_folder(path, owner, repo)

    json_data = json.dumps(pull_requests)

    file = open(path + "/" + owner + "/" + repo +
                "/" + file_name + ".json", "w")
    file.write(json_data)
    file.close()


def write_summary(data, file_name):
    path = "data/summary"

    json_data = json.dumps(data)

    file = open(path + "/" + file_name + ".json", "w")
    file.write(json_data)
    file.close()

def read_summary(file_name):
    path = "data/summary"
    file = open(path + "/" + file_name + ".json", "r")
    data = file.read()
    file.close()

    json_data = json.loads(data)

    return json_data

def get_token():
    """
    Gets the GitHub authorization token.
    """
    file = open("token.txt", "r")
    token = file.read()
    file.close()
    return token


def get_projects_to_mine():
    """
    Gets all the projects to mine from along with the queries to get the correct PR's
    """
    file = open("settings/projects.json", "r")
    projects = json.loads(file.read())
    file.close()
    return projects


def get_metric_file(owner, repo, file):
    path = f"data/projects/{owner}/{repo}/{file}.json"
    file = open(path, "r")
    projects = json.loads(file.read())
    file.close()
    return projects


def get_extensions():
    """
    Gets all the extensions that are considered source files
    """
    file = open("settings/programming_file_extensions.json", "r")
    extensions = json.loads(file.read())
    file.close()
    return extensions


def get_graphql_parameters():
    """
    Gets the parameters to collect on the PR's in the GraphQL query and their description.
    """
    file = open("settings/graphql_attributes_to_collect.json", "r")
    attributes = json.loads(file.read())
    file.close()
    return attributes


def get_all_mined_prs(owner, repo):
    path = f"data/projects/{owner}/{repo}"

    # (bot PR's file name, all PR's file name, data set name)
    data_set = ("botPRs", "nonBotPRs", "BOT PRS - NON BOT PRS")

    bot_prs_full_path = path + f"/{data_set[0]}.json"
    non_bot_prs_full_path = path + f"/{data_set[1]}.json"

    bot_prs_file = open(bot_prs_full_path, "r")
    non_bot_prs_file = open(non_bot_prs_full_path, "r")

    data_set = {
        "name": data_set[2],
        "bot_prs_name": "Bot PR's",
        "non_bot_prs_name": "Non bot PR's",
        "bot_prs": json.loads(bot_prs_file.read()),
        "non_bot_prs": json.loads(non_bot_prs_file.read())
    }

    bot_prs_file.close()
    non_bot_prs_file.close()

    return data_set


def get_data_sets(owner, repo):
    prs = []

    path = f"data/projects/{owner}/{repo}"

    comparison_data_sets = [
        # (bot PR's file name, all PR's file name, data set name)
        # ("botPrsPerformanceLabels", "nonBotPrsPerformanceLabels", "A"),
        # ("botPRsOneToOne", "nonBotPRsOneToOne", "B"),
        ("botPRsChangedSourceFilesAtLeast2", "nonBotPRsChangedSourceFilesAtLeast2", "C"),
        ("botPRsChangedSourceFilesAtLeast4", "nonBotPRsChangedSourceFilesAtLeast4", "D"),
        ("botPRsChangedSourceFilesAtLeast8", "nonBotPRsChangedSourceFilesAtLeast8", "E"),
    ]

    for data_sets in comparison_data_sets:
        bot_prs_full_path = path + f"/{data_sets[0]}.json"
        non_bot_prs_full_path = path + f"/{data_sets[1]}.json"

        bot_prs_file = open(bot_prs_full_path, "r")
        non_bot_prs_file = open(non_bot_prs_full_path, "r")

        prs.append({
            "name": data_sets[2],
            "bot_prs_name": "Bot PR's",
            "non_bot_prs_name": "Similar PR's'",
            "bot_prs": json.loads(bot_prs_file.read()),
            "non_bot_prs": json.loads(non_bot_prs_file.read())
        })

        bot_prs_file.close()
        non_bot_prs_file.close()

    return prs


def get_data_set_pairs(owner, repo):
    path = f"data/projects/{owner}/{repo}"
    files_in_dir = os.listdir(path)
    data_files = [file for file in files_in_dir if file.endswith(".json")]

    data_set_pairs = []

    for data_file in data_files:
        pair_file = "non" + data_file[0].upper() + data_file[1:]
        if pair_file in data_files:
            name = data_file[3:len(data_file) - 5]

            bot_prs_full_path = path + f"/{data_file}"
            non_bot_prs_full_path = path + f"/{pair_file}"

            bot_prs_file = open(bot_prs_full_path, "r")
            non_bot_prs_file = open(non_bot_prs_full_path, "r")

            data_set_pairs.append({
                "name": name,
                "bot_prs_name": "Bot PR's",
                "non_bot_prs_name": "Similar non-bot PR's'",
                "bot_prs": json.loads(bot_prs_file.read()),
                "non_bot_prs": json.loads(non_bot_prs_file.read())
            })

            bot_prs_file.close()
            non_bot_prs_file.close()

    return data_set_pairs
