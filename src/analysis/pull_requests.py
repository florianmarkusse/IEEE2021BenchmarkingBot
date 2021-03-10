from src.utility.helpers import periodize_prs, categorize_prs, get_date_from_string
from statistics import mean, median


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

        if user in bot_prs_per_user:
            user_summary["last_bot_pr_created"] = \
                str(get_date_from_string(bot_prs_per_user[user][len(bot_prs_per_user[user]) - 1]["createdAt"]).date())
        else:
            user_summary["last_bot_pr_created"] = "N/A"

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

    print("Contributor\tBot PR's\tLast bot PR created\tNon-bot PR's\tFraction\tTotal PR's")
    for user_summary in user_summaries:
        print("{user}\t{bot_prs}\t{last_bot_pr_created}\t{non_bot_prs}\t{fraction}\t{all_prs}".format(
            user=user_summary["user"],
            bot_prs=user_summary["bot_prs"],
            last_bot_pr_created=user_summary["last_bot_pr_created"],
            non_bot_prs=user_summary["all_prs"] - user_summary["bot_prs"],
            fraction=user_summary["fraction"],
            all_prs=user_summary["all_prs"],
        ))

    return user_summaries


def pr_activity_analysis(owner, repo, prs, pr_type):

    pr_activity_summary = {}

    # Calculate avg/median comments/participants/reviews/commits
    number_of_comments = []
    number_of_participants = []
    number_of_reviews = []
    number_of_commits = []

    for pr in prs:
        number_of_comments.append(pr["comments"]["totalCount"])
        number_of_participants.append(pr["participants"]["totalCount"])
        number_of_reviews.append(pr["reviews"]["totalCount"])
        number_of_commits.append(pr["commits"]["totalCount"])

    print("Project\tType of PR's\tAverage # of comments\tMedian # of comments\tAverage # of participants\tMedian # of "
          "participants\tAverage # of reviews\tMedian # of reviews\tAverage # of commits\tMedian # of commits")
    print(
        "{owner}/{repo}\t{pr_type}\t{avg_comments}\t{med_comments}\t{avg_participants}\t{med_participants}\t{avg_reviews}\t{med_reviews}\t{avg_commits}\t{med_commits}\n".format(
            owner=owner,
            repo=repo,
            pr_type=pr_type,
            avg_comments=mean(number_of_comments),
            med_comments=median(number_of_comments),
            avg_participants=mean(number_of_participants),
            med_participants=median(number_of_participants),
            avg_reviews=mean(number_of_reviews),
            med_reviews=median(number_of_reviews),
            avg_commits=mean(number_of_commits),
            med_commits=median(number_of_commits)
        ))

    print("PR number\t# of comments\t# of participants\t# of reviews\t# of commits")

    for pr in prs:
        print("{pr_number}\t{comment_count}\t{participant_count}\t{review_count}\t{commit_count}".format(
            pr_number=pr["number"],
            comment_count=pr["comments"]["totalCount"],
            participant_count=pr["participants"]["totalCount"],
            review_count=pr["reviews"]["totalCount"],
            commit_count=pr["commits"]["totalCount"]
        ))

    return {
        "average_comments": mean(number_of_comments),
        "median_comments": median(number_of_comments),
        "average_participants": mean(number_of_participants),
        "median_participants": median(number_of_participants),
        "average_reviews": mean(number_of_reviews),
        "median_reviews": median(number_of_reviews),
        "average_commits": mean(number_of_commits),
        "median_commits": median(number_of_commits)
    }
