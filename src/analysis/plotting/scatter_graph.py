from src.analysis import helpers
import matplotlib.pyplot as plt


def scatter_graph(owner, repo, x_distribution, y_distribution, x_min, x_max, x_label, y_label):
    """
    Creates a scatter plot out of the elements in @summaries that are above the @cut_off with their "all_prs" member.

    Parameters
    ----------
    owner : The owner of the repository.
    repo : The name of the repository.
    x_label : The label to give the x-axis.
    y_label : The label to give the y-axis.

    Returns
    -------
    """
    if x_min is None:
        x_min = min(x_distribution)
    if x_max is None:
        x_max = max(x_distribution)
    plt.xlim(left=x_min, right=x_max)

    plt.scatter(x_distribution, y_distribution)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    file_name = str.lower(x_label[0]) + x_label[1:] + "_" + str.lower(y_label[0]) + y_label[1:]
    file_name = file_name.replace(" ", "_")

    plt.tight_layout(pad=0.1)
    plt.savefig(helpers.get_graph_path(owner, repo) + f"/scatter/{file_name}{cut_off}.png", transparent=True)

    plt.show()
