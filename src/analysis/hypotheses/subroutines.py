from src.utility.file_management import get_projects_to_mine
from src.utility.helpers import categorize_prs
import statistics

def get_distributions(data_set, attribute, at_least=0):
    x_distribution = []
    for pr in data_set["bot_prs"]:
        if attribute in pr and pr[attribute] >= at_least:
            x_distribution.append(pr[attribute])
    y_distribution = []
    for pr in data_set["non_bot_prs"]:
        if attribute in pr and pr[attribute] >= at_least:
            y_distribution.append(pr[attribute])

    return x_distribution, y_distribution


def categorize_data_set(owner, repo, data_set, attribute_to_categorize_on):
    bot_prs_categorized = categorize_prs(data_set["bot_prs"], attribute_to_categorize_on)
    bot_prs_categorized.pop(get_bot_username(owner, repo), None)

    non_bot_prs_categorized = categorize_prs(data_set["non_bot_prs"], attribute_to_categorize_on)
    non_bot_prs_categorized.pop(get_bot_username(owner, repo), None)

    return bot_prs_categorized, non_bot_prs_categorized


def get_always(owner, repo):
    projects = get_projects_to_mine()
    for project in projects:
        if project["owner"] == owner and project["repo"] == repo:
            return project["always"]
    return None

def get_additional_bots(owner, repo):
    projects = get_projects_to_mine()
    for project in projects:
        if project["owner"] == owner and project["repo"] == repo:
            # Remove bot from results if applicable
            return project["additionalBots"]
    return None


def get_bot_username(owner, repo):
    projects = get_projects_to_mine()
    for project in projects:
        if project["owner"] == owner and project["repo"] == repo:
            # Remove bot from results if applicable
            return project["botUsername"]
    return None

def get_mean_median(prs, attribute):
    distribution = []
    for pr in prs:
        if isinstance(pr[attribute], list):
            distribution.append(len(pr[attribute]))
        else:
            distribution.append(pr[attribute])

    if len(distribution) > 0:
        print(f"{attribute}: median = {statistics.median(distribution)}, average = {statistics.mean(distribution)}")

def descriptive_statistics(prs):
    get_mean_median(prs, "participants")
    get_mean_median(prs, "comments")
    get_mean_median(prs, "reviews")
    get_mean_median(prs, "commits")
    get_mean_median(prs, "additions")
    get_mean_median(prs, "deletions")
