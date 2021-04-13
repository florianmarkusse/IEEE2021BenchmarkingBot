from scipy.stats import ks_2samp
from src.analysis.helpers import split_prs_into_lists
import matplotlib.pyplot as plt
import statsmodels.api as sm
import math


def pp_plot(x, dist, line=True, ax=None):
    """
    Function for comparing empirical data to a theoretical distribution by using a P-P plot.

    Params:
    x - empirical data
    dist - distribution object from scipy.stats; for example scipy.stats.norm(0, 1)
    line - boolean; specify if the reference line (y=x) should be drawn on the plot
    ax - specified ax for subplots, None is standalone
    """
    if ax is None:
        ax = plt.figure().add_subplot(1, 1, 1)

    n = len(x)
    p = np.arange(1, n + 1) / n - 0.5 / n
    pp = np.sort(dist.cdf(x))
    sns.scatterplot(x=p, y=pp, color='blue', edgecolor='blue', ax=ax)
    ax.set_title('PP-plot')
    ax.set_xlabel('Theoretical Probabilities')
    ax.set_ylabel('Sample Probabilities')
    ax.margins(x=0, y=0)

    if line: ax.plot(np.linspace(0, 1), np.linspace(0, 1), 'r', lw=2)

    return ax


def ks_test(first_distribution, second_distribution):
    alpha = 0.01
    c_alpha = 1.628  # Assuming alpha = 0.01
    ks_critical_value = c_alpha * math.sqrt(
        (len(first_distribution) + len(second_distribution)) /
        (len(first_distribution) * len(second_distribution))
    )
    res = ks_2samp(first_distribution, second_distribution)

    if res[0] > ks_critical_value:
        print(f"Rejecting null hypothesis that both samples are drawn from the same distribution.")
        print(f"Because KS-statistic > cricitcal value")
        print(f"{res[0]} > {ks_critical_value}")
    else:
        print(f"Cannot reject null hypothesis that both samples are drawn from the same distribution.")
        print(f"Because KS-statistic <= cricitcal value")
        print(f"{res[0]} <= {ks_critical_value}")

    print(f"p-values: {res[1]} with alpha: {alpha}")


def do_stuff(bot_prs, sim_prs):

    bot_variables = split_prs_into_lists(bot_prs)
    sim_variables = split_prs_into_lists(sim_prs)

    c_alpha = 1.628  # Assuming alpha = 0.01
    ks_critical_value = c_alpha * math.sqrt(
        (len(bot_number_of_comments) + len(sim_number_of_commits)) /
        (len(bot_number_of_comments) * len(sim_number_of_commits))
    )
    res = ks_2samp(bot_number_of_comments, sim_number_of_comments)
    print(res)
    print(ks_critical_value)
