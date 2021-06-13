import matplotlib.pyplot as plt
import numpy as np

edf1 = [-90, -536, -2897, -14198]
sjf1 = [-80, -394, -2091, -9872]
msf1 = [-143, -654, -3581, -14323]
minsf1 = [-131, -648, -3532, -15038]

edf2 = [7, -248, -1562, -7642]
sjf2 = [-1, -179, -1094, -5311]
msf2 = [-20, -300, -1776, -8619]
minsf2 = [-20, -331, -1859, -8126]

edf3 = [48, -46, -578, -3951]
sjf3 = [48, -36, -398, -2520]
msf3 = [48, -82, -620, -4048]
minsf3 = [47, -68, -677, -3822]

datax = [10, 20, 50, 100]

slack_drop_thin_1 = [6341.16, 6648.64, 6775.77]
slack_drop_wide_1 = [4645.21, 5004.75, 5210.12]
slack_ndrop_thin_1 = [4156.67, 4985.63, 5299.80]
slack_ndrop_wide_1 = [-16789.13, -9964.91, -6769.86]

runtime_drop_thin_1 = [5363, 5559, 5613]
runtime_drop_wide_1 = [5755, 6107, 6229]
runtime_ndrop_thin_1 = [5663, 5922, 5928]
runtime_ndrop_wide_1 = [8048, 8111, 8129]

drop_thin_1 = [157, 156, 151]
drop_wide_1 = [346, 328, 322]

slack_drop_thin_2 = [7480.04, 7349.26, 7140.98]
slack_drop_wide_2 = [6280.4, 6440.95, 6359.30]
slack_ndrop_thin_2 = [6969.21, 6762.21, 6266.62]
slack_ndrop_wide_2 = [4151.51, 4658.84, 4821.9]

runtime_drop_thin_2 = [3225, 3396, 3642]
runtime_drop_wide_2 = [3786, 4034, 4352]
runtime_ndrop_thin_2 = [3431, 3679, 4110]
runtime_ndrop_wide_2 = [4379, 4567, 4864]

drop_thin_2 = [94, 98, 120]
drop_wide_2 = [195, 192, 194]

load_drop_thin_2 = [[0.79, 0.76, 0.74], [0.7, 0.65, 0.56]]
load_drop_wide_2 = [[0.89, 0.86, 0.83], [0.84, 0.79, 0.7]]
load_ndrop_thin_2 = [[0.8, 0.78, 0.76], [0.75, 0.68, 0.58]]
load_ndrop_wide_2 = [[0.94, 0.92, 0.89], [0.93, 0.88, 0.82]]

slack_drop_thin_4 = [7098.55, 7082.01, 6845.04]
slack_drop_wide_4 = [6721.45, 6808.68, 6660.97]
slack_ndrop_thin_4 = [6658.79, 6450.06, 6217.83]
slack_ndrop_wide_4 = [6189.26, 5953.99, 5600.71]

runtime_drop_thin_4 = [2574, 2681, 2911]
runtime_drop_wide_4 = [3221, 3237, 3459]
runtime_ndrop_thin_4 = [2776, 3011, 3248]
runtime_ndrop_wide_4 = [3381, 3662, 3982]

drop_thin_4 = [120, 117, 126]
drop_wide_4 = [157, 154, 174]

load_drop_thin_4 = [[0.75, 0.77, 0.73], [0.65, 0.65, 0.62], [0.4, 0.3, 0.24], [0.06, 0.03, 0]]
load_drop_wide_4 = [[0.8, 0.8, 0.77], [0.71, 0.68, 0.67], [0.5, 0.53, 0.47], [0.2, 0.18, 0.09]]
load_ndrop_thin_4 = [[0.78, 0.76, 0.75], [0.69, 0.67, 0.66], [0.42, 0.34, 0.25], [0.06, 0.01, 0]]
load_ndrop_wide_4 = [[0.81, 0.81, 0.8], [0.74, 0.72, 0.69], [0.61, 0.54, 0.5], [0.3, 0.18, 0.11]]

fail_slack_4 = [-66640, -66177, -66018, -58363]
fail_objects = ("SJAF", "SJF", "EDF", "LFF")
y_pos_fail = np.arange(len(fail_objects))

objects = ("EDF", "SJF", "MSF")
y_pos = np.arange(len(objects))

# plt.plot(datax, edf3, marker=".", linestyle="--", label="EDF")
# plt.plot(datax, sjf3, marker=".", linestyle="--", label="SJF")
# plt.plot(datax, msf3, marker=".", linestyle="--", label="MSF")
# plt.plot(datax, minsf3, marker=".", linestyle="--", label="MinSF")
# plt.xticks(datax, datax)
# plt.title("Algorithm comparison")
# plt.legend()
# plt.xlabel("Jobs")
# plt.ylabel("Slack")
# plt.show()

# plt.plot(datax, sjf1, marker=".", linestyle="--", label="N=1")
# plt.plot(datax, sjf2, marker=".", linestyle="--", label="N=2")
# plt.plot(datax, sjf3, marker=".", linestyle="--", label="N=4")
# plt.xticks(datax, datax)
# plt.title("Node comparison")
# plt.legend()
# plt.xlabel("Jobs")
# plt.ylabel("Slack")
# plt.show()

def gen_slack_1():
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    fig.tight_layout()
    fig.subplots_adjust(wspace=.3, top=.95)
    ax1.bar(y_pos, slack_drop_thin_1, width=0.5, color=['blue', 'orange', 'green'])
    ax1.set_xticks(y_pos, minor=False)
    ax1.set_xticklabels(objects, fontdict=None, minor=False)
    ax1.set_ylabel("Slack (s)")
    ax1.set_title("Drop, Thin")

    ax2.bar(y_pos, slack_drop_wide_1, width=0.5, color=['blue', 'orange', 'green'])
    ax2.set_xticks(y_pos, minor=False)
    ax2.set_xticklabels(objects, fontdict=None, minor=False)
    ax2.set_title("Drop, Wide")

    ax3.bar(y_pos, slack_ndrop_thin_1, width=0.5, color=['blue', 'orange', 'green'])
    ax3.set_xticks(y_pos, minor=False)
    ax3.set_xticklabels(objects, fontdict=None, minor=False)
    ax3.set_ylabel("Slack (s)")
    ax3.set_title("No Drop, Thin")

    ax4.bar(y_pos, slack_ndrop_wide_1, width=0.5, color=['blue', 'orange', 'green'])
    ax4.set_xticks(y_pos, minor=False)
    ax4.set_xticklabels(objects, fontdict=None, minor=False)
    ax4.set_title("No Drop, Wide")

    plt.savefig("graph_slack1.png")

def gen_runtime_1():
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    fig.tight_layout()
    fig.subplots_adjust(wspace=.3, top=.95)
    ax1.bar(y_pos, runtime_drop_thin_1, width=0.5, color=['blue', 'orange', 'green'])
    ax1.set_xticks(y_pos, minor=False)
    ax1.set_xticklabels(objects, fontdict=None, minor=False)
    ax1.set_ylabel("Runtime (s)")
    ax1.set_title("Drop, Thin")

    ax2.bar(y_pos, runtime_drop_wide_1, width=0.5, color=['blue', 'orange', 'green'])
    ax2.set_xticks(y_pos, minor=False)
    ax2.set_xticklabels(objects, fontdict=None, minor=False)
    ax2.set_title("Drop, Wide")

    ax3.bar(y_pos, runtime_ndrop_thin_1, width=0.5, color=['blue', 'orange', 'green'])
    ax3.set_xticks(y_pos, minor=False)
    ax3.set_xticklabels(objects, fontdict=None, minor=False)
    ax3.set_ylabel("Runtime (s)")
    ax3.set_title("No Drop, Thin")

    ax4.bar(y_pos, runtime_ndrop_wide_1, width=0.5, color=['blue', 'orange', 'green'])
    ax4.set_xticks(y_pos, minor=False)
    ax4.set_xticklabels(objects, fontdict=None, minor=False)
    ax4.set_title("No Drop, Wide")

    plt.savefig("graph_runtime1.png")

def gen_drop_1():
    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    fig.tight_layout()
    fig.subplots_adjust(top=.95)
    ax1.bar(y_pos, drop_thin_1, width=0.5, color=['blue', 'orange', 'green'])
    ax1.set_xticks(y_pos, minor=False)
    ax1.set_xticklabels(objects, fontdict=None, minor=False)
    ax1.set_ylabel("Dropped jobs")
    ax1.set_title("Drop, Thin")

    ax2.bar(y_pos, drop_wide_1, width=0.5, color=['blue', 'orange', 'green'])
    ax2.set_xticks(y_pos, minor=False)
    ax2.set_xticklabels(objects, fontdict=None, minor=False)
    ax2.set_title("Drop, Wide")

    plt.savefig("graph_drop1.png")

def gen_slack_2():
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    fig.tight_layout()
    fig.subplots_adjust(wspace=.3, top=.95)
    ax1.bar(y_pos, slack_drop_thin_2, width=0.5, color=['blue', 'orange', 'green'])
    ax1.set_xticks(y_pos, minor=False)
    ax1.set_xticklabels(objects, fontdict=None, minor=False)
    ax1.set_ylabel("Slack (s)")
    ax1.set_title("Drop, Thin")

    ax2.bar(y_pos, slack_drop_wide_2, width=0.5, color=['blue', 'orange', 'green'])
    ax2.set_xticks(y_pos, minor=False)
    ax2.set_xticklabels(objects, fontdict=None, minor=False)
    ax2.set_title("Drop, Wide")

    ax3.bar(y_pos, slack_ndrop_thin_2, width=0.5, color=['blue', 'orange', 'green'])
    ax3.set_xticks(y_pos, minor=False)
    ax3.set_xticklabels(objects, fontdict=None, minor=False)
    ax3.set_ylabel("Slack (s)")
    ax3.set_title("No Drop, Thin")

    ax4.bar(y_pos, slack_ndrop_wide_2, width=0.5, color=['blue', 'orange', 'green'])
    ax4.set_xticks(y_pos, minor=False)
    ax4.set_xticklabels(objects, fontdict=None, minor=False)
    ax4.set_title("No Drop, Wide")

    plt.savefig("graph_slack2.png")

def gen_runtime_2():
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    fig.tight_layout()
    fig.subplots_adjust(wspace=.3, top=.95)
    ax1.bar(y_pos, runtime_drop_thin_2, width=0.5, color=['blue', 'orange', 'green'])
    ax1.set_xticks(y_pos, minor=False)
    ax1.set_xticklabels(objects, fontdict=None, minor=False)
    ax1.set_ylabel("Runtime (s)")
    ax1.set_title("Drop, Thin")

    ax2.bar(y_pos, runtime_drop_wide_2, width=0.5, color=['blue', 'orange', 'green'])
    ax2.set_xticks(y_pos, minor=False)
    ax2.set_xticklabels(objects, fontdict=None, minor=False)
    ax2.set_title("Drop, Wide")

    ax3.bar(y_pos, runtime_ndrop_thin_2, width=0.5, color=['blue', 'orange', 'green'])
    ax3.set_xticks(y_pos, minor=False)
    ax3.set_xticklabels(objects, fontdict=None, minor=False)
    ax3.set_ylabel("Runtime (s)")
    ax3.set_title("No Drop, Thin")

    ax4.bar(y_pos, runtime_ndrop_wide_2, width=0.5, color=['blue', 'orange', 'green'])
    ax4.set_xticks(y_pos, minor=False)
    ax4.set_xticklabels(objects, fontdict=None, minor=False)
    ax4.set_title("No Drop, Wide")

    plt.savefig("graph_runtime2.png")

def gen_drop_2():
    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    fig.tight_layout()
    fig.subplots_adjust(top=.95)
    ax1.bar(y_pos, drop_thin_2, width=0.5, color=['blue', 'orange', 'green'])
    ax1.set_xticks(y_pos, minor=False)
    ax1.set_xticklabels(objects, fontdict=None, minor=False)
    ax1.set_ylabel("Dropped jobs")
    ax1.set_title("Drop, Thin")

    ax2.bar(y_pos, drop_wide_2, width=0.5, color=['blue', 'orange', 'green'])
    ax2.set_xticks(y_pos, minor=False)
    ax2.set_xticklabels(objects, fontdict=None, minor=False)
    ax2.set_title("Drop, Wide")

    plt.savefig("graph_drop2.png")

def gen_load_2():
    width = 0.25
    nodes = 2
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    fig.tight_layout()
    fig.subplots_adjust(wspace=.1, top=.95)
    ax1.bar(y_pos, load_drop_thin_2[0], width, color="C4", label="Node 1")
    ax1.bar(y_pos + width, load_drop_thin_2[1], width, color="C5", label="Node 2")
    ax1.set_xticks(y_pos + width/nodes, minor=False)
    ax1.set_xticklabels(objects, fontdict=None, minor=False)
    ax1.set_ylabel("Load (%)")
    ax1.set_title("Drop, Thin")

    ax2.bar(y_pos, load_drop_wide_2[0], width, color="C4")
    ax2.bar(y_pos + width, load_drop_wide_2[1], width, color="C5")
    ax2.set_xticks(y_pos + width/nodes, minor=False)
    ax2.set_xticklabels(objects, fontdict=None, minor=False)
    ax2.set_title("Drop, Wide")

    ax3.bar(y_pos, load_ndrop_thin_2[0], width, color="C4")
    ax3.bar(y_pos + width, load_ndrop_thin_2[1], width, color="C5")
    ax3.set_xticks(y_pos + width/nodes, minor=False)
    ax3.set_xticklabels(objects, fontdict=None, minor=False)
    ax3.set_ylabel("Load (%)")
    ax3.set_title("No Drop, Thin")

    ax4.bar(y_pos, load_ndrop_wide_2[0], width, color="C4")
    ax4.bar(y_pos + width, load_ndrop_wide_2[1], width, color="C5")
    ax4.set_xticks(y_pos + width/nodes, minor=False)
    ax4.set_xticklabels(objects, fontdict=None, minor=False)
    ax4.set_title("No Drop, Wide")

    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center')
    # plt.legend()

    plt.savefig("graph_load2.png")

def gen_slack_4():
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    fig.tight_layout()
    fig.subplots_adjust(wspace=.3, top=.95)
    ax1.bar(y_pos, slack_drop_thin_4, width=0.5, color=['blue', 'orange', 'green'])
    ax1.set_xticks(y_pos, minor=False)
    ax1.set_xticklabels(objects, fontdict=None, minor=False)
    ax1.set_ylabel("Slack (s)")
    ax1.set_title("Drop, Thin")

    ax2.bar(y_pos, slack_drop_wide_4, width=0.5, color=['blue', 'orange', 'green'])
    ax2.set_xticks(y_pos, minor=False)
    ax2.set_xticklabels(objects, fontdict=None, minor=False)
    ax2.set_title("Drop, Wide")

    ax3.bar(y_pos, slack_ndrop_thin_4, width=0.5, color=['blue', 'orange', 'green'])
    ax3.set_xticks(y_pos, minor=False)
    ax3.set_xticklabels(objects, fontdict=None, minor=False)
    ax3.set_ylabel("Slack (s)")
    ax3.set_title("No Drop, Thin")

    ax4.bar(y_pos, slack_ndrop_wide_4, width=0.5, color=['blue', 'orange', 'green'])
    ax4.set_xticks(y_pos, minor=False)
    ax4.set_xticklabels(objects, fontdict=None, minor=False)
    ax4.set_title("No Drop, Wide")

    plt.savefig("graph_slack4.png")

def gen_runtime_4():
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    fig.tight_layout()
    fig.subplots_adjust(wspace=.3, top=.95)
    ax1.bar(y_pos, runtime_drop_thin_4, width=0.5, color=['blue', 'orange', 'green'])
    ax1.set_xticks(y_pos, minor=False)
    ax1.set_xticklabels(objects, fontdict=None, minor=False)
    ax1.set_ylabel("Runtime (s)")
    ax1.set_title("Drop, Thin")

    ax2.bar(y_pos, runtime_drop_wide_4, width=0.5, color=['blue', 'orange', 'green'])
    ax2.set_xticks(y_pos, minor=False)
    ax2.set_xticklabels(objects, fontdict=None, minor=False)
    ax2.set_title("Drop, Wide")

    ax3.bar(y_pos, runtime_ndrop_thin_4, width=0.5, color=['blue', 'orange', 'green'])
    ax3.set_xticks(y_pos, minor=False)
    ax3.set_xticklabels(objects, fontdict=None, minor=False)
    ax3.set_ylabel("Runtime (s)")
    ax3.set_title("No Drop, Thin")

    ax4.bar(y_pos, runtime_ndrop_wide_4, width=0.5, color=['blue', 'orange', 'green'])
    ax4.set_xticks(y_pos, minor=False)
    ax4.set_xticklabels(objects, fontdict=None, minor=False)
    ax4.set_title("No Drop, Wide")

    plt.savefig("graph_runtime4.png")

def gen_drop_4():
    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    fig.tight_layout()
    fig.subplots_adjust(top=.95)
    ax1.bar(y_pos, drop_thin_4, width=0.5, color=['blue', 'orange', 'green'])
    ax1.set_xticks(y_pos, minor=False)
    ax1.set_xticklabels(objects, fontdict=None, minor=False)
    ax1.set_ylabel("Dropped jobs")
    ax1.set_title("Drop, Thin")

    ax2.bar(y_pos, drop_wide_4, width=0.5, color=['blue', 'orange', 'green'])
    ax2.set_xticks(y_pos, minor=False)
    ax2.set_xticklabels(objects, fontdict=None, minor=False)
    ax2.set_title("Drop, Wide")

    plt.savefig("graph_drop4.png")

def gen_load_4():
    width = 0.2
    nodes = 4
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    fig.tight_layout()
    fig.subplots_adjust(wspace=.3, top=.95)
    ax1.bar(y_pos, load_drop_thin_4[0], width, color="C4", label="Node 1")
    ax1.bar(y_pos + width, load_drop_thin_4[1], width, color="C5", label="Node 2")
    ax1.bar(y_pos + 2*width, load_drop_thin_4[2], width, color="C6", label="Node 3")
    ax1.bar(y_pos + 3*width, load_drop_thin_4[3], width, color="C7", label="Node 4")
    ax1.set_xticks(y_pos + width * 3/2, minor=False)
    ax1.set_xticklabels(objects, fontdict=None, minor=False)
    ax1.set_ylabel("Load (%)")
    ax1.set_title("Drop, Thin")

    ax2.bar(y_pos, load_drop_wide_4[0], width, color="C4")
    ax2.bar(y_pos + width, load_drop_wide_4[1], width, color="C5")
    ax2.bar(y_pos + 2*width, load_drop_wide_4[2], width, color="C6")
    ax2.bar(y_pos + 3*width, load_drop_wide_4[3], width, color="C7")
    ax2.set_xticks(y_pos + width * 3/2, minor=False)
    ax2.set_xticklabels(objects, fontdict=None, minor=False)
    ax2.set_title("Drop, Wide")

    ax3.bar(y_pos, load_ndrop_thin_4[0], width, color="C4")
    ax3.bar(y_pos + width, load_ndrop_thin_4[1], width, color="C5")
    ax3.bar(y_pos + 2*width, load_ndrop_thin_4[2], width, color="C6")
    ax3.bar(y_pos + 3*width, load_ndrop_thin_4[3], width, color="C7")
    ax3.set_xticks(y_pos + width * 3/2, minor=False)
    ax3.set_xticklabels(objects, fontdict=None, minor=False)
    ax3.set_ylabel("Load (%)")
    ax3.set_title("No Drop, Thin")

    ax4.bar(y_pos, load_ndrop_wide_4[0], width, color="C4")
    ax4.bar(y_pos + width, load_ndrop_wide_4[1], width, color="C5")
    ax4.bar(y_pos + 2*width, load_ndrop_wide_4[2], width, color="C6")
    ax4.bar(y_pos + 3*width, load_ndrop_wide_4[3], width, color="C7")
    ax4.set_xticks(y_pos + width * 3/2, minor=False)
    ax4.set_xticklabels(objects, fontdict=None, minor=False)
    ax4.set_title("No Drop, Wide")

    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center')
    # plt.legend()

    plt.savefig("graph_load4.png")

def gen_slack_fail_4():
    plt.tight_layout()
    plt.gcf().subplots_adjust(left=.15, top=.95)
    plt.bar(y_pos_fail, fail_slack_4, width=0.5, color=['blue', 'orange', 'green', 'red'])
    plt.xticks(y_pos_fail, fail_objects)
    plt.ylabel("Slack (s)")
    plt.title("Fail model")

    plt.savefig("graph_slack_fail4.png")


# gen_slack_1()
# gen_runtime_1()
# gen_drop_1()

# gen_slack_2()
# gen_runtime_2()
# gen_drop_2()
# gen_load_2()

# gen_slack_4()
# gen_runtime_4()
# gen_drop_4()
# gen_load_4()

gen_slack_fail_4()