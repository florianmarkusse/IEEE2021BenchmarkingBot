def add_human_comments_member(prs):
    for pr in prs:
        pr["humanComments"] = pr["comments"] - (len(pr["callers"]) * 2)


def add_benchmark_bot_free_participants_member(prs):
    for pr in prs:
        pr["benchmarkBotFreeParticipants"] = len(pr["participants"]) - 1
