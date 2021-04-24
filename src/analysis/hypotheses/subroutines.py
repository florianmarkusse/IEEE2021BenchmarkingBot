from src.utility.file_management import get_projects_to_mine
from src.utility.helpers import categorize_prs


def get_distributions(data_set, attribute, at_least=0):
    x_distribution = []
    for pr in data_set["bot_prs"]:
        if pr[attribute] >= at_least:
            x_distribution.append(pr[attribute])
    y_distribution = []
    for pr in data_set["non_bot_prs"]:
        if pr[attribute] >= at_least:
            y_distribution.append(pr[attribute])

    return x_distribution, y_distribution


def categorize_data_set(owner, repo, data_set, attribute_to_categorize_on):
    bot_prs_categorized = categorize_prs(data_set["bot_prs"], attribute_to_categorize_on)
    bot_prs_categorized.pop(get_bot_username(owner, repo), None)

    non_bot_prs_categorized = categorize_prs(data_set["non_bot_prs"], attribute_to_categorize_on)
    non_bot_prs_categorized.pop(get_bot_username(owner, repo), None)

    return bot_prs_categorized, non_bot_prs_categorized


def get_bot_username(owner, repo):
    projects = get_projects_to_mine()
    for project in projects:
        if project["owner"] == owner and project["repo"] == repo:
            # Remove bot from results if applicable
            return project["botUsername"]
    return None
