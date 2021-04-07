def add_human_comments_member(prs):
    for pr in prs:
        if "humanComments" not in pr:
            pr["humanComments"] = {}
        pr["humanComments"]["totalCount"] = pr["comments"]["totalCount"] - (len(pr["callers"]) * 2)


def add_benchmark_bot_free_participants_member(prs):
    for pr in prs:
        if "benchmarkBotFreeParticipants" not in pr:
            pr["benchmarkBotFreeParticipants"] = {}
        pr["benchmarkBotFreeParticipants"]["totalCount"] = pr["participants"]["totalCount"] - 1
