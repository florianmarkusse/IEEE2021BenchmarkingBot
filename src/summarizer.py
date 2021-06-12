from src.utility import file_management


# only do data set B and C
# "PRsOneToOne" and "PRsChangedSourceFilesAtLeast2

projects = file_management.get_projects_to_mine()

file_starts = [
    "PRsOneToOne",
    "PRsChangedSourceFilesAtLeast2",
    "PRsChangedSourceFilesAtLeast4",
    "PRsChangedSourceFilesAtLeast8",
]

file_ends = {
    "_# of commits": "Number of commits",
    "_# of participants": "Number of participants",
    "_# of reviews": "Number of reviews",
    "_# of comments": "Number of comments",
    "_total comment length": "Total comment length"
}

measures = {
    "Bot mean",
    "Bot median",
    "Non-bot mean",
    "Non-bot median"
}

big_summary = {}
for project in projects:
    project_summary_data = {}
    for file_start in file_starts:
        project_summary_data.update({
            file_start: {}
        })
        for file_end, file_desc in file_ends.items():
            file_to_get = file_start + file_end
            metric_file = file_management.get_metric_file(project.get("owner"), project.get("repo"), file_to_get)

            value = {}

            for measure in measures:
                value.update({
                    measure: metric_file.get(measure)
                })

            project_summary_data[file_start].update({
                file_desc: value
            })

    project_key = f"{project.get('owner')}/{project.get('repo')}"

    big_summary.update({
        project_key: project_summary_data
    })

print(big_summary)
file_management.write_summary(big_summary, "ProjectMetrics")