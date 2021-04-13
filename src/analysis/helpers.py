def get_graph_path(owner, repo):
    """
    Gets the path to the repository's graph folder.

    Parameters
    ----------
    owner : The owner of the repository.
    repo : The name of the repository.

    Returns
    -------
    The path to get to a repository's graph folder.
    """
    return f"../data/projects/{owner}/{repo}/images/graphs"


def split_prs_into_lists(prs, remove_bot_contribution=True):
    number_of_comments = []
    number_of_participants = []
    number_of_reviews = []
    number_of_commits = []

    for pr in prs:
        if remove_bot_contribution and "humanComments" in pr:
            number_of_comments.append(pr["humanComments"])
        else:
            number_of_comments.append(pr["comments"])
        if remove_bot_contribution and "benchmarkBotFreeParticipants" in pr:
            number_of_participants.append(pr["benchmarkBotFreeParticipants"])
        else:
            number_of_participants.append(pr["participants"])
        number_of_reviews.append(pr["reviews"])
        number_of_commits.append(pr["commits"])

    return {
        "number_of_comments": number_of_comments,
        "number_of_participants": number_of_participants,
        "number_of_reviews": number_of_reviews,
        "number_of_commits": number_of_commits
    }
