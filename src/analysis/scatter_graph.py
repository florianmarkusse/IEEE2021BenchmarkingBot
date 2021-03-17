from src.analysis import helpers
import matplotlib.pyplot as plt


def scatter_contributor_bot(owner, repo, summaries, cut_off, x_label, y_label):
    significant_summaries = [summary for summary in summaries if
                             summary["all_prs"] >= cut_off]

    significant_summaries_fraction = [summary["fraction"] for summary in significant_summaries]
    significant_summaries_total_prs = [summary["all_prs"] for summary in significant_summaries]

    plt.xlim(left=0, right=1.0)

    plt.scatter(significant_summaries_fraction, significant_summaries_total_prs)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    file_name = str.lower(x_label[0]) + x_label[1:] + "_" + str.lower(y_label[0]) + y_label[1:]
    file_name = file_name.replace(" ", "_")

    plt.tight_layout(pad=0)
    plt.savefig(helpers.get_graph_path(owner, repo) + f"/scatter/{file_name}{cut_off}.png", transparent=True)

    plt.show()
