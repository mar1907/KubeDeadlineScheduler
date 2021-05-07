import kube_job_manager
import kube_task_spawner
import kube_scheduler
import time
import thread

# algorithm list and current
ALGORITHM = "edf"
algorithms = ["edf", "sjf", "msf"]

DROP = True
drops = [True, False]

SIZE = 100
sizes = [100, 1000, 5000]
# sizes = [1, 2, 3]

SHAPE = "thin"
shapes = ["thin", "wide"]


def main():
    # start scheduler on a thread
    f = open("results.txt", "w")
    thread.start_new_thread(kube_scheduler.main, ())

    global ALGORITHM, SIZE, DROP, SHAPE
    # iterate through all the sizes
    for size in sizes:
        SIZE = size

        # iterate through all the algorithms
        for alg in algorithms:
            ALGORITHM = alg

            # iterate through all the drop values
            for drop in drops:
                DROP = drop

                # iterate through all the shapes
                for shape in shapes:
                    SHAPE = shape

                    f.write("Size %d algorithm %s drop %s shape %s " % (SIZE, ALGORITHM, DROP, SHAPE))

                    start = time.time()

                    kube_scheduler.dropped_tasks = 0

                    # run a test with these parameters
                    kube_task_spawner.spawner(SIZE, SHAPE)

                    # Print collected results
                    f.write("Slack %f " % kube_job_manager.slack)
                    f.write("Runtime %d " % (time.time() - start))
                    f.write("Dropped tasks %d " % kube_scheduler.dropped_tasks)
                    f.write("\n")

    f.close()


if __name__ == "__main__":
    main()
