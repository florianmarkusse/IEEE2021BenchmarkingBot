import matplotlib.pyplot as plt
from src.analysis import helpers


def boxplot(owner, repo, data, file_name):
    fig1, ax1 = plt.subplots()
    green_diamond = dict(markerfacecolor='g', marker='D')
    ax1.boxplot(data, flierprops=green_diamond)

    plt.xticks([])

    plt.tight_layout(pad=0.1)
    plt.savefig(helpers.get_graph_path(owner, repo) + f"/boxplot/{file_name}.png", transparent=True)

    plt.show()

