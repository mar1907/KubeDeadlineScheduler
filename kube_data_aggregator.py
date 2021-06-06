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
    ax1.set_ylabel("Slack")
    ax1.set_title("Drop, Thin")

    ax2.bar(y_pos, slack_drop_wide_1, width=0.5, color=['blue', 'orange', 'green'])
    ax2.set_xticks(y_pos, minor=False)
    ax2.set_xticklabels(objects, fontdict=None, minor=False)
    ax2.set_title("Drop, Wide")

    ax3.bar(y_pos, slack_ndrop_thin_1, width=0.5, color=['blue', 'orange', 'green'])
    ax3.set_xticks(y_pos, minor=False)
    ax3.set_xticklabels(objects, fontdict=None, minor=False)
    ax3.set_ylabel("Slack")
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
    ax1.set_ylabel("Runtime")
    ax1.set_title("Drop, Thin")

    ax2.bar(y_pos, runtime_drop_wide_1, width=0.5, color=['blue', 'orange', 'green'])
    ax2.set_xticks(y_pos, minor=False)
    ax2.set_xticklabels(objects, fontdict=None, minor=False)
    ax2.set_title("Drop, Wide")

    ax3.bar(y_pos, runtime_ndrop_thin_1, width=0.5, color=['blue', 'orange', 'green'])
    ax3.set_xticks(y_pos, minor=False)
    ax3.set_xticklabels(objects, fontdict=None, minor=False)
    ax3.set_ylabel("Runtime")
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


gen_slack_1()
gen_runtime_1()
gen_drop_1()