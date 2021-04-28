from src.mining.graphql import pull_requests
from src.mining.rest import changed_files, participants_bot_callers_comment_lengths, reviewers
from src.mining.enhancement import enhancement
from src.utility import file_management


def collect_and_enrich(owner, repo, search_parameters, start_date, attributes, bot_call_string, file_name, token):
    print(f"Collecting {file_name}")
    prs = pull_requests.get_prs(owner, repo, search_parameters, start_date, attributes, token)
    file_management.write_data(prs, owner, repo, file_name)

    # In GraphQL it is hard to get some other parameters so add this data using their REST API.
    # Add the following parameters:
    #   - changed files
    #   - participants
    #   - bot callers
    #   - comment length per comment
    #   - reviewers
    #   - commits at PR open
    #   - "human" comments: The number of comments made by human contributors to human contributors. Note that this
    #     number excludes the contribution by the benchmarking bot as well as the comments asking for a benchmark.
    #   - participants without benchmarking bot: Simply the number of participants excluding the benchmarking bot, i.e.
    #     the number of participants minus 1.
    print(f"Collecting {file_name} changed files")
    changed_files.get_changes(owner, repo, prs, token)
    file_management.write_data(prs, owner, repo, file_name)

    print(f"Collecting {file_name} participants/bot callers/comment lengths")
    participants_bot_callers_comment_lengths.get_bot_caller_participants_commenters_in_prs(owner, repo, prs,
                                                                                           bot_call_string, token)
    file_management.write_data(prs, owner, repo, file_name)

    print(f"Collecting {file_name} reviewers")
    reviewers.get_reviewers_prs(owner, repo, prs, token)
    file_management.write_data(prs, owner, repo, file_name)

    print(f"Enriching {file_name} with human comments")
    enhancement.add_human_comments_member(prs)
    file_management.write_data(prs, owner, repo, file_name)

    print(f"Enriching {file_name} with benchmark bot free participants")
    enhancement.add_benchmark_bot_free_participants_member(owner, repo, prs)
    file_management.write_data(prs, owner, repo, file_name)

    print(f"Enriching {file_name} with comments after benchmarking bot contribution")
    enhancement.add_comments_after_benchmarking_bot_contribution(owner, repo, prs)
    file_management.write_data(prs, owner, repo, file_name)

    return prs
