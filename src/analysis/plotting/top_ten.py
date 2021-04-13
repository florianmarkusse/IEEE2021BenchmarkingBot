import matplotlib.pyplot as plt

from src.analysis.helpers import get_graph_path
from src.utility.file_management import get_projects_to_mine
from src.utility.helpers import categorize_prs


def create_top_ten_prs(owner, repo, data_set_name, prs, categorized_prs, pr_type, attribute_label):
    attribute_occurrence_normalized = {}
    for category in categorized_prs:
        attribute_occurrence_normalized[category] = len(categorized_prs[category]) / len(prs)

    descending_attributes_normalized = {key: val for key, val in
                                        sorted(attribute_occurrence_normalized.items(), key=lambda ele: ele[1],
                                               reverse=True)}

    print(descending_attributes_normalized)

    top_ten_attribute_occurrences_normalized = {}

    for attribute in list(descending_attributes_normalized)[0:10]:
        top_ten_attribute_occurrences_normalized[attribute] = descending_attributes_normalized[attribute]

    top_attributes = list(top_ten_attribute_occurrences_normalized.keys())
    top_normalized_values = list(top_ten_attribute_occurrences_normalized.values())

    # Reverse them so highest value is on top.
    top_attributes = list(reversed(top_attributes))
    top_normalized_values = list(reversed(top_normalized_values))

    plt.barh(top_attributes, top_normalized_values)
    plt.ylabel("Top " + attribute_label)
    plt.xlabel('Normalized frequency')

    plt.xlim(left=0.0, right=1.0)

    pr_type = str.lower(pr_type)
    pr_type = pr_type.replace(" ", "_")

    path = get_graph_path(owner, repo) + f"/top_ten/{data_set_name}_{pr_type}_{attribute_label}.png"

    plt.tight_layout(pad=0.04)
    plt.savefig(path, transparent=True)

    plt.show()
