import datetime


def get_only_files_with_extensions(files, extensions):
    """
    Keeps only the files that have the extensions present in the extensions variable.
    """
    extensions = tuple(extensions)
    source_files = []

    for file_name in files:
        if file_name.endswith(extensions):
            source_files.append(file_name)

    return source_files


def get_graphql_attributes(graphql_parameters):
    """
    Transforms the attributes that are wanted from the GraphQL mining into a well-formed query for GraphQL.
    """
    attributes = ""

    for parameter in graphql_parameters:
        attributes += (parameter.get("query") + "\n")

    return attributes


def is_similar(pr, min_max_source_files_changed, min_max_additions, min_max_deletions):
    """
    Checks if a Pull Request falls within the bounds given by the other arguments.
    """
    if "changedSourceFiles" not in pr:
        print("did not find")
    return (
            "changedSourceFiles" in pr and
            within_range_incl(len(pr.get("changedSourceFiles")), min_max_source_files_changed) and
            within_range_incl(pr.get("additions"), min_max_additions) and
            within_range_incl(pr.get("deletions"), min_max_deletions)
    )


def within_range_incl(val, bounds):
    """
    Checks if the value is withing the bounds given (inclusive).
    """
    return bounds[0] <= val <= bounds[1]


def pr_is_contained_in_prs(pr, other_prs):
    """
    Checks if the Pull Request is contained in the Pull Request iterable.
    """
    for other_pr in other_prs:
        if int(pr.get("number")) == int(other_pr.get("number")):
            return True
    return False


def get_date_from_string(created_at):
    """
    Create datetime object from string given in ISO 8601 format.
    """
    return datetime.datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')


def periodize_prs(prs, datetime_period):
    """
    Periodize the Pull Request iterable based on the period given by the second argument. Note that this is a string
    such that it can be parsed by the datetime module.
    """
    period_prs = {}

    for pr in prs:
        date_object = get_date_from_string(pr.get("createdAt"))
        period = date_object.strftime(datetime_period)

        if period in period_prs:
            period_prs[period].append(pr)
        else:
            period_prs[period] = [pr]

    return period_prs


def categorize_prs(prs, *attributes):
    """
    Categorize the Pull Request iterable based on the attribute(s) given by the second argument. If more than 1
    attribute is supplied, it is assumed this next attribute is a key included in the dictionary from the previous
    attribute supplied.
    """
    categorized_prs = {}

    for pr in prs:

        no_category = False

        category = pr
        for attribute in attributes:

            if attribute not in category or category[attribute] is None:
                no_category = True
            else:
                category = category[attribute]

        if no_category:
            if "uncategorized" in categorized_prs:
                categorized_prs["uncategorized"].append(pr)
            else:
                categorized_prs["uncategorized"] = [pr]
        else:
            if isinstance(category, list):
                for element in category:
                    if element in categorized_prs:
                        categorized_prs[element].append(pr)
                    else:
                        categorized_prs[element] = [pr]
            else:
                if category in categorized_prs:
                    categorized_prs[category].append(pr)
                else:
                    categorized_prs[category] = [pr]

    return categorized_prs
