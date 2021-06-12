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

measure_order = [
    'p-value',
    "CL",
    "Cliff's Delta",
    "Cliff's Effect",
    "Glass' Delta"
]

p_cutoff = 0.05 / (13 * 5)

def print_header():
    header = "\\multicolumn{2}{c|}{}\t"

    for project in projects:
        header += f"& {project.get('owner')}/{project.get('repo')}\t"

    header += " \\\\ \\hline"

    print(header)


def print_metric(end, file_metric):
    file_to_get = file_start + end

    measure_size = len(measure_order)
    pre_print = "\\multirow{" + str(measure_size) + "}{*}{" + file_metric + "}\t"
    print(pre_print, end="")

    p_values_list = {}
    for measure in measure_order:
        print(f"& {measure}\t", end="")
        for project in projects:
            metric_file = file_management.get_metric_file(project.get("owner"), project.get("repo"), file_to_get)

            if measure == "p-value":
                p_values_list.update({f"{project.get('owner')}{project.get('repo')}": metric_file.get(measure)})
                print(f"& ${metric_file.get(measure):.2g}$\t", end="")
            else:
                if p_values_list.get(f"{project.get('owner')}{project.get('repo')}") < p_cutoff:
                    if measure == "Cliff's Effect":
                        print(f"& {metric_file.get(measure)}\t", end="")
                    else:
                        print(f"& ${metric_file.get(measure):.2g}$\t", end="")
                else:
                    print("&\t", end="")

        if measure == "Glass' Delta" and file_metric != "Total comment length":
            print("\\\\ \\hline")
        else:
            print("\\\\")


for file_start in file_starts:
    start_table = """\\begin{landscape}
\\bgroup
\def\\arraystretch{1.5}
\\begin{table}[ht]
\\centering
\\begin{tabular}{c|c|c|c|c|c|c|c}"""

    end_table = """\\end{tabular}
\\caption{"""
    end_table += f"{file_start}"
    end_table += "}\n"
    end_table += """\\end{table}
\\egroup
\\end{landscape}"""

    print(start_table)
    print_header()
    for file_end, element_name in file_ends.items():
        print_metric(file_end, element_name)
    print(end_table)
    print("")
    print("")
