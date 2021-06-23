class PodObject:
    def __init__(self, name, runtime, deadline):
        self.name = name
        self.runtime = runtime
        self.deadline = deadline

        self.finish_time = 0
        self.value = 0
        self.mark = 0

    def get_latest_starttime(self):
        # -1 to account for delays
        return self.deadline - self.runtime - 1

    def get_delay(self):
        sleep = self.name.split("-")[0]
        nr = int(sleep[5:])
        return 1 + round(nr/100)

    def __str__(self):
        return str(round(self.runtime))[-3:] + " " + self.name + " " + str(round(self.finish_time))[-3:] + " " + str(round(self.deadline))[-3:]

    def __repr__(self):
        return str(round(self.runtime))[-3:] + " " + self.name + " " + str(round(self.finish_time))[-3:] + " " + str(round(self.deadline))[-3:]

    def __hash__(self):
        return self.name

    def __eq__(self, other):
        return other and self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)