def print_again_interaction_with_bot(summaries, member, max_range, value):
    """
    Prints the table of odds of seeing the bot again in a PR for a contributor.
    A row would for example be:
    Odds of going from 3 interaction(s) to 4 interaction(s): 0.8 50 40

    Parameters
    ----------
    summaries : The dictionary that contains the member whose odds of happening again are to be calculated.
    member : The member to look for in each entry of @summaries.
    max_range : To how many interactions the table should calculate the odds for.
    value : The string value that represents the action.

    Returns
    -------
    """
    for i in range(max_range):
        previous = len([summary for summary in summaries if summary[member] >= i])
        again = len([summary for summary in summaries if summary[member] >= i + 1])

        again_fraction = '%.3f' % (again / previous)

        print(f"Odds of going from {i} {value} to {i + 1} {value}:\t{again_fraction}\t{previous}\t{again}")


def print_contributor_created_prs_bot_interaction(user_summaries):
    """
    Prints for each contributor how many PR's they created and what fraction of these PR's contains a bot contribution.

    Parameters
    ----------
    user_summaries : The dictionary containing all the contributors. Each of the entries in this dictionary is assumed
    to have the following members:
        "user": The username of the contributor.
        "bot_prs": The number of PR's they created that contains a bot contribution.
        "last_bot_pr_created": When they last created a PR that contains a bot contribution.
        "all_prs": The number of PR's they created.
        "fraction": The fraction of the PR's with bot contribution out of all the PR's they created.

    Returns
    -------
    """
    print("Contributor\tBot PR's\tLast bot PR created\tNon-bot PR's\tFraction\tTotal PR's")
    for user_summary in user_summaries:
        print("{user}\t{bot_prs}\t{last_bot_pr_created}\t{non_bot_prs}\t{fraction}\t{all_prs}".format(
            user=user_summary["user"],
            bot_prs=user_summary["bot_prs"],
            last_bot_pr_created=user_summary["last_bot_pr_created"],
            non_bot_prs=user_summary["all_prs"] - user_summary["bot_prs"],
            fraction=user_summary["fraction"],
            all_prs=user_summary["all_prs"],
        ))


def print_project_prs_data(owner, repo, all_prs_number, bot_prs_number, period_summaries):
    """
    Prints the data that is calculated for the PR's of the project.

    Parameters
    ----------
    owner : The owner of the repository.
    repo : The name of the repository.
    all_prs_number : The total number of PR's created for this repository.
    bot_prs_number : The total number of PR's created that contains a bot contribution for this repository.
    period_summaries : The dictionary that contains the data for the PR's in this repository per a period.

    Returns
    -------
    """
    print_project_prs_bot_summary(owner, repo, all_prs_number, bot_prs_number)
    print_project_prs_period(period_summaries)


def print_project_prs_bot_summary(owner, repo, all_prs_number, bot_prs_number):
    """
    Print a summary of the PR's for this repository with regard to bot contribution.

    Parameters
    ----------
    owner : The owner of the repository.
    repo : The name of the repository.
    all_prs_number : The total number of PR's created for this repository.
    bot_prs_number : The total number of PR's created that contains a bot contribution for this repository.

    Returns
    -------
    """
    print("Project\tBot PR's\tNon-bot PR's\tFraction\tTotal PR's")
    print("{owner}/{repo}\t{bot_prs}\t{non_bot_prs}\t{fraction}\t{total_prs}\n".format(
        owner=owner,
        repo=repo,
        bot_prs=bot_prs_number,
        non_bot_prs=all_prs_number - bot_prs_number,
        fraction=bot_prs_number / all_prs_number,
        total_prs=all_prs_number
    ))


def print_project_prs_period(period_summaries):
    """
    Print the PR data for this repository on a periodic basis with regard to bot contribution.

    Parameters
    ----------
    period_summaries : The dictionary that contains the data for the PR's in this repository per a period.

    Returns
    -------
    """
    print("Period\tBot PR's\tNon-bot PR's\tFraction\tTotal PR's")
    for period_summary in period_summaries:
        print("{period}\t{bot_prs}\t{non_bot_prs}\t{fraction}\t{all_prs}".format(
            period=period_summary["period"],
            bot_prs=period_summary["bot_prs"],
            non_bot_prs=period_summary["all_prs"] - period_summary["bot_prs"],
            fraction=period_summary["fraction"],
            all_prs=period_summary["all_prs"],
        ))