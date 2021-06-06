import kube_job_manager
import kube_task_spawner
import kube_scheduler
import time
import _thread

# algorithm list and current
ALGORITHM = "edf"
algorithms = ["edf", "sjf", "msf"]

DROP = True
drops = [True, False]

SIZE = 100
# sizes = [100, 1000]
sizes = [6, 2, 3]

SHAPE = "thin"
shapes = ["thin", "wide"]


def main():
    # start scheduler on a thread
    f = open("results.txt", "w")
    _thread.start_new_thread(kube_scheduler.main, ())
    node_count = kube_scheduler.nodes

    global ALGORITHM, SIZE, DROP, SHAPE
    # iterate through all the sizes
    for size in sizes:
        SIZE = size

        # iterate through all the algorithms
        for alg in algorithms:
            ALGORITHM = alg
            kube_scheduler.set_algo(ALGORITHM)

            # iterate through all the drop values
            for drop in drops:
                DROP = drop
                kube_scheduler.set_drop(drop)

                # iterate through all the shapes
                for shape in shapes:
                    SHAPE = shape

                    f.write("Size %d algorithm %s drop %s shape %s " % (SIZE, ALGORITHM, DROP, SHAPE))

                    start = time.time()

                    kube_scheduler.dropped_tasks = 0

                    # run a test with these parameters
                    kube_task_spawner.spawner(SIZE, SHAPE, node_count)

                    # Print collected results
                    total_time = time.time() - start
                    node_load = [str(round((x / total_time) * 100, 2)) + "%" for x in kube_job_manager.node_load]
                    f.write("Slack %f " % kube_job_manager.slack)
                    f.write("Runtime %d " % (total_time))
                    f.write("Dropped tasks %d " % kube_scheduler.dropped_tasks)
                    f.write("Node load " + str(node_load))
                    f.write("\n")

    f.close()


if __name__ == "__main__":
    main()
