from src.analysis.hypotheses import subroutines


def add_human_comments_member(prs):
    for pr in prs:
        pr["comments"] = len(pr["commenterAndLengths"])
        pr["humanComments"] = pr["comments"] - (len(pr["callers"]) * 2)


def add_benchmark_bot_free_participants_member(owner, repo, prs):
    for pr in prs:
        botUserName = subroutines.get_bot_username(owner, repo)
        if botUserName in pr["participants"]:
            pr["benchmarkBotFreeParticipants"] = len(pr["participants"]) - 1
        else:
            pr["benchmarkBotFreeParticipants"] = len(pr["participants"])
