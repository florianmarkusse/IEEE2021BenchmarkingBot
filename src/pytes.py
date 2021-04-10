from utility import file_management, helpers

from src.mining.enhancement import enhancement

# Get projects to collect PR data for
projects = file_management.get_projects_to_mine()

# Get token for GitHub API
token = file_management.get_token()

for project in projects:
    owner = project.get("owner")
    repo = project.get("repo")
    bot_query = project.get("botQuery")
    start_date = project.get("startDate")
    bot_call_string = project.get("botCallString")

    prs = file_management.get_mined_prs(owner, repo)
    bot_prs = prs.get("bot_prs")
    all_prs = prs.get("all_prs")

    matchings = []
    timer = 0
    for bot_pr in bot_prs:
        timer += 1
        matchings.append((bot_pr, helpers.find_one_to_one(bot_pr, all_prs)))
        if timer % 50 == 0 or timer == len(bot_prs):
            print(f"got {timer} out of {len(bot_prs)}")

    print(len(bot_prs))
    print(len(matchings))

    bot_matching_prs = []
    non_bot_matching_prs = []
    total_matches = 0

    for matching in matchings:
        total_matches += 1

        if len(matching[1]) > 0:
            bot_matching_prs.append(matching[0])
            pr_match = matching[1][0]
            non_bot_matching_prs.append(pr_match)

            for match in matchings:
                if pr_match in match[1]:
                    match[1].remove(pr_match)



    print(f"Got a total of {total_matches} matches")
    print(f"Assignment resulted in {len(bot_matching_prs)}/{len(non_bot_matching_prs)} out of {total_matches} total")

    file_management.write_data(bot_matching_prs, owner, repo, "botPRsMatching")
    file_management.write_data(non_bot_matching_prs, owner, repo, "nonBotPRsMatching")
