from scipy.stats import ks_2samp
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


def do_stuff(bot_prs, sim_prs):
    bot_number_of_comments = []
    bot_number_of_participants = []
    bot_number_of_reviews = []
    bot_number_of_commits = []

    for pr in bot_prs:
        bot_number_of_comments.append(pr["comments"]["totalCount"])
        bot_number_of_participants.append(pr["participants"]["totalCount"])
        bot_number_of_reviews.append(pr["reviews"]["totalCount"])
        bot_number_of_commits.append(pr["commits"]["totalCount"])

    sim_number_of_comments = []
    sim_number_of_participants = []
    sim_number_of_reviews = []
    sim_number_of_commits = []

    for pr in sim_prs:
        sim_number_of_comments.append(pr["comments"]["totalCount"])
        sim_number_of_participants.append(pr["participants"]["totalCount"])
        sim_number_of_reviews.append(pr["reviews"]["totalCount"])
        sim_number_of_commits.append(pr["commits"]["totalCount"])

    c_alpha = 1.628  # Assuming alpha = 0.01
    ks_critical_value = c_alpha * math.sqrt(
        (len(bot_number_of_comments) + len(sim_number_of_commits)) /
        (len(bot_number_of_comments) * len(sim_number_of_commits))
    )
    res = ks_2samp(bot_number_of_comments, sim_number_of_comments)
    print(res)
    print(ks_critical_value)
