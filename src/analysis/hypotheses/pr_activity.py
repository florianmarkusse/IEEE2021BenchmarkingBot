import statistics
import collections

from src.analysis.plotting import qq_plot, top_ten, frequency_graph, boxplot, scatter_graph
from src.analysis.hypotheses.subroutines import get_distributions, get_bot_username, categorize_data_set, get_always, \
    get_additional_bots
from src.utility import helpers
from src.analysis.tests.MC_test import perform_mc_test

def generate_participants(owner, repo, data_set):
    # Q-Q plot
    distributions = get_distributions(data_set, "benchmarkBotFreeParticipants")

    perform_mc_test(owner, repo, data_set["name"], "# of participants", distributions[0], distributions[1])

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
        non_countable_indices = []
        if get_always(owner, repo):
            for pair in pr["commenterAndLengths"]:
                if pair[0] == get_bot_username(owner, repo) or pair[0] in get_additional_bots(owner, repo):
                    non_countable_indices.append(pr["commenterAndLengths"].index(pair))
        else:
            for pair in pr["commenterAndLengths"]:
                if pair[0] == get_bot_username(owner, repo):
                    bot_index = pr["commenterAndLengths"].index(pair)
                    non_countable_indices.append(bot_index - 1)
                    non_countable_indices.append(bot_index)
                if pair[0] in get_additional_bots(owner, repo):
                    non_countable_indices.append(pr["commenterAndLengths"].index(pair))

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
            is_always = get_always(owner, repo)
            if is_always:
                if pair[0] == get_bot_username(owner, repo) or pair[0] in get_additional_bots(owner, repo):
                    benchmark_bot_contributions += 1
            else:
                if pair[0] == get_bot_username(owner, repo):
                    benchmark_bot_contributions += (1 + 1)  # Add explicit invocation
                if pair[0] in get_additional_bots(owner, repo):
                    benchmark_bot_contributions += 1
        bot_pr_comments_distribution_without_bot_contribution.append(
            max(0, len(pr["commenterAndLengths"]) - benchmark_bot_contributions)
        )

    number_of_comments_distributions = get_distributions(data_set, "comments")

    perform_mc_test(owner, repo, data_set["name"], "# of comments",
                    bot_pr_comments_distribution_without_bot_contribution, number_of_comments_distributions[1])

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
            is_always = get_always(owner, repo)
            if is_always:
                if pair[0] == get_bot_username(owner, repo) or pair[0] in get_additional_bots(owner, repo):
                    benchmark_bot_contributions += 1
            else:
                if pair[0] == get_bot_username(owner, repo):
                    benchmark_bot_contributions += (1 + 1)  # Add explicit invocation
                if pair[0] in get_additional_bots(owner, repo):
                    benchmark_bot_contributions += 1
        result = max(0, len(pr["commenterAndLengths"]) - benchmark_bot_contributions)
        if result >= at_least:
            bot_pr_comments_distribution_without_bot_contribution.append(result)

    number_of_comments_distributions = get_distributions(data_set, "comments", at_least)

    if len(number_of_comments_distributions[1]) > 0 and len(bot_pr_comments_distribution_without_bot_contribution) > 0:
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

    perform_mc_test(owner, repo, data_set["name"], "total comment length",
                    comment_lengths_bot_prs, comment_lengths_non_bot_prs)

    divider = 1000
    comment_lengths_bot_prs = [ele / divider for ele in comment_lengths_bot_prs]
    comment_lengths_non_bot_prs = [ele / divider for ele in comment_lengths_non_bot_prs]

    qq_plot.qq_plotting(owner, repo, data_set["name"], comment_lengths_bot_prs,
                        comment_lengths_non_bot_prs,
                        data_set["bot_prs_name"],
                        data_set["non_bot_prs_name"], f"comment_lengths_X{divider}")

    frequency_graph.create_single_hist(
        owner,
        repo,
        data_set["name"],
        f"Total comment length",
        50000 / divider,
        comment_lengths_bot_prs,
        data_set["bot_prs_name"],
        comment_lengths_non_bot_prs,
        data_set["non_bot_prs_name"],
        1.0,
        2500 / divider,
        4,
        True,
        False,
        0
    )

    comments_after_benchmarking_bot_distributions = get_distributions(data_set, "commentsAfterContribution")
    number_of_comments_distributions = get_distributions(data_set, "comments")

    min_length = min(len(comments_after_benchmarking_bot_distributions[0]), len(number_of_comments_distributions[0]))

    comment_after_bb_distributions = comments_after_benchmarking_bot_distributions[0][:min_length]
    number_of_comments_bot_distributions = number_of_comments_distributions[0][:min_length]

    fraction_of_comments_after_benchmarking_contribution = []

    for index in range(len(number_of_comments_bot_distributions)):
        fraction = comment_after_bb_distributions[index] / number_of_comments_bot_distributions[index]
        fraction_of_comments_after_benchmarking_contribution.append(fraction)

    scatter_graph.scatter_graph(owner, repo, data_set["name"],
                                number_of_comments_bot_distributions,
                                fraction_of_comments_after_benchmarking_contribution,
                                "total # of comments", "Fraction remaining")

    frequency_graph.create_single_hist(
        owner,
        repo,
        data_set["name"],
        f"Fraction of comments remaining",
        1.0,
        fraction_of_comments_after_benchmarking_contribution,
        data_set["bot_prs_name"],
        None,
        None,
        0.5,
        0.1,
        1,
        False,
        False,
    )
    frequency_graph.create_single_hist(
        owner,
        repo,
        data_set["name"],
        f"Fraction of comments remaining",
        1.0,
        fraction_of_comments_after_benchmarking_contribution,
        data_set["bot_prs_name"],
        None,
        None,
        1.0,
        0.1,
        1,
        False,
        True
    )

    comments_printer(owner, repo, data_set, "bot_prs")
    comments_printer(owner, repo, data_set, "non_bot_prs")


def generate_reviews(owner, repo, data_set):
    # number of reviews
    distributions = get_distributions(data_set, "reviews")

    perform_mc_test(owner, repo, data_set["name"], "# of reviews", distributions[0], distributions[1])

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
        0.5,
        True
    )
