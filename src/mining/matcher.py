from src.utility import helpers, file_management
import os
import json

def create_non_bot_prs(owner, repo):

    path = f"../data/projects/{owner}/{repo}"
    all_prs_full_path = path + "/allPRs.json"

    all_prs_file = open(all_prs_full_path, "r")
    all_prs = json.loads(all_prs_file.read())
    all_prs_file.close()

    bot_prs_full_path = path + "/botPRs.json"

    bot_prs_file = open(bot_prs_full_path, 'r')
    bot_prs = json.loads(bot_prs_file.read())
    bot_prs_file.close()

    all_bot_prs_numbers = [pr["number"] for pr in bot_prs]

    all_non_bot_prs = [pr for pr in all_prs if pr["number"] not in all_bot_prs_numbers]

    file_management.write_data(all_non_bot_prs, owner, repo, "nonBotPRs")


def do_matchings(owner, repo, bot_prs, non_bot_prs):
    do_one_to_one_matching(owner, repo, bot_prs, non_bot_prs, "OneToOne")
    do_changed_source_files_larger_matching(owner, repo, bot_prs, non_bot_prs, "ChangedSourceFilesAtLeast")
    do_performance_label_matching(owner, repo, bot_prs, non_bot_prs, "PerformanceLabels")


def do_one_to_one_matching(owner, repo, bot_prs, non_bot_prs, file_name):
    # Find one to one matchings of bot PR's and all PR's
    matchings = []
    for bot_pr in bot_prs:
        matchings.append((bot_pr, helpers.find_one_to_one(bot_pr, non_bot_prs)))

    bot_matching_prs = []
    non_bot_matching_prs = []

    for matching in matchings:
        if len(matching[1]) > 0:
            bot_matching_prs.append(matching[0])
            pr_match = matching[1][0]
            non_bot_matching_prs.append(pr_match)

            for match in matchings:
                if pr_match in match[1]:
                    match[1].remove(pr_match)

    file_management.write_data(bot_matching_prs, owner, repo, "botPRs" + file_name)
    file_management.write_data(non_bot_matching_prs, owner, repo, "nonBotPRs" + file_name)


def do_changed_source_files_larger_matching(owner, repo, bot_prs, non_bot_prs, file_name):
    at_least_source_files = [2, 4, 8]

    key = "changedSourceFiles"
    for at_least in at_least_source_files:
        changed_source_bot_prs = []
        changed_source_all_prs = []
        for pr in bot_prs:
            if key in pr and pr["closed"] and len(pr["changedSourceFiles"]) >= at_least:
                changed_source_bot_prs.append(pr)

        for pr in non_bot_prs:
            if key in pr and pr["closed"] and len(pr["changedSourceFiles"]) >= at_least:
                changed_source_all_prs.append(pr)

        file_management.write_data(changed_source_bot_prs, owner, repo, "botPRs" + file_name + str(at_least))
        file_management.write_data(changed_source_all_prs, owner, repo, "nonBotPRs" + file_name + str(at_least))


def do_performance_label_matching(owner, repo, bot_prs, non_bot_prs, file_name):
    performance_label = {
        "node": {
            "name": "performance"
        }
    }

    performance_labeled_bot_prs = [pr for pr in bot_prs if performance_label in pr["labels"]["edges"]]
    performance_labeled_all_prs = [pr for pr in non_bot_prs if performance_label in pr["labels"]["edges"]]

    file_management.write_data(performance_labeled_bot_prs, owner, repo, "botPRs" + file_name)
    file_management.write_data(performance_labeled_all_prs, owner, repo, "nonBotPRs" + file_name)
