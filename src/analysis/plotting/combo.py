import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from src.analysis import helpers


def combo_period_analysis(owner, repo, data_set_name, period_summaries):
    """
    Creates a combo chart consisting of a stacked bar chart and line to analyze the usage over time.

    Parameters
    ----------
    owner : The owner of the repository.
    repo : The name of the repository.
    period_summaries : The summaries categorized on a period. Assumed to have the following members:
        "period": The name of this period (e.g. a month and year: 11-2020)
        "all_prs": The number of all the PR's in this period.
        "bot_prs": The number of all the PR's with bot contribution in this period.
        "fraction": The fraction of the PR's with bot contribution out of all the PR's in this period.

    Returns
    -------
    """
    periods = [period_summary["period"] for period_summary in period_summaries]
    frequency_non_bot_pr_per_month = [(period_summary["all_prs"] - period_summary["bot_prs"]) for period_summary in
                                      period_summaries]
    frequency_bot_pr_per_month = [period_summary["bot_prs"] for period_summary in period_summaries]

    fraction = [period_summary["fraction"] for period_summary in period_summaries]

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.bar(periods, frequency_bot_pr_per_month, 0.35, label="Frequency bot PR's")
    ax1.bar(periods, frequency_non_bot_pr_per_month, 0.35, label="Frequency non-bot PR's",
            bottom=frequency_bot_pr_per_month)
    ax2.plot(periods, fraction, color="red")

    ax1.set_ylabel('Frequency')
    ax1.legend()

    ax2.set_ylabel("Fraction bot PR's out of total PR's")

    myLocator = ticker.MultipleLocator(4)
    ax1.xaxis.set_major_locator(myLocator)

    fig.autofmt_xdate()

    plt.tight_layout(pad=0)
    plt.savefig(helpers.get_graph_path(owner, repo) + f"/combo/{data_set_name}_bot_pr_periodized.png", transparent=True)

    plt.show()
