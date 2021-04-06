import matplotlib.pyplot as plt
from src.analysis import helpers


def pie_chart(owner, repo, labels, colors, values, explode, file_title):
    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels=labels, labeldistance=None, explode=explode, radius=0.1, autopct='%1.0f%%',
            startangle=90, colors=colors)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.savefig(helpers.get_graph_path(owner, repo) + f"/pie/{file_title}.png", transparent=True)

    plt.show()
