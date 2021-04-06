from src.analysis.statistics import ks_test
from src.analysis.helpers import split_prs_into_lists


def perform_statistical_tests(bot_prs, sim_prs):
    bot_variables = split_prs_into_lists(bot_prs)
    sim_variables = split_prs_into_lists(sim_prs)

    for key in bot_variables.keys():
        print(f"KS-test for {key}")
        ks_test.ks_test(bot_variables[key], sim_variables[key])
