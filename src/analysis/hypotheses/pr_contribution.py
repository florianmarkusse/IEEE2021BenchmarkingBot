from src.analysis.plotting import combo, boxplot, frequency_graph, scatter_graph
from src.analysis.hypotheses import subroutines
from src.utility.helpers import periodize_prs, categorize_prs
from src.analysis.helpers import split_prs_into_lists
from functools import cmp_to_key

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


def generate_pr_benchmark_calling(owner, repo, data_set):

    bot_username = subroutines.get_bot_username(owner, repo)
    benchmarking_bot_calls = []

    for pr in data_set["bot_prs"]:
        total_bot_calls = 0
        for comment in pr["commenterAndLengths"]:
            if bot_username in comment:
                total_bot_calls += 1
        benchmarking_bot_calls.append(total_bot_calls)

    frequency_graph.create_overlapping_histogram(
        owner,
        repo,
        data_set["name"],
        "Benchmark bot calls",
        10,
        benchmarking_bot_calls,
        data_set["bot_prs_name"],
        None,
        None,
        1.0,
        True,
        1,
    )

def generate_contributor_interaction(owner, repo, all_prs, bot_prs):

    created_to_prs = categorize_prs(all_prs, "author", "login")

    for author in created_to_prs:
        with_benchmark = 0
        total_prs = len(created_to_prs[author])
        for pr in created_to_prs[author]:
            if "callers" in pr and len(pr["callers"]) > 0:
                with_benchmark += 1

        created_to_prs[author] = {
            "created": total_prs,
            "fraction": with_benchmark / total_prs,
            "with_benchmark": with_benchmark
        }

    cut_offs = [0, 10, 50, 100]

    for cut_off in cut_offs:
        x_distribution = [created_to_prs[key]["fraction"] for key in created_to_prs if created_to_prs[key]["created"] >= cut_off]
        y_distribution = [created_to_prs[key]["created"] for key in created_to_prs if created_to_prs[key]["created"] >= cut_off]

        scatter_graph.scatter_graph(owner, repo, f"allPRs_at_least_{cut_off}", x_distribution, y_distribution,
                                    "Fraction of PR's", "Number of created PR's",
                                    0.0, 1.0)
    for i in range(10):
        interacted_previously = 0
        interacted_again = 0
        for author in created_to_prs:
            if created_to_prs[author]["with_benchmark"] >= i:
                interacted_previously += 1
            if created_to_prs[author]["with_benchmark"] >= i + 1:
                interacted_again += 1

        fraction = interacted_again / interacted_previously

        print(f"From {i} to {i + 1}: Fraction: {fraction}\tPreviously: {interacted_previously}\tAgain: {interacted_again}")
