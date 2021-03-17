from src.analysis import helpers
import matplotlib.pyplot as plt
import collections


def frequency_analysis(owner, repo, pr_type, frequencies, x_label, cut_offs):
    counter = collections.Counter(frequencies)
    sorted_counter = sorted(counter.items())

    file_name = str.lower(x_label[0]) + x_label[1:]
    file_name = file_name.replace(" ", "_")

    for cut_off in cut_offs:
        path = helpers.get_graph_path(owner, repo) + "/frequency/{pr_type}_{file_name}{cut_off}.png".format(
            owner=owner,
            repo=repo,
            pr_type=pr_type,
            file_name=file_name,
            cut_off=cut_off
        )
        if cut_off <= 20:
            create_frequency_bar_chart(sorted_counter, cut_off, True, x_label, path)
        else:
            create_frequency_bar_chart(sorted_counter, cut_off, False, x_label, path)


def create_frequency_bar_chart(sorted_counter, cut_off, is_every_tick, x_label, path):
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
