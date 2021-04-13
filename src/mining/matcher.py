from src.utility import helpers, file_management


def do_matchings(owner, repo, bot_prs, all_prs):
    do_one_to_one_matching(owner, repo, bot_prs, all_prs, "OneToOne")
    do_changed_source_files_larger_matching(owner, repo, bot_prs, all_prs, "ChangedSourceFilesLargerThanOne")
    do_performance_label_matching(owner, repo, bot_prs, all_prs, "PerformanceLabels")


def do_one_to_one_matching(owner, repo, bot_prs, all_prs, file_name):
    # Find one to one matchings of bot PR's and all PR's
    matchings = []
    for bot_pr in bot_prs:
        matchings.append((bot_pr, helpers.find_one_to_one(bot_pr, all_prs)))

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
    file_management.write_data(non_bot_matching_prs, owner, repo, "botPRs" + file_name)


def do_changed_source_files_larger_matching(owner, repo, bot_prs, all_prs, file_name):
    changed_source_bot_prs = []
    changed_source_all_prs = []

    for pr in bot_prs:
        if pr["closed"] and len(pr["changedSourceFiles"]) > 1:
            changed_source_bot_prs.append(pr)

    for pr in all_prs:
        if pr["closed"] and len(pr["changedSourceFiles"]) > 1:
            changed_source_all_prs.append(pr)

    file_management.write_data(changed_source_bot_prs, owner, repo, "botPRs" + file_name)
    file_management.write_data(changed_source_all_prs, owner, repo, "botPRs" + file_name)


def do_performance_label_matching(owner, repo, bot_prs, all_prs, file_name):
    performance_label = {
        "node": {
            "name": "performance"
        }
    }

    performance_labeled_bot_prs = []
    performance_labeled_all_prs = []

    for pr in bot_prs:
        if pr["closed"] and performance_label in pr["labels"]["edges"]:
            performance_labeled_bot_prs.append(pr)

    for pr in all_prs:
        if pr["closed"] and performance_label in pr["labels"]["edges"]:
            performance_labeled_all_prs.append(pr)

    file_management.write_data(performance_labeled_bot_prs, owner, repo, "botPRs" + file_name)
    file_management.write_data(performance_labeled_all_prs, owner, repo, "botPRs" + file_name)

    return {
        "bot_prs": performance_labeled_bot_prs,
        "non_bot_prs": performance_labeled_all_prs
    }