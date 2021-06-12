import scipy.stats
from src.utility import file_management
import statistics


def perform_mc_test(owner, repo, name, metric, x, y):
    result = scipy.stats.mannwhitneyu(x, y, True, "two-sided")
    print(f"{owner}/{repo}, dataset: {name} for metric: {metric}")
    print(f"Statistic: {result[0]}, p-value: {result[1]}")
    common_language_effect_size = result[0] / (len(x) * len(y))
    print(f"effect size is: {common_language_effect_size}")

    control_std = scipy.stats.tstd(y)

    glass_delta = (scipy.stats.tmean(x) - scipy.stats.tmean(y)) / control_std
    cliffs_effect, cliffs_size = cliffsDelta(x, y)

    test_result = {
        "U-statistic": result[0],
        "p-value": result[1],
        "CL": common_language_effect_size,
        "Glass' Delta": glass_delta,
        "Cliff's Delta": cliffs_effect,
        "Cliff's Effect": cliffs_size,
        "Bot mean": scipy.stats.tmean(x),
        "Bot median": statistics.median(x),
        "Non-bot mean": scipy.stats.tmean(y),
        "Non-bot median": statistics.median(y),
    }

    file_management.write_data(test_result, owner, repo, f"{name}_{metric}")


def cliffsDelta(lst1, lst2, **dull):

    """Returns delta and true if there are more than 'dull' differences"""
    if not dull:
        dull = {'small': 0.147, 'medium': 0.33, 'large': 0.474} # effect sizes from (Hess and Kromrey, 2004)
    m, n = len(lst1), len(lst2)
    lst2 = sorted(lst2)
    j = more = less = 0
    for repeats, x in runs(sorted(lst1)):
        while j <= (n - 1) and lst2[j] < x:
            j += 1
        more += j*repeats
        while j <= (n - 1) and lst2[j] == x:
            j += 1
        less += (n - j)*repeats
    d = (more - less) / (m*n)
    size = lookup_size(d, dull)
    return d, size


def lookup_size(delta: float, dull: dict) -> str:
    """
    :type delta: float
    :type dull: dict, a dictionary of small, medium, large thresholds.
    """
    delta = abs(delta)
    if delta < dull['small']:
        return 'negligible'
    if dull['small'] <= delta < dull['medium']:
        return 'small'
    if dull['medium'] <= delta < dull['large']:
        return 'medium'
    if delta >= dull['large']:
        return 'large'


def runs(lst):
    """Iterator, chunks repeated values"""
    for j, two in enumerate(lst):
        if j == 0:
            one, i = two, 0
        if one != two:
            yield j - i, one
            i = j
        one = two
    yield j - i + 1, two