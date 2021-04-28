from src.analysis.hypotheses.subroutines import get_distributions
from src.analysis.plotting import qq_plot, frequency_graph
from src.utility import helpers
import statistics


def pr_status_printer(owner, repo, data_set, pr_type):
    total_merges = 0
    total_closes = 0

    days_until_merged_or_closed = []

    for pr in data_set[pr_type]:
        date_created = helpers.get_date_from_string(pr["createdAt"])
        date_closed = helpers.get_date_from_string(pr["closedAt"])
        time_opened = date_closed - date_created
        days_until_merged_or_closed.append(time_opened.seconds / (24 * 60 * 60))
        if pr["merged"]:
            total_merges += 1
        else:
            total_closes += 1

    print(f"{owner}/{repo}: # of merges for {data_set['name']}: {pr_type}: {total_merges}")
    print(f"{owner}/{repo}: # of closes for {data_set['name']}: {pr_type}: {total_closes}")
    print(
        f"{owner}/{repo}: merge probability for PR opened for {data_set['name']}: {pr_type}: {total_merges / (total_closes + total_merges)}")
    print(
        f"{owner}/{repo}: Median days opened until merged/closed for {data_set['name']}: {pr_type}: "
        f"{statistics.median(days_until_merged_or_closed)}")
    print(
        f"{owner}/{repo}: Average days opened until merged/closed for {data_set['name']}: {pr_type}: "
        f"{statistics.mean(days_until_merged_or_closed)}")


def generate_pr_status(owner, repo, data_set):
    # bot PR's
    pr_status_printer(owner, repo, data_set, "bot_prs")
    # non-bot PR's
    pr_status_printer(owner, repo, data_set, "non_bot_prs")


def generate_commits(owner, repo, data_set):
    distributions = get_distributions(data_set, "commits")

    qq_plot.qq_plotting(owner, repo, data_set["name"], distributions[0], distributions[1],
                        data_set["bot_prs_name"],
                        data_set["non_bot_prs_name"], "Number of commits")

    # Histogram
    frequency_graph.create_overlapping_histogram(
        owner,
        repo,
        data_set["name"],
        "Number of commits",
        60,
        distributions[0],
        data_set["bot_prs_name"],
        distributions[1],
        data_set["non_bot_prs_name"],
        0.6,
        True
    )

    at_most = 200

    x_dist = [commit for commit in distributions[0] if commit <= at_most]
    y_dist = [commit for commit in distributions[1] if commit <= at_most]

    qq_plot.qq_plotting(owner, repo, data_set["name"], x_dist, y_dist,
                        data_set["bot_prs_name"],
                        data_set["non_bot_prs_name"], f"Number of commits at most {at_most}")

    at_least = 3

    distributions = get_distributions(data_set, "commits", at_least)

    qq_plot.qq_plotting(owner, repo, data_set["name"], distributions[0], distributions[1],
                        data_set["bot_prs_name"],
                        data_set["non_bot_prs_name"], f"Number of commits at least {at_least}")

    x_dist = [commit for commit in distributions[0] if commit <= at_most]
    y_dist = [commit for commit in distributions[1] if commit <= at_most]

    qq_plot.qq_plotting(owner, repo, data_set["name"], x_dist, y_dist,
                        data_set["bot_prs_name"],
                        data_set["non_bot_prs_name"], f"Number of commits at least {at_least} at most {at_most}")


def source_files_changed_printer(owner, repo, data_set, pr_type):
    source_files_changed = []

    for pr in data_set[pr_type]:
        if "changedSourceFiles" in pr:
            source_files_changed.append(len(pr["changedSourceFiles"]))

    print(
        f"{owner}/{repo}: Median source files changed length for {data_set['name']}: {pr_type}: "
        f"{statistics.median(source_files_changed)}")
    print(
        f"{owner}/{repo}: Average source files changed length for {data_set['name']}: {pr_type}: "
        f"{statistics.mean(source_files_changed)}")


def generate_source_files_changed(owner, repo, data_set):
    source_files_changed_printer(owner, repo, data_set, "bot_prs")
    source_files_changed_printer(owner, repo, data_set, "non_bot_prs")


def additions_deletions_printer(owner, repo, data_set, pr_type):
    additions = []
    deletions = []

    for pr in data_set[pr_type]:
        additions.append(pr["additions"])
        deletions.append(pr["deletions"])

    print(
        f"{owner}/{repo}: Median additions for {data_set['name']}: {pr_type}: "
        f"{statistics.median(additions)}")
    print(
        f"{owner}/{repo}: Average additions for {data_set['name']}: {pr_type}: "
        f"{statistics.mean(additions)}")

    print(
        f"{owner}/{repo}: Median deletions for {data_set['name']}: {pr_type}: "
        f"{statistics.median(deletions)}")
    print(
        f"{owner}/{repo}: Average deletions for {data_set['name']}: {pr_type}: "
        f"{statistics.mean(deletions)}")


def generate_additions_deletions(owner, repo, data_set):
    additions_deletions_printer(owner, repo, data_set, "bot_prs")
    additions_deletions_printer(owner, repo, data_set, "non_bot_prs")
