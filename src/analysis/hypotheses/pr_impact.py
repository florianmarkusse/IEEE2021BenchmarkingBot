from src.analysis.hypotheses.subroutines import get_distributions
from src.analysis.plotting import qq_plot


def pr_status_printer(owner, repo, data_set, pr_type):
    total_merges = 0
    total_closes = 0

    for pr in data_set[pr_type]:
        if pr["merged"]:
            total_merges += 1
        else:
            total_closes += 1

    print(f"{owner}/{repo}: # of merges for {data_set['name']}: {pr_type}: {total_merges}")
    print(f"{owner}/{repo}: # of closes for {data_set['name']}: {pr_type}: {total_closes}")
    print(
        f"{owner}/{repo}: merge/close for {data_set['name']}: {pr_type}: {total_merges / (total_closes + total_merges)}")


def generate_pr_status(owner, repo, data_set):
    # bot PR's
    pr_status_printer(owner, repo, data_set, "bot_prs")
    # non-bot PR's
    pr_status_printer(owner, repo, data_set, "non_bot_prs")


def generate_commits(owner, repo, data_set):
    distributions = get_distributions(data_set, "commits")

    qq_plot.qq_plotting(owner, repo, data_set["name"], distributions[0], distributions[1], data_set["bot_prs_name"],
                        data_set["non_bot_prs_name"], "commits")
