import scipy.stats


def perform_mc_test(owner, repo, name, metric, x, y):
    result = scipy.stats.mannwhitneyu(x, y, True, "two-sided")
    print(f"{owner}/{repo}, dataset: {name} for metric: {metric}")
    print(f"Statistic: {result[0]}, p-value: {result[1]}")
