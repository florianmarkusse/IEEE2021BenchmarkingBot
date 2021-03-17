def print_again_interaction_with_bot(summaries, member, max_range, value):
    for i in range(max_range):
        previous = len([summary for summary in summaries if summary[member] >= i])
        again = len([summary for summary in summaries if summary[member] >= i + 1])

        again_fraction = '%.3f' % (again / previous)

        print(f"Odds of going from {i} {value} to {i + 1} {value}:\t{again_fraction}\t{previous}\t{again}")


def print_contributor_created_prs_bot_interaction(user_summaries):
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


def print_project_prs_data(owner, repo, all_prs_number, bot_prs_number, period_summaries):
    print_project_prs_bot_summary(owner, repo, all_prs_number, bot_prs_number)
    print_project_prs_monthly(period_summaries)


def print_project_prs_bot_summary(owner, repo, all_prs_number, bot_prs_number):
    print("Project\tBot PR's\tNon-bot PR's\tFraction\tTotal PR's")
    print("{owner}/{repo}\t{bot_prs}\t{non_bot_prs}\t{fraction}\t{total_prs}\n".format(
        owner=owner,
        repo=repo,
        bot_prs=bot_prs_number,
        non_bot_prs=all_prs_number - bot_prs_number,
        fraction=bot_prs_number / all_prs_number,
        total_prs=all_prs_number
    ))


def print_project_prs_monthly(period_summaries):
    print("Period\tBot PR's\tNon-bot PR's\tFraction\tTotal PR's")
    for period_summary in period_summaries:
        print("{period}\t{bot_prs}\t{non_bot_prs}\t{fraction}\t{all_prs}".format(
            period=period_summary["period"],
            bot_prs=period_summary["bot_prs"],
            non_bot_prs=period_summary["all_prs"] - period_summary["bot_prs"],
            fraction=period_summary["fraction"],
            all_prs=period_summary["all_prs"],
        ))