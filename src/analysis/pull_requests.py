from src.analysis import data_printer
from src.analysis.plotting import combo, frequency_graph, scatter_graph, pie, boxplot
from src.utility.helpers import periodize_prs, categorize_prs, get_date_from_string
from src.analysis.helpers import split_prs_into_lists
from statistics import mean, median


def monthly_analysis(owner, repo, all_prs, bot_prs):
    """
    Perform a monthly analysis on the repository based on the PR's that were created and those that contain a bot
    contribution.

    Parameters
    ----------
    owner : The owner of the repository.
    repo : The name of the repository.
    all_prs : All the PR's of this repository.
    bot_prs : All the PR's that contain a bot contribution of this repository.

    Returns
    -------
    A dictionary where each entry is a period that contains PR data from that repository in that specific period.
    """
    all_prs_per_month = periodize_prs(all_prs, "%m-%y")
    all_bot_prs_per_month = periodize_prs(bot_prs, "%m-%y")

    period_summaries = []

    for period in all_prs_per_month:
        period_summary = {
            "period": period,
            "all_prs": len(all_prs_per_month[period]),
            "bot_prs": len(all_bot_prs_per_month[period]) if period in all_bot_prs_per_month else 0,
        }

        period_summary["fraction"] = period_summary["bot_prs"] / period_summary["all_prs"]

        period_summaries.append(period_summary)

    # Print summarizing data for the PR's in the data.
    data_printer.print_project_prs_data(owner, repo, len(all_prs), len(bot_prs), period_summaries)

    # Create periodized combo chart for PR's with bot contribution and without bot contribution.
    combo.combo_period_analysis(owner, repo, period_summaries)

    return period_summaries


def contributor_analysis(owner, repo, all_prs, bot_prs):
    """
    Perform a user analysis on the repository based on the PR's that were created and those that contain a bot
    contribution.

    Parameters
    ----------
    owner : The owner of the repository.
    repo : The name of the repository.
    all_prs : All the PR's of this repository.
    bot_prs : All the PR's that contain a bot contribution of this repository.

    Returns
    -------
    A dictionary where each entry is a contributor that contains PR data from that repository from that contributor.
    """
    all_prs_per_user = categorize_prs(all_prs, "author", "login")
    bot_prs_per_user = categorize_prs(bot_prs, "author", "login")
    bot_prs_per_caller = categorize_prs(bot_prs, "callers")

    user_summaries = []

    for user in all_prs_per_user:
        user_summary = {
            "user": user,
            "all_prs": len(all_prs_per_user[user]),
            "bot_prs": len(bot_prs_per_user[user]) if user in bot_prs_per_user else 0,
            "bot_calls": len(bot_prs_per_caller[user]) if user in bot_prs_per_caller else 0,
        }

        if user in bot_prs_per_user:
            user_summary["last_bot_pr_created"] = \
                str(get_date_from_string(bot_prs_per_user[user][len(bot_prs_per_user[user]) - 1]["createdAt"]).date())
        else:
            user_summary["last_bot_pr_created"] = "N/A"

        user_summary["fraction"] = user_summary["bot_prs"] / user_summary["all_prs"]
        user_summary["bot_calls_fraction"] = user_summary["bot_calls"] / user_summary["all_prs"]

        user_summaries.append(user_summary)

    # Create scatter plot for contributors having PR's where the bot contributes.
    for cut_off in [0, 10, 50, 100]:
        x_label = "Fraction of PR's with bot contribution"
        y_label = "Number of created PR's"
        scatter_graph.scatter_graph(owner, repo, user_summaries, cut_off, 0.0, 1.0, "fraction", "all_prs", x_label,
                                    y_label)

    significance = 5

    contributors_without_bot_calls = [user_summary for user_summary in user_summaries if user_summary["bot_calls"] == 0]
    contributors_with_bot_calls = [user_summary for user_summary in user_summaries if user_summary["bot_calls"] > 0]

    significant_contributors_without_bot_calls = [user_summary for user_summary in contributors_without_bot_calls if
                                                  user_summary["all_prs"] >= significance]
    significant_contributors_with_bot_calls = [user_summary for user_summary in contributors_with_bot_calls if
                                               user_summary["all_prs"] >= significance]

    pie.pie_chart(owner, repo, ["without bot call(s)", "with bot calls"], ["tab:red", "tab:green"],
                  [len(contributors_without_bot_calls), len(contributors_with_bot_calls)], (0, 0),
                  "Percentage_of_contributors_calling_benchmarking_bot")

    pie.pie_chart(owner, repo, ["without bot call(s)", "with bot calls"], ["tab:red", "tab:green"],
                  [len(significant_contributors_without_bot_calls), len(significant_contributors_with_bot_calls)],
                  (0, 0),
                  "Percentage_of_significant_5_contributors_calling_benchmarking_bot")

    bot_calls_frequencies = [contributor["bot_calls"] for contributor in contributors_with_bot_calls]

    frequency_graph.frequency_analysis(owner, repo, "bot_PRs",
                                       bot_calls_frequencies,
                                       "Contributors having called the benchmarking bot",
                                       [50])

    boxplot.boxplot(owner, repo, bot_calls_frequencies, "benchmark_bot_calls")

    upper_half = [frequency for frequency in bot_calls_frequencies if frequency >= median(bot_calls_frequencies)]
    top_25 = [frequency for frequency in upper_half if frequency >= median(upper_half)]

    scatter_graph.scatter_graph(owner, repo, [contributor for contributor in contributors_with_bot_calls], 99, 0.0, 1.0,
                                "bot_calls_fraction", "all_prs",
                                "Fraction of benchmark bot calls compared to the number of created PR's",
                                "Number of created PR's")
    scatter_graph.scatter_graph(owner, repo, [contributor for contributor in contributors_with_bot_calls if
                                              contributor["bot_calls"] > min(top_25)], 100,
                                0.0, 1.0,
                                "bot_calls_fraction", "all_prs",
                                "Fraction of benchmark bot calls compared to the number of created PR's",
                                "Number of created PR's")

    # Print the data for contributors' odds of having another PR where the bot contributes.
    # data_printer.print_again_interaction_with_bot(user_summaries, "bot_prs", 20, "interaction(s)")

    # Print the data for contributors with the amount of PR's they created with and without bot contribution.
    # data_printer.print_contributor_created_prs_bot_interaction(user_summaries)

    return user_summaries


def pr_activity_analysis(owner, repo, prs, pr_type):
    """
    Perform an activity analysis on the PR's of the repository.

    Parameters
    ----------
    owner : The owner of the repository.
    repo : The name of the repository.
    prs : The PR's to perform the activity analysis on.
    pr_type : he type of PR's where this is about (e.g. this can be about "bot_PRs")

    Returns
    -------
    A summary of the activity in the PR's supplied with @prs.
    """

    variables = split_prs_into_lists(prs)

    # Create frequency bar charts for the different types of activity in PR's
    frequency_graph.frequency_analysis(owner, repo, pr_type, variables["number_of_comments"], "Comments per PR",
                                       [40, 60])
    frequency_graph.frequency_analysis(owner, repo, pr_type, variables["number_of_participants"], "Participants per PR",
                                       [20])
    frequency_graph.frequency_analysis(owner, repo, pr_type, variables["number_of_reviews"], "Reviews per PR", [10])
    frequency_graph.frequency_analysis(owner, repo, pr_type, variables["number_of_commits"], "Commits per PR", [10])

    return {
        "average_comments": mean(variables["number_of_comments"]),
        "median_comments": median(variables["number_of_comments"]),
        "average_participants": mean(variables["number_of_participants"]),
        "median_participants": median(variables["number_of_participants"]),
        "average_reviews": mean(variables["number_of_reviews"]),
        "median_reviews": median(variables["number_of_reviews"]),
        "average_commits": mean(variables["number_of_commits"]),
        "median_commits": median(variables["number_of_commits"])
    }
