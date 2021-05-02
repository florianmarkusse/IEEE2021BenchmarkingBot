from src.utility import file_management
from src.analysis.plotting import qq_plot, top_ten, frequency_graph
from src.analysis.hypotheses import pr_activity, pr_impact, pr_contribution, subroutines
import json

# Get projects to collect PR data for
projects = file_management.get_projects_to_mine()

for project in projects:
    owner = project.get("owner")
    repo = project.get("repo")

    # Create directories if missing.
    file_management.make_project_folder("../data/projects", owner, repo)

    # Get data set pairs.
    data_set_pairs = file_management.get_data_set_pairs(owner, repo)

    ##
    # Create summarizing data.
    ##

    # Data sets sizes
    # for data_set_pair in data_set_pairs:
    #     print(f" {data_set_pair['name']}: bot PR's size: {len(data_set_pair['bot_prs'])}")
    #     print(f" {data_set_pair['name']}: non bot PR's size: {len(data_set_pair['non_bot_prs'])}")

    # ### PR Activity
    # # Participants
    # for data_set_pair in data_set_pairs:
    #     pr_activity.generate_participants(owner, repo, data_set_pair)

    # Comments
    # for data_set_pair in data_set_pairs:
    #     pr_activity.generate_comments(owner, repo, data_set_pair)

    # changed_source_sets = []
    # colors = ["red", "green", "blue"]
    # found = 0
    # for data_set_pair in data_set_pairs:
    #     if any(chr.isdigit() for chr in data_set_pair["name"]):
    #         number = ""
    #         for char in data_set_pair["name"]:
    #             if char.isdigit():
    #                 number = char
    #
    #         comments_after_benchmarking_bot_distributions = subroutines.get_distributions(data_set_pair, "commentsAfterContribution")
    #         number_of_comments_distributions = subroutines.get_distributions(data_set_pair, "comments")
    #
    #         fraction_of_comments_after_benchmarking_contribution = []
    #
    #         for index in range(len(number_of_comments_distributions[0])):
    #             fraction = comments_after_benchmarking_bot_distributions[0][index] / \
    #                        number_of_comments_distributions[0][index]
    #             fraction_of_comments_after_benchmarking_contribution.append(fraction)
    #
    #         add = {
    #             "name": f">= {number}",
    #             "data": fraction_of_comments_after_benchmarking_contribution,
    #             "color": colors[found]
    #         }
    #         found += 1
    #
    #         changed_source_sets.append(add)
    #
    # frequency_graph.compare_changed_files(owner, repo, "changed_files", 1.0, changed_source_sets, "Fraction of comments remaining",
    #                                       1.0, 0.1, 1, False, True)

    # # Reviews
    # for data_set_pair in data_set_pairs:
    #     pr_activity.generate_reviews(owner, repo, data_set_pair)

    # # Benchmarking bot callers
    # for data_set_pair in data_set_pairs:
    #     pr_activity.generate_benchmarking_bot_callers(owner, repo, data_set_pair)

    # ### PR impact
    #
    # PR status
    # for data_set_pair in data_set_pairs:
    #     pr_impact.generate_pr_status(owner, repo, data_set_pair)
    # Commits
    # for data_set_pair in data_set_pairs:
    #     pr_impact.generate_commits(owner, repo, data_set_pair)
    #
    # # Source files changed
    # for data_set_pair in data_set_pairs:
    #     pr_impact.generate_source_files_changed(owner, repo, data_set_pair)
    #
    # Additions - Deletions
    # for data_set_pair in data_set_pairs:
    #     pr_impact.generate_additions_deletions(owner, repo, data_set_pair)

    # ### PR contribution
    # for data_set_pair in data_set_pairs:
    #     pr_contribution.generate_quarterly_pr_contribution(owner, repo, data_set_pair)

    path = f"../data/projects/{owner}/{repo}/allPRs.json"

    all_prs_file = open(path, "r")
    all_prs = json.loads(all_prs_file.read()),
    all_prs_file.close()

    subroutines.descriptive_statistics(all_prs[0])
