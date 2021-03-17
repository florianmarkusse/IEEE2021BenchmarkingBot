from utility import file_management
from src.analysis import pull_requests

# Get projects to collect PR data for
projects = file_management.get_projects_to_mine()

for project in projects:
    owner = project.get("owner")
    repo = project.get("repo")

    prs = file_management.get_mined_prs(owner, repo)

    # create directories if missing.
    file_management.make_project_folder("../data/projects", owner, repo)

    ##
    # Create summarizing data.
    ##

    # Do an analysis based on a monthly period.
    period_summaries = pull_requests.monthly_analysis(owner, repo, prs.get("all_prs"), prs.get("bot_prs"))

    # Do an analysis based on a per-contributor basis.
    user_summaries = pull_requests.user_analysis(owner, repo, prs.get("all_prs"), prs.get("bot_prs"))

    # Do an activity analysis on the PR's.
    bot_pr_activity_summary = pull_requests.pr_activity_analysis(owner, repo, prs.get("bot_prs"), "bot_PRs")
    similar_pr_activity_summary = pull_requests.pr_activity_analysis(owner, repo, prs.get("similar_to_bot_prs"),
                                                                     "sim_PRs")
    all_pr_activity_summary = pull_requests.pr_activity_analysis(owner, repo, prs.get("all_prs"), "all_PRs")

    summary = {
        "totals": {
            "all_prs": len(prs.get("all_prs")),
            "bot_prs": len(prs.get("bot_prs")),
            "fraction": len(prs.get("bot_prs")) / len(prs.get("all_prs")),
            "similar_to_bot_prs": len(prs.get("similar_to_bot_prs"))
        },
        "periodized": period_summaries,
        "categorized_per_user": user_summaries,
        "all_pr_activity_summary": all_pr_activity_summary,
        "bot_pr_activity_summary": bot_pr_activity_summary,
        "similar_pr_activity_summary": similar_pr_activity_summary
    }

    file_management.write_data(summary, owner, repo, "summary")
