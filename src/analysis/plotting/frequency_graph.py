from src.analysis import helpers
import matplotlib.pyplot as plt
import collections

def create_overlapping_histogram(owner, repo, data_set_name, x_label, bins, first_values, first_name, second_values,
                                 second_name, max_value=1.0):
    plt.hist(first_values, bins, alpha=0.5, label=first_name, color='blue', edgecolor="black", density=True)
    plt.hist(second_values, bins, alpha=0.5, label=second_name, color='green', edgecolor="black", density=True)
    plt.xlabel(x_label)
    plt.legend(loc='upper right')
    plt.ylim([0, max_value])

    plt.tight_layout(pad=0.04)
    plt.savefig(helpers.get_graph_path(owner, repo) + f"/frequency/{data_set_name}.png", transparent=True)

    plt.show()


def frequency_analysis(owner, repo, pr_type, frequencies, x_label, cut_offs):
    """
    Creates frequency bar charts for each element in @cut_offs.

    Parameters
    ----------
    owner : The owner of the repository.
    repo : The name of the repository.
    pr_type : The type of PR's where this is about (e.g. this can be about "bot_PRs")
    frequencies : The frequency which something occurred per element in @frequencies.
    x_label : The label to give to the x-axis in the resulting frequency bar chart.
    cut_offs : List containing values for which the graph will create an overflow bucket for the elements that have a
    greater value than the elements.

    Returns
    -------
    """
    counter = collections.Counter(frequencies)
    sorted_counter = sorted(counter.items())

    file_name = str.lower(x_label[0]) + x_label[1:]
    file_name = file_name.replace(" ", "_")

    for cut_off in cut_offs:
        path = helpers.get_graph_path(owner, repo) + "/frequency/{pr_type}_{file_name}{cut_off}.png".format(
            pr_type=pr_type,
            file_name=file_name,
            cut_off=cut_off
        )
        # If showing ticks for more than 20 consecutive buckets, the labels will overlap.
        if cut_off <= 20:
            create_frequency_bar_chart(sorted_counter, cut_off, True, x_label, path)
        else:
            create_frequency_bar_chart(sorted_counter, cut_off, False, x_label, path)


def create_frequency_bar_chart(sorted_counter, cut_off, is_every_tick, x_label, path):
    """
    Creates a frequency bar chart.

    Parameters
    ----------
    sorted_counter : The sorted counter that contains all the values that occur and how often they occurred.
    cut_off : The value after which all the values will be put in the overflow bucket.
    is_every_tick : Whether or not to show labels for the x-axis on every tick.
    x_label : The label to give to the x-axis.
    path : The path to save the resulting frequency bar chart.

    Returns
    -------
    """
    counter_with_cut_off = []
    for i in range(cut_off + 1):
        found_in_counter = False
        for pair in sorted_counter:
            if not found_in_counter and pair[0] == i:
                counter_with_cut_off.append((str(pair[0]), pair[1]))
                found_in_counter = True
        if not found_in_counter:
            counter_with_cut_off.append((str(i), 0))

    cut_offs = [count[1] for count in sorted_counter if count[0] > cut_off]
    counter_with_cut_off.append((f">{cut_off}", sum(cut_offs)))

    if is_every_tick:
        x_ticks = [str(possible_tick[0]) for possible_tick in counter_with_cut_off]
    else:
        x_ticks = [str(ele) for ele in range(cut_off) if ele % 5 == 0 and ele != cut_off]
        x_ticks.append(f">{cut_off}")

    x = [str(pair[0]) for pair in counter_with_cut_off]
    y = [pair[1] for pair in counter_with_cut_off]

    fig, ax1 = plt.subplots()

    plt.bar(x, y)
    plt.xlabel(x_label)
    plt.ylabel("Frequency")

    ax1.xaxis.set_ticks(x_ticks)

    plt.tight_layout(pad=0.04)
    plt.savefig(path, transparent=True)

    plt.show()
