from src.analysis.tests import ks_test
from src.analysis.plotting import qq_plot
from src.analysis.helpers import split_prs_into_lists


def perform_statistical_tests(bot_prs, sim_prs):
    bot_variables = split_prs_into_lists(bot_prs)
    sim_variables = split_prs_into_lists(sim_prs)

    #qq_plot.qq_stuff(sim_variables["number_of_comments"], bot_variables["number_of_comments"])

    for key in bot_variables.keys():
        print(f"KS-test for {key}")
        ks_test.ks_test(sim_variables[key], bot_variables[key])
        qq_plot.qq_plotting(sim_variables[key], bot_variables[key], "Similar PR's", "Bot PR's", key)
