import statistics

from src.analysis.plotting import qq_plot, top_ten
from src.analysis.hypotheses.subroutines import get_distributions, get_bot_username, categorize_data_set

def generate_participants(owner, repo, data_set):
    # Q-Q plot
    distributions = get_distributions(data_set, "benchmarkBotFreeParticipants")

    qq_plot.qq_plotting(owner, repo, data_set["name"], distributions[0], distributions[1], data_set["bot_prs_name"],
                        data_set["non_bot_prs_name"], "participants")

    # participant distribution
    participant_categorization = categorize_data_set(owner, repo, data_set, "participants")

    top_ten.create_top_ten_prs(owner, repo, data_set["name"], data_set["bot_prs"], participant_categorization[0],
                               data_set["bot_prs_name"],
                               "participants")
    top_ten.create_top_ten_prs(owner, repo, data_set["name"], data_set["non_bot_prs"], participant_categorization[1],
                               data_set["non_bot_prs_name"],
                               "participants")


def comments_printer(owner, repo, data_set, pr_type):
    # comments length distribution
    prs_total_comment_lengths_without_bot = []
    for pr in data_set[pr_type]:
        bot_indices = []
        for pair in pr["commenterAndLengths"]:
            if pair[0] != get_bot_username(owner, repo):
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

    print(
        f"{owner}/{repo}: Median comment length for {data_set['name']}: {pr_type}: "
        f"{statistics.median(prs_total_comment_lengths_without_bot)}")
    print(
        f"{owner}/{repo}: Average comment length for {data_set['name']}: {pr_type}: "
        f"{statistics.mean(prs_total_comment_lengths_without_bot)}")


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

    # comments length distribution
    comments_printer(owner, repo, data_set, "bot_prs")
    comments_printer(owner, repo, data_set, "non_bot_prs")


def generate_reviews(owner, repo, data_set):
    # number of reviews
    distributions = get_distributions(data_set, "reviews")

    qq_plot.qq_plotting(owner, repo, data_set["name"], distributions[0],
                        distributions[1],
                        data_set["bot_prs_name"],
                        data_set["non_bot_prs_name"], "reviews")

    reviews_categorized = categorize_data_set(owner, repo, data_set, "reviews")

    top_ten.create_top_ten_prs(owner, repo, data_set["name"], data_set["bot_prs"], reviews_categorized[0],
                               data_set["bot_prs_name"],
                               "reviewers")
    top_ten.create_top_ten_prs(owner, repo, data_set["name"], data_set["non_bot_prs"], reviews_categorized[1],
                               data_set["non_bot_prs_name"],
                               "reviewers")
