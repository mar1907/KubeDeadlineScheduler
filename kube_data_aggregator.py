import matplotlib.pyplot as plt

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

plt.plot(datax, sjf1, marker=".", linestyle="--", label="N=1")
plt.plot(datax, sjf2, marker=".", linestyle="--", label="N=2")
plt.plot(datax, sjf3, marker=".", linestyle="--", label="N=4")
plt.xticks(datax, datax)
plt.title("Node comparison")
plt.legend()
plt.xlabel("Jobs")
plt.ylabel("Slack")
plt.show()
