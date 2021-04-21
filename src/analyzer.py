from src.utility import file_management
from src.analysis.plotting import qq_plot, top_ten
from src.analysis.hypotheses import pr_activity, pr_impact, pr_contribution

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

    ### PR Activity

    # Participants
    # for data_set_pair in data_set_pairs:
    #     pr_activity.generate_participants(owner, repo, data_set_pair)

    # # Comments
    # for data_set_pair in data_set_pairs:
    #     pr_activity.generate_comments(owner, repo, data_set_pair)
    #
    # Reviews
    # for data_set_pair in data_set_pairs:
    #     pr_activity.generate_reviews(owner, repo, data_set_pair)
    #
    # ### PR impact
    #
    # # PR status
    # for data_set_pair in data_set_pairs:
    #     pr_impact.generate_pr_status(owner, repo, data_set_pair)

    # Commits
    for data_set_pair in data_set_pairs:
        pr_impact.generate_commits(owner, repo, data_set_pair)
    #
    # # Source files changed
    # for data_set_pair in data_set_pairs:
    #     pr_impact.generate_source_files_changed(owner, repo, data_set_pair)
    #
    # # Additions - Deletions
    # for data_set_pair in data_set_pairs:
    #     pr_impact.generate_additions_deletions(owner, repo, data_set_pair)

    ### PR contribution
    for data_set_pair in data_set_pairs:
        pr_contribution.generate_quarterly_pr_contribution(owner, repo, data_set_pair)
