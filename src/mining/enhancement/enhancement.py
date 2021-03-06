from src.analysis.hypotheses import subroutines


def add_human_comments_member(owner, repo, prs):
    for pr in prs:
        pr["comments"] = len(pr["commenterAndLengths"])
        if subroutines.get_always(owner, repo):
            pr["callers"] = []
        counter = 0
        counter += len(pr["callers"]) * 2
        for comment in pr["commenterAndLengths"]:
            if subroutines.get_always(owner, repo):
                if comment[0] == subroutines.get_bot_username(owner, repo) or comment[0] in subroutines.get_additional_bots(owner, repo):
                    counter += 1
            else:
                if comment[0] in subroutines.get_additional_bots(owner, repo):
                    counter += 1
        pr["humanComments"] = pr["comments"] - counter


def add_benchmark_bot_free_participants_member(owner, repo, prs):
    botUserName = subroutines.get_bot_username(owner, repo)
    if subroutines.get_always(owner, repo):
        other_bots = subroutines.get_additional_bots(owner, repo)
        for pr in prs:
            counter = 0
            for participant in pr["participants"]:
                if participant == botUserName or participant in other_bots:
                    counter += 1
            pr["benchmarkBotFreeParticipants"] = len(pr["participants"]) - counter
    else:
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


def delete_element(list_object, pos):
    """Delete element from list at given index
     position (pos) """
    if pos < len(list_object):
        list_object.pop(pos)

def fix_additionalbots(owner, repo, additional_bots, prs):
    for pr in prs:
        indices_to_remove = []
        for i in range(len(pr["commenterAndLengths"])):
            if pr["commenterAndLengths"][i][0] in additional_bots:
                indices_to_remove.append(i)
        for index in indices_to_remove:
            delete_element(pr["commenterAndLengths"], index)

    for pr in prs:
        indices_to_remove = []
        for i in range(len(pr["participants"])):
            if pr["participants"][i] in additional_bots:
                indices_to_remove.append(i)
        for index in indices_to_remove:
            delete_element(pr["participants"], index)

    for pr in prs:
        pr["comments"] = len(pr["commenterAndLengths"])

    add_human_comments_member(owner, repo, prs)
    add_benchmark_bot_free_participants_member(owner, repo, prs)
    add_comments_after_benchmarking_bot_contribution(owner, repo, prs)

    return prs