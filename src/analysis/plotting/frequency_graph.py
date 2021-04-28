import collections

import matplotlib.pyplot as plt
import numpy as np

from src.analysis import helpers


def create_overlapping_histogram_step(owner, repo, data_set_name, x_label, overflow_value, first_values, first_name,
                                      second_values=None, second_name=None, max_value=1.0, step_size=1, tick_frequency=1):
    bins = list(np.linspace(0, overflow_value, num=round(overflow_value/step_size) + 1))

    first_values = np.clip(first_values, bins[0], bins[-1])

    first_density, first_bins = np.histogram(first_values, density=True, bins=bins)
    first_unity_density = first_density / first_density.sum()
    first_widths = first_bins[:-1] - first_bins[1:]

    plt.bar(first_bins[1:], first_unity_density, width=first_widths, label=first_name, color="blue", alpha=0.5, edgecolor="black", align="edge")

    if second_values is not None:
        second_values = np.clip(second_values, bins[0], bins[-1])

        second_density, second_bins = np.histogram(second_values, density=True, bins=bins)
        second_unity_density = second_density / second_density.sum()
        second_widths = second_bins[:-1] - second_bins[1:]

        plt.bar(second_bins[1:], second_unity_density, width=second_widths, label=second_name, color="green", alpha=0.5, edgecolor="black", align="edge")

    N_ticks = round(overflow_value / step_size / tick_frequency + 1)

    ticks = [round(tick * step_size * tick_frequency, 1) for tick in range(N_ticks)]

    str_ticks = [str(tick) for tick in ticks]
    str_ticks[-1] += "+"

    plt.xticks(ticks=ticks, labels=str_ticks)

    plt.legend(loc='upper right', fontsize=20)
    plt.ylim([0, max_value])

    plt.xlabel(x_label)
    plt.xlabel(x_label, size=24)

    plt.xticks(size=16)
    plt.yticks(size=16)

    plt.tight_layout(pad=0.04)
    plt.savefig(helpers.get_graph_path(owner, repo) + f"/frequency/{data_set_name}_{x_label.replace(' ', '_')}.png",
                transparent=True)

    plt.show()


def create_overlapping_histogram(owner, repo, data_set_name, x_label, overflow_value, first_values, first_name,
                                 second_values=None, second_name=None, max_value=1.0, overflow=False, tick_frequency=5,
                                 is_step=False, density=True, step_size=1):
    if overflow:
        bins = range(0, overflow_value + 2, step_size)

        if is_step:
            plt.hist(np.clip(first_values, bins[0], bins[-1] - 1), bins, label=first_name, color='blue',
                     density=density, histtype='step')
            if second_values is not None:
                plt.hist(np.clip(second_values, bins[0], bins[-1] - 1), bins, label=second_name, color='green',
                         density=density, histtype='step')
        else:
            plt.hist(np.clip(first_values, bins[0], bins[-1] - 1), bins, alpha=0.5, label=first_name, color='blue',
                     edgecolor="black", density=density)
            if second_values is not None:
                plt.hist(np.clip(second_values, bins[0], bins[-1] - 1), bins, alpha=0.5, label=second_name,
                         color='green',
                         edgecolor="black", density=density)

        x_labels = [str(i) for i in bins]
        del x_labels[-1]

        x_labels_frequency = [x_label for x_label in x_labels if int(x_label) % tick_frequency == 0]
        if int(x_labels_frequency[-1]) > 1000:
            x_labels_frequency_scientific = []
            for label in x_labels_frequency:
                number = label[0]
                x_labels_frequency_scientific.append(number)
            x_labels_frequency = x_labels_frequency_scientific
        x_labels_frequency[-1] += '+'
        N_labels = len(x_labels) / tick_frequency
        plt.xlim([0 - 0.5, max(bins) + 0.5])
        plt.xticks(tick_frequency * np.arange(N_labels) + 0.5, x_labels_frequency)
    else:
        bins = range(0, overflow_value + 2, step_size)

        if is_step:
            plt.hist(first_values, [bucket - 0.5 for bucket in bins], label=first_name, color='blue',
                     density=density, histtype='step')
            if second_values is not None:
                plt.hist(second_values, [bucket - 0.5 for bucket in bins], label=second_name, color='green',
                         density=density, histtype='step')
        else:
            plt.hist(first_values, [bucket - 0.5 for bucket in bins], alpha=0.5, label=first_name, color='blue',
                     edgecolor="black", density=density)
            if second_values is not None:
                plt.hist(second_values, [bucket - 0.5 for bucket in bins], alpha=0.5, label=second_name, color='green',
                         edgecolor="black", density=density)

    plt.xlabel(x_label)
    plt.xlabel(x_label, size=24)

    plt.xticks(size=20)
    plt.yticks(size=20)
    plt.legend(loc='upper right', fontsize=20)
    plt.ylim([0, max_value])

    plt.tight_layout(pad=0.04)
    plt.savefig(helpers.get_graph_path(owner, repo) + f"/frequency/{data_set_name}_{x_label.replace(' ', '_')}.png",
                transparent=True)

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