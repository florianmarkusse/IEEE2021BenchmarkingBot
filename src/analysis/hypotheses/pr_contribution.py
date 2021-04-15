from src.analysis import data_printer
from src.analysis.plotting import combo, boxplot
from src.utility.helpers import periodize_prs
from src.analysis.helpers import split_prs_into_lists


def generate_pr_contribution(owner, repo, data_set, members_are_exclusive):
    """
    Perform a monthly analysis on the repository based on the PR's that were created and those that contain a bot
    contribution.

    Parameters
    ----------
    members_are_exclusive : boolean value to check if members bot_prs and non_bot_prs are exclusive data sets.
    owner : The owner of the repository.
    repo : The name of the repository.
    data_set : The data set to be analyzed.

    Returns
    -------
    A dictionary where each entry is a period that contains PR data from that repository in that specific period.
    """
    all_bot_prs_per_month = periodize_prs(data_set["bot_prs"], "%m-%y")
    all_prs_per_month = periodize_prs(data_set["non_bot_prs"], "%m-%y")

    period_summaries = []

    for period in all_prs_per_month:
        if members_are_exclusive:
            non_bot_prs_per_period = len(all_prs_per_month[period]) if period in all_prs_per_month else 0
            bot_prs_per_period = len(all_bot_prs_per_month[period]) if period in all_bot_prs_per_month else 0
            period_summary = {
                "period": period,
                "all_prs": non_bot_prs_per_period + bot_prs_per_period,
                "bot_prs": bot_prs_per_period,
            }
        else:
            period_summary = {
                "period": period,
                "all_prs": len(all_prs_per_month[period]),
                "bot_prs": len(all_bot_prs_per_month[period]) if period in all_bot_prs_per_month else 0,
            }

        period_summary["fraction"] = period_summary["bot_prs"] / period_summary["all_prs"]

        period_summaries.append(period_summary)

    # Create periodized combo chart for PR's with bot contribution and without bot contribution.
    combo.combo_period_analysis(owner, repo, data_set["name"], period_summaries)
