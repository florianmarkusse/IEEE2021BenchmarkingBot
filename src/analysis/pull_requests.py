from src.utility.helpers import periodize_prs, categorize_prs, get_date_from_string
from statistics import mean, median

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import collections


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

    periods = [period_summary["period"] for period_summary in period_summaries]
    frequency_non_bot_pr_per_month = [(period_summary["all_prs"] - period_summary["bot_prs"]) for period_summary in
                                      period_summaries]
    frequency_bot_pr_per_month = [period_summary["bot_prs"] for period_summary in period_summaries]

    fraction = [period_summary["fraction"] for period_summary in period_summaries]

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.bar(periods, frequency_bot_pr_per_month, 0.35, label="Frequency bot PR's")
    ax1.bar(periods, frequency_non_bot_pr_per_month, 0.35, label="Frequency non-bot PR's",
            bottom=frequency_bot_pr_per_month)
    ax2.plot(periods, fraction, color="gray")

    ax1.set_ylabel('Frequency')
    ax1.legend()

    ax2.set_ylabel("Fraction bot PR's out of total PR's")

    myLocator = mticker.MultipleLocator(4)
    ax1.xaxis.set_major_locator(myLocator)

    fig.autofmt_xdate()

    plt.tight_layout(pad=0)
    plt.savefig("../data/projects/{owner}/{repo}/images/bot_pr_periodized.png".format(owner=owner, repo=repo),
                transparent=True)

    plt.show()

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

    for cut_off in [0, 10, 50, 100]:
        significant_contributors = [user_summary for user_summary in user_summaries if
                                    user_summary["all_prs"] >= cut_off]

        significant_contributors_fraction = [user_summary["fraction"] for user_summary in significant_contributors]
        significant_contributors_total_prs = [user_summary["all_prs"] for user_summary in significant_contributors]

        plt.xlim(left=0, right=1.0)

        plt.scatter(significant_contributors_fraction, significant_contributors_total_prs)
        plt.xlabel("Fraction PR's with bot contribution")
        plt.ylabel("Number of PR's")

        plt.tight_layout(pad=0)
        plt.savefig("../data/projects/{owner}/{repo}/images/user_interaction_with_bot{cut_off}.png".format(
            owner=owner, repo=repo, cut_off=cut_off),
            transparent=True)

        plt.show()

    for i in range(20):
        previous_interactors = len([user_summary for user_summary in user_summaries if user_summary["bot_prs"] >= i])
        again_interactors = len([user_summary for user_summary in user_summaries if user_summary["bot_prs"] >= i + 1])

        interact_again = '%.3f' % (again_interactors / previous_interactors)

        print(
            f"Odds of interaction from {i} interaction(s) to {i + 1} interaction(s):\t{interact_again}\t{previous_interactors}\t{again_interactors}")

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

    pr_comment_frequency_analysis(owner, repo, pr_type, number_of_comments)
    pr_participant_frequency_analysis(owner, repo, pr_type, number_of_participants)
    pr_review_activity_analysis(owner, repo, pr_type, number_of_participants)
    pr_commit_activity_analysis(owner, repo, pr_type, number_of_commits)

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


def pr_comment_frequency_analysis(owner, repo, pr_type, number_of_comments):
    counter = collections.Counter(number_of_comments)
    counter = sorted(counter.items())

    if pr_type == "bot_PRs":
        counter = [(pair[0], max(0, pair[1] - 2)) for pair in counter]

    for cut_off in [40, 60]:
        path = "../data/projects/{owner}/{repo}/images/graphs/{pr_type}_comment{cut_off}.png".format(owner=owner,
                                                                                              repo=repo,
                                                                                              pr_type=pr_type,
                                                                                              cut_off=cut_off)
        create_frequency_bar_chart(counter, cut_off, False, "Comments per PR", path)


def pr_participant_frequency_analysis(owner, repo, pr_type, number_of_participants):
    counter = collections.Counter(number_of_participants)
    counter = sorted(counter.items())

    if pr_type == "bot_PRs":
        counter = [(pair[0], pair[1] - 1) for pair in counter]

    for cut_off in [20]:
        path = "../data/projects/{owner}/{repo}/images/graphs/{pr_type}_participant{cut_off}.png".format(owner=owner,
                                                                                                  repo=repo,
                                                                                                  pr_type=pr_type,
                                                                                                  cut_off=cut_off)
        create_frequency_bar_chart(counter, cut_off, True, "Participants per PR", path)


def pr_review_activity_analysis(owner, repo, pr_type, number_of_reviews):
    counter = collections.Counter(number_of_reviews)
    counter = sorted(counter.items())

    for cut_off in [10]:
        path = "../data/projects/{owner}/{repo}/images/graphs/{pr_type}_review{cut_off}.png".format(owner=owner, repo=repo,
                                                                                             pr_type=pr_type,
                                                                                             cut_off=cut_off)
        create_frequency_bar_chart(counter, cut_off, True, "Reviews per PR", path)


def pr_commit_activity_analysis(owner, repo, pr_type, number_of_commits):
    counter = collections.Counter(number_of_commits)
    counter = sorted(counter.items())

    for cut_off in [10]:
        path = "../data/projects/{owner}/{repo}/images/graphs/{pr_type}_commit{cut_off}.png".format(owner=owner,
                                                                                             repo=repo,
                                                                                             pr_type=pr_type,
                                                                                             cut_off=cut_off)
        create_frequency_bar_chart(counter, cut_off, True, "Commits per PR", path)


def create_frequency_bar_chart(counter, cut_off, is_every_tick, x_label, path):
    counter_with_cut_off = []
    for i in range(cut_off + 1):
        found_in_counter = False
        for pair in counter:
            if not found_in_counter and pair[0] == i:
                counter_with_cut_off.append((str(pair[0]), pair[1]))
                found_in_counter = True
        if not found_in_counter:
            counter_with_cut_off.append((str(i), 0))

    cut_offs = [count[1] for count in counter if count[0] > cut_off]
    counter_with_cut_off.append((f">{cut_off}", sum(cut_offs)))

    if is_every_tick:
        ticks = [str(possible_tick[0]) for possible_tick in counter_with_cut_off]
    else:
        ticks = [str(ele) for ele in range(cut_off) if ele % 5 == 0 and ele != cut_off]
        ticks.append(f">{cut_off}")

    x = [str(pair[0]) for pair in counter_with_cut_off]
    y = [pair[1] for pair in counter_with_cut_off]

    show_frequency_bar_chart(x, y, ticks, x_label, path)


def show_frequency_bar_chart(x, y, x_ticks, x_label, path):
    fig, ax1 = plt.subplots()

    plt.bar(x, y)
    plt.xlabel(x_label)
    plt.ylabel("Frequency")

    ax1.xaxis.set_ticks(x_ticks)

    plt.tight_layout(pad=0.04)
    plt.savefig(path, transparent=True)

    plt.show()
