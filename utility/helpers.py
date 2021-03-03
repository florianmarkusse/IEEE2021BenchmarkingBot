def get_only_files_with_extensions(files, extensions):

    extensions = tuple(extensions)
    source_files = []

    for file_name in files:
        if file_name.endswith(extensions):
            source_files.append(file_name)

    return source_files

def get_graphql_attributes(graphql_parameters):

    attributes = ""

    for parameter in graphql_parameters:
        attributes += (parameter.get("query") + "\n")

    return attributes