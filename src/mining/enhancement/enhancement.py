from src.analysis.hypotheses import subroutines


def add_human_comments_member(prs):
    for pr in prs:
        pr["comments"] = len(pr["commenterAndLengths"])
        pr["humanComments"] = pr["comments"] - (len(pr["callers"]) * 2)


def add_benchmark_bot_free_participants_member(owner, repo, prs):
    botUserName = subroutines.get_bot_username(owner, repo)
    for pr in prs:
        if botUserName in pr["participants"]:
            pr["benchmarkBotFreeParticipants"] = len(pr["participants"]) - 1
        else:
            pr["benchmarkBotFreeParticipants"] = len(pr["participants"])


def add_comments_after_benchmarking_bot_contribution(owner, repo, prs):
    botUserName = subroutines.get_bot_username(owner, repo)
    for pr in prs:
        after_benchmark_contribution_count = 0
        benchmark_bot_contributed = False
        for comment in pr["commenterAndLengths"]:
            if benchmark_bot_contributed:
                after_benchmark_contribution_count += 1
            if botUserName in comment[0]:
                benchmark_bot_contributed = True
        pr["commentsAfterContribution"] = after_benchmark_contribution_count
