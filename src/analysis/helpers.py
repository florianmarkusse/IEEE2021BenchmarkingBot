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
