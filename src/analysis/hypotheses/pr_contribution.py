from src.analysis import data_printer
from src.analysis.plotting import combo, boxplot
from src.utility.helpers import periodize_prs
from src.analysis.helpers import split_prs_into_lists
from functools import cmp_to_key


# def generate_monthly_pr_contribution(owner, repo, data_set):
#     """
#     Perform a monthly analysis on the repository based on the PR's that were created and those that contain a bot
#     contribution.
#
#     Parameters
#     ----------
#     members_are_exclusive : boolean value to check if members bot_prs and non_bot_prs are exclusive data sets.
#     owner : The owner of the repository.
#     repo : The name of the repository.
#     data_set : The data set to be analyzed.
#
#     Returns
#     -------
#     A dictionary where each entry is a period that contains PR data from that repository in that specific period.
#     """
#     all_bot_prs_per_month = periodize_prs(data_set["bot_prs"], "%m-%y")
#     all_prs_per_month = periodize_prs(data_set["non_bot_prs"], "%m-%y")
#
#     period_summaries = []
#
#     for period in all_prs_per_month:
#         non_bot_prs_per_period = len(all_prs_per_month[period]) if period in all_prs_per_month else 0
#         bot_prs_per_period = len(all_bot_prs_per_month[period]) if period in all_bot_prs_per_month else 0
#         period_summary = {
#             "period": period,
#             "all_prs": non_bot_prs_per_period + bot_prs_per_period,
#             "bot_prs": bot_prs_per_period,
#         }
#
#         period_summary["fraction"] = period_summary["bot_prs"] / period_summary["all_prs"]
#
#         period_summaries.append(period_summary)
#
#     # Create periodized combo chart for PR's with bot contribution and without bot contribution.
#     combo.combo_period_analysis(owner, repo, data_set["name"], period_summaries)


def month_year_comp(a, b):
    a_month = int(a[0:2])
    a_year = int(a[3:len(a)])

    b_month = int(b[0:2])
    b_year = int(b[3:len(a)])

    if a_year > b_year:
        return 1
    elif a_year == b_year:
        if a_month > b_month:
            return 1
        else:
            return -1
    else:
        return -1


def calculate_pr_contribution_monthly(data_set):
    bot_prs_per_month = periodize_prs(data_set["bot_prs"], "%m-%y")
    bot_prs_per_month_copy = bot_prs_per_month.copy()
    non_bot_prs_per_month = periodize_prs(data_set["non_bot_prs"], "%m-%y")
    non_bot_prs_per_month_copy = non_bot_prs_per_month.copy()

    bot_months = list(bot_prs_per_month.keys())
    non_bot_months = list(non_bot_prs_per_month.keys())

    all_months = [month for month in bot_months]
    all_months.extend([month for month in non_bot_months])

    all_months = list(set(all_months))
    all_months.sort(key=cmp_to_key(month_year_comp))

    monthly_summaries = []

    for month in all_months:
        bot_prs_per_month = len(bot_prs_per_month_copy[month]) if month in bot_months else 0
        non_bot_prs_per_month = len(non_bot_prs_per_month_copy[month]) if month in non_bot_months else 0

        monthly_summary = {
            "period": month,
            "non_bot_prs": non_bot_prs_per_month,
            "bot_prs": bot_prs_per_month,
        }

        monthly_summary["fraction"] = monthly_summary["bot_prs"] / (
                monthly_summary["bot_prs"] + monthly_summary["non_bot_prs"])

        monthly_summaries.append(monthly_summary)

    return monthly_summaries


def generate_monthly_pr_contribution(owner, repo, data_set):
    monthly_summaries = calculate_pr_contribution_monthly(data_set)

    periods = [monthly_summary["period"] for monthly_summary in monthly_summaries]
    bot_frequency = [monthly_summary["bot_prs"] for monthly_summary in monthly_summaries]
    non_bot_frequency = [monthly_summary["non_bot_prs"] for monthly_summary in monthly_summaries]
    bot_fraction = [monthly_summary["fraction"] for monthly_summary in monthly_summaries]

    combo.combo_period(owner, repo, data_set["name"], "monthly", periods, bot_frequency, non_bot_frequency,
                       bot_fraction)


def get_quarterly_period(monthly_period):
    year = monthly_period[3:len(monthly_period)]

    quarter = ""
    month = int(monthly_period[0:2])
    if month < 4:
        quarter = "Q1"
    elif month < 7:
        quarter = "Q2"
    elif month < 10:
        quarter = "Q3"
    else:
        quarter = "Q4"

    return quarter + "-" + year


def generate_quarterly_pr_contribution(owner, repo, data_set):
    monthly_summaries = calculate_pr_contribution_monthly(data_set)

    months = [monthly_summary["period"] for monthly_summary in monthly_summaries]

    quarterly_periods = {}
    for monthly_summary in monthly_summaries:
        quarterly_period = get_quarterly_period(monthly_summary["period"])
        if quarterly_period in quarterly_periods.keys():
            current_quarter_data = quarterly_periods.get(quarterly_period)
            current_quarter_data["non_bot_prs"] += monthly_summary.get("non_bot_prs")
            current_quarter_data["bot_prs"] += monthly_summary.get("bot_prs")
        else:
            quarterly_periods[quarterly_period] = {
                "period": get_quarterly_period(monthly_summary["period"]),
                "non_bot_prs": monthly_summary.get("non_bot_prs"),
                "bot_prs": monthly_summary.get("bot_prs"),
            }

    quarterly_periods = list(quarterly_periods.values())

    for quarter in quarterly_periods:
        quarter["fraction"] = quarter["bot_prs"] / (quarter["bot_prs"] + quarter["non_bot_prs"])

    periods = [quarter["period"] for quarter in quarterly_periods]
    bot_frequency = [quarter["bot_prs"] for quarter in quarterly_periods]
    non_bot_frequency = [quarter["non_bot_prs"] for quarter in quarterly_periods]
    bot_fraction = [quarter["fraction"] for quarter in quarterly_periods]

    combo.combo_period(owner, repo, data_set["name"], "quarterly", periods, bot_frequency, non_bot_frequency,
                       bot_fraction)
