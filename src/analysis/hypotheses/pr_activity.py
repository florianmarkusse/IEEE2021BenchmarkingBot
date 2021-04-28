import statistics
import collections

from src.analysis.plotting import qq_plot, top_ten, frequency_graph, boxplot
from src.analysis.hypotheses.subroutines import get_distributions, get_bot_username, categorize_data_set
from src.utility import helpers


def generate_participants(owner, repo, data_set):
    # Q-Q plot
    distributions = get_distributions(data_set, "benchmarkBotFreeParticipants")

    qq_plot.qq_plotting(owner, repo, data_set["name"], distributions[0], distributions[1], data_set["bot_prs_name"],
                        data_set["non_bot_prs_name"], "participants")

    # Histogram
    frequency_graph.create_overlapping_histogram(
        owner,
        repo,
        data_set["name"],
        "Number of participants",
        15,
        distributions[0],
        data_set["bot_prs_name"],
        distributions[1],
        data_set["non_bot_prs_name"],
        0.4,
        True
    )

    at_least = 3

    distributions = get_distributions(data_set, "benchmarkBotFreeParticipants", at_least)

    qq_plot.qq_plotting(owner, repo, data_set["name"], distributions[0], distributions[1], data_set["bot_prs_name"],
                        data_set["non_bot_prs_name"], f"participants at least {at_least}")

    # Histogram
    frequency_graph.create_overlapping_histogram(
        owner,
        repo,
        data_set["name"],
        f"Number of participants at least {at_least}",
        15,
        distributions[0],
        data_set["bot_prs_name"],
        distributions[1],
        data_set["non_bot_prs_name"],
        0.5,
        True
    )


def get_total_comment_lengths_without_bot_contribution(owner, repo, data_set, pr_type):
    # comments length distribution
    prs_total_comment_lengths_without_bot = []
    for pr in data_set[pr_type]:
        bot_indices = []
        for pair in pr["commenterAndLengths"]:
            if pair[0] == get_bot_username(owner, repo):
                bot_indices.append(pr["commenterAndLengths"].index(pair))
        non_countable_indices = []
        for index in bot_indices:
            non_countable_indices.append(index - 1)
            non_countable_indices.append(index)

        total_length = 0

        for index, pair in enumerate(pr["commenterAndLengths"]):
            if index not in non_countable_indices:
                total_length += pair[1]

        prs_total_comment_lengths_without_bot.append(total_length)

    return prs_total_comment_lengths_without_bot


def comments_printer(owner, repo, data_set, pr_type):
    comment_lengths = get_total_comment_lengths_without_bot_contribution(owner, repo, data_set, pr_type)

    print(
        f"{owner}/{repo}: Median total comment length for {data_set['name']}: {pr_type}: "
        f"{statistics.median(comment_lengths)}")
    print(
        f"{owner}/{repo}: Average total comment length for {data_set['name']}: {pr_type}: "
        f"{statistics.mean(comment_lengths)}")


def generate_comments(owner, repo, data_set):
    # number of comments

    # get_distributions does not work correctly for bot PR's as benchmarking bot can also comment on the PR. This would
    # inflate the actual number of human contributions.
    bot_pr_comments_distribution_without_bot_contribution = []
    for pr in data_set["bot_prs"]:
        benchmark_bot_contributions = 0
        for pair in pr["commenterAndLengths"]:
            if pair[0] == get_bot_username(owner, repo):
                benchmark_bot_contributions += 1
        bot_pr_comments_distribution_without_bot_contribution.append(
            max(0, len(pr["commenterAndLengths"]) - (2 * benchmark_bot_contributions))
        )

    number_of_comments_distributions = get_distributions(data_set, "comments")

    qq_plot.qq_plotting(owner, repo, data_set["name"], bot_pr_comments_distribution_without_bot_contribution,
                        number_of_comments_distributions[1],
                        data_set["bot_prs_name"],
                        data_set["non_bot_prs_name"], "comments")

    frequency_graph.create_overlapping_histogram(
        owner,
        repo,
        data_set["name"],
        "Number of comments",
        40,
        bot_pr_comments_distribution_without_bot_contribution,
        data_set["bot_prs_name"],
        number_of_comments_distributions[1],
        data_set["non_bot_prs_name"],
        0.4,
        True,
        5,
        False
    )

    at_least = 5

    bot_pr_comments_distribution_without_bot_contribution = []
    for pr in data_set["bot_prs"]:
        benchmark_bot_contributions = 0
        for pair in pr["commenterAndLengths"]:
            if pair[0] == get_bot_username(owner, repo):
                benchmark_bot_contributions += 1
        result = max(0, len(pr["commenterAndLengths"]) - (2 * benchmark_bot_contributions))
        if result >= at_least:
            bot_pr_comments_distribution_without_bot_contribution.append(result)

    number_of_comments_distributions = get_distributions(data_set, "comments", at_least)

    qq_plot.qq_plotting(owner, repo, data_set["name"], bot_pr_comments_distribution_without_bot_contribution,
                        number_of_comments_distributions[1],
                        data_set["bot_prs_name"],
                        data_set["non_bot_prs_name"], f"comments at least {at_least}")

    frequency_graph.create_overlapping_histogram(
        owner,
        repo,
        data_set["name"],
        f"Number of comments at least {at_least}",
        40,
        bot_pr_comments_distribution_without_bot_contribution,
        data_set["bot_prs_name"],
        number_of_comments_distributions[1],
        data_set["non_bot_prs_name"],
        0.4,
        True,
        5,
        False
    )

    # comments length distribution
    comment_lengths_bot_prs = get_total_comment_lengths_without_bot_contribution(owner, repo, data_set, "bot_prs")
    comment_lengths_non_bot_prs = get_total_comment_lengths_without_bot_contribution(owner, repo, data_set,
                                                                                     "non_bot_prs")

    qq_plot.qq_plotting(owner, repo, data_set["name"], comment_lengths_bot_prs,
                        comment_lengths_non_bot_prs,
                        data_set["bot_prs_name"],
                        data_set["non_bot_prs_name"], "comment_lengths")

    frequency_graph.create_overlapping_histogram_step(
        owner,
        repo,
        data_set["name"],
        "Total comment length",
        50000,
        comment_lengths_bot_prs,
        data_set["bot_prs_name"],
        comment_lengths_non_bot_prs,
        data_set["non_bot_prs_name"],
        1.0,
        2500,
        4
    )

    comments_after_benchmarking_bot_distributions = get_distributions(data_set, "commentsAfterContribution")

    fraction_of_comments_after_benchmarking_contriubiton = []

    for index in range(len(number_of_comments_distributions[0])):
        fraction = comments_after_benchmarking_bot_distributions[0][index] / number_of_comments_distributions[0][index]
        fraction_of_comments_after_benchmarking_contriubiton.append(fraction)



    frequency_graph.create_overlapping_histogram_step(
        owner,
        repo,
        data_set["name"],
        f"Fraction of comments remaining",
        0.9,
        fraction_of_comments_after_benchmarking_contriubiton,
        data_set["bot_prs_name"],
        None,
        None,
        0.4,
        0.1,
        1
    )

    comments_printer(owner, repo, data_set, "bot_prs")
    comments_printer(owner, repo, data_set, "non_bot_prs")


def generate_reviews(owner, repo, data_set):
    # number of reviews
    distributions = get_distributions(data_set, "reviews")

    qq_plot.qq_plotting(owner, repo, data_set["name"], distributions[0],
                        distributions[1],
                        data_set["bot_prs_name"],
                        data_set["non_bot_prs_name"], "reviews")

    reviews_categorized = categorize_data_set(owner, repo, data_set, "reviewers")

    # Histogram
    frequency_graph.create_overlapping_histogram(
        owner,
        repo,
        data_set["name"],
        "Number of reviews",
        60,
        distributions[0],
        data_set["bot_prs_name"],
        distributions[1],
        data_set["non_bot_prs_name"],
        0.4,
        True
    )


def generate_benchmarking_bot_callers(owner, repo, data_set):

    caller_to_prs = helpers.categorize_prs(data_set["bot_prs"], "callers")

    caller_frequencies = []
    for key in caller_to_prs:
        caller_frequencies.append(len(caller_to_prs[key]))

    result = boxplot.boxplot(owner, repo, data_set["name"], caller_frequencies, "benchmark_bot_calls")

    outlier_values = []
    for ele in result["fliers"]:
        for outlier in ele.get_data()[1]:
            outlier_values.append(outlier)

    frequency_graph.create_overlapping_histogram(
        owner,
        repo,
        data_set["name"],
        "Benchmark bot calls",
        min(outlier_values),
        caller_frequencies,
        "Contributors",
        None,
        None,
        0.4,
        True,
        20,
        False,
        True
    )
    # print(data_set["name"])
    # print(len(caller_to_prs.keys()))
    # print(list(caller_to_prs.keys())[0])
    # print(len(caller_to_prs[list(caller_to_prs.keys())[0]]))
