import scipy.stats
from src.utility import file_management


def perform_mc_test(owner, repo, name, metric, x, y):
    result = scipy.stats.mannwhitneyu(x, y, True, "two-sided")
    print(f"{owner}/{repo}, dataset: {name} for metric: {metric}")
    print(f"Statistic: {result[0]}, p-value: {result[1]}")
    common_language_effect_size = result[0] / (len(x) * len(y))
    print(f"effect size is: {common_language_effect_size}")

    test_result = {
        "U-statistic": result[0],
        "p-value": result[1],
        "CL effect size": common_language_effect_size
    }

    file_management.write_data(test_result, owner, repo, f"{name}_{metric}")