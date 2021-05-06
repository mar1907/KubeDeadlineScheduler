import kube_job_manager
import kube_task_spawner
import kube_scheduler
import time

# algorithm list and current
ALGORITHM = "edf"
algorithms = ["edf", "sjf", "msf"]

DROP = False
drops = [True, False]

SIZE = 100
sizes = [100, 10000, 1000000]

SHAPE = "thin"
shapes = ["thin", "wide"]


def main():
    # start scheduler on a thread
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

                    start = time.time()

                    kube_scheduler.dropped_tasks = 0

                    # run a test with these parameters
                    kube_task_spawner.spawner(SIZE, SHAPE)

                    # Print collected results
                    print("Size %d algorithm %s drop %s shape %s" % (SIZE, ALGORITHM, DROP, SHAPE))
                    print("Slack %d" % kube_job_manager.slack)
                    print("Runtime %d" % (time.time() - start))
                    print("Dropped tasks %d" % kube_scheduler.dropped_tasks)
                    print("\n")


if __name__ == "__main__":
    main()
