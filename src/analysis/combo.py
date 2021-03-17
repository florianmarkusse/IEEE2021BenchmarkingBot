import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from src.analysis import helpers


def combo_period_analysis(owner, repo, period_summaries):
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
    ax2.plot(periods, fraction, color="gray")

    ax1.set_ylabel('Frequency')
    ax1.legend()

    ax2.set_ylabel("Fraction bot PR's out of total PR's")

    myLocator = ticker.MultipleLocator(4)
    ax1.xaxis.set_major_locator(myLocator)

    fig.autofmt_xdate()

    plt.tight_layout(pad=0)
    plt.savefig(helpers.get_graph_path(owner, repo) + "/combo/bot_pr_periodized.png", transparent=True)

    plt.show()
