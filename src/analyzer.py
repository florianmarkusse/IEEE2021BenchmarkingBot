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
    # for data_set in data_sets:
    #     print(f" {data_set['name']}: bot PR's size: {len(data_set['bot_prs'])}")
    #     print(f" {data_set['name']}: non bot PR's size: {len(data_set['non_bot_prs'])}")

    ### PR Activity

    # # Participants
    # for data_set_pair in data_set_pairs:
    #     pr_activity.generate_participants(owner, repo, data_set_pair)

    # # Comments
    # for data_set_pair in data_set_pairs:
    #     pr_activity.generate_comments(owner, repo, data_set_pair)
    #
    # # Reviews
    # for data_set_pair in data_set_pairs:
    #     pr_activity.generate_reviews(owner, repo, data_set_pair)
    #
    # ### PR impact
    #
    # # PR status
    # for data_set in data_sets:
    #     pr_impact.generate_pr_status(owner, repo, data_set)
    #
    # # Commits
    # for data_set in data_sets:
    #     pr_impact.generate_commits(owner, repo, data_set)
    #
    # # Source files changed
    # for data_set in data_sets:
    #     pr_impact.generate_source_files_changed(owner, repo, data_set)
    #
    # # Additions - Deletions
    # for data_set in data_sets:
    #     pr_impact.generate_additions_deletions(owner, repo, data_set)

    ### PR contribution
    for data_set_pair in data_set_pairs:
        pr_contribution.generate_pr_contribution(owner, repo, data_set_pair)



    # # Do an analysis based on a monthly period.
    # period_summaries = pull_requests.monthly_analysis(owner, repo, prs.get("all_prs"), prs.get("bot_prs"))
    #
    # # Do an analysis based on a per-contributor basis.
    # user_summaries = pull_requests.contributor_analysis(owner, repo, prs.get("all_prs"), prs.get("bot_prs"))

    # # Do an activity analysis on the PR's for similar PR's
    # bot_pr_activity_summary = pull_requests.pr_activity_analysis(owner, repo, prs.get("bot_prs"), "bot_PRs")
    # similar_pr_activity_summary = pull_requests.pr_activity_analysis(owner, repo, prs.get("similar_to_bot_prs"),
    #                                                                  "sim_PRs")
    # all_pr_activity_summary = pull_requests.pr_activity_analysis(owner, repo, prs.get("all_prs"), "all_PRs")

    # # Do an activity analysis on the PR's with one-to-one matching PR's
    # bot_pr_activity_summary = pull_requests.pr_activity_analysis(owner, repo, prs.get("performance_labeled_bot_prs"), "performance_labeled_bot_prs")
    # similar_pr_activity_summary = pull_requests.pr_activity_analysis(owner, repo, prs.get("performance_labeled_all_prs"),
    #                                                                  "performance_labeled_all_prs")
    #
    # # Statistical test on PR variables and their frequencies
    # statistical_tests.perform_statistical_tests(prs.get("performance_labeled_bot_prs"), prs.get("performance_labeled_all_prs"))

    #
    # summary = {
    #     "totals": {
    #         "all_prs": len(prs.get("all_prs")),
    #         "bot_prs": len(prs.get("bot_prs")),
    #         "fraction": len(prs.get("bot_prs")) / len(prs.get("all_prs")),
    #         "similar_to_bot_prs": len(prs.get("similar_to_bot_prs"))
    #     },
    #     "periodized": period_summaries,
    #     "categorized_per_user": user_summaries,
    #     "all_pr_activity_summary": all_pr_activity_summary,
    #     "bot_pr_activity_summary": bot_pr_activity_summary,
    #     "similar_pr_activity_summary": similar_pr_activity_summary
    # }
    # #
    # ##
    # # Write summarizing data.
    # ##
    # file_management.write_data(summary, owner, repo, "summary")

    ##
    # Perform statistical tests.
    ##
    # ks_test.do_stuff(prs.get("bot_prs"), prs.get("similar_to_bot_prs"))
