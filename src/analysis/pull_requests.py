from src.utility.helpers import periodize_prs
from src.utility.helpers import categorize_prs


def monthly_analysis(owner, repo, all_prs, bot_prs):
    all_prs_per_month = periodize_prs(all_prs, "%m-%y")
    all_bot_prs_per_month = periodize_prs(bot_prs, "%m-%y")

    period_summaries = []

    for period in all_prs_per_month:
        period_summary = {
            "period": period,
            "all_prs": len(all_prs_per_month[period]),
            "bot_prs": len(all_bot_prs_per_month[period]) if period in all_bot_prs_per_month else 0,
        }

        period_summary["fraction"] = period_summary["bot_prs"] / period_summary["all_prs"]

        period_summaries.append(period_summary)

    print("Project\tBot PR's\tNon-bot PR's\tFraction\tTotal PR's")
    print("{owner}/{repo}\t{bot_prs}\t{non_bot_prs}\t{fraction}\t{total_prs}\n".format(
        owner=owner,
        repo=repo,
        bot_prs=len(bot_prs),
        non_bot_prs=len(all_prs) - len(bot_prs),
        fraction=len(bot_prs) / len(all_prs),
        total_prs=len(all_prs)
    ))

    print("Period\tBot PR's\tNon-bot PR's\tFraction\tTotal PR's")

    for period_summary in period_summaries:
        print("{period}\t{bot_prs}\t{non_bot_prs}\t{fraction}\t{all_prs}".format(
            period=period_summary["period"],
            bot_prs=period_summary["bot_prs"],
            non_bot_prs=period_summary["all_prs"] - period_summary["bot_prs"],
            fraction=period_summary["fraction"],
            all_prs=period_summary["all_prs"],
        ))

    return period_summaries


def user_analysis(owner, repo, all_prs, bot_prs):
    all_prs_per_user = categorize_prs(all_prs, "author", "login")
    bot_prs_per_user = categorize_prs(bot_prs, "author", "login")

    user_summaries = []

    for user in all_prs_per_user:
        user_summary = {
            "user": user,
            "all_prs": len(all_prs_per_user[user]),
            "bot_prs": len(bot_prs_per_user[user]) if user in bot_prs_per_user else 0
        }

        user_summary["fraction"] = user_summary["bot_prs"] / user_summary["all_prs"]

        user_summaries.append(user_summary)

    print("Project\tContributors creating PR with bot contribution\tContributors calling for bot "
          "contribution\tFraction\tTotal contributors")
    print(
        "{owner}/{repo}\t{users_creating_pr_with_bot}\t{users_calling_bot}\t{fraction}\t{total_contributors}\n".format(
            owner=owner,
            repo=repo,
            users_creating_pr_with_bot=len(bot_prs_per_user),
            users_calling_bot="N/A",  # TODO: CHANGE WHEN ALSO INCLUDING PROJECTS THAT CALL BOTS EXPLICITLY
            fraction=len(bot_prs_per_user) / len(all_prs_per_user),
            total_contributors=len(all_prs_per_user)
        ))

    print("Contributor\tBot PR's\tNon-bot PR's\tFraction\tTotal PR's")
    for user_summary in user_summaries:
        print("{user}\t{bot_prs}\t{non_bot_prs}\t{fraction}\t{all_prs}".format(
            user=user_summary["user"],
            bot_prs=user_summary["bot_prs"],
            non_bot_prs=user_summary["all_prs"] - user_summary["bot_prs"],
            fraction=user_summary["fraction"],
            all_prs=user_summary["all_prs"],
        ))

    return user_summaries
