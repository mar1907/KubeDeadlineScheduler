import kube_job_manager
import kube_task_spawner
import kube_scheduler
import time
import _thread

# algorithm list and current
ALGORITHM = "edf"
# algorithms = ["edf", "sjf", "msf"]
# algorithms = ["edf", "lff", "sjaf", "sjf", "edf", "lff"]
# algorithms = ["hvf", "hvf_d"]
algorithms = {"dsc"}

DROP = True
# drops = [False, True]
drops = [False]

SIZE = 100
# sizes = [100, 1000]
# sizes = [30, 2, 3]
sizes = [1000]

SHAPE = "thin"
# shapes = ["thin", "wide"]
shapes = ["wide"]


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
                    print("Size %d algorithm %s drop %s shape %s " % (SIZE, ALGORITHM, DROP, SHAPE))

                    f.write("Size %d algorithm %s drop %s shape %s " % (SIZE, ALGORITHM, DROP, SHAPE))

                    start = time.time()

                    kube_scheduler.dropped_tasks = 0
                    kube_scheduler.reset_history()

                    # run a test with these parameters
                    kube_task_spawner.spawner(SIZE, SHAPE, node_count, fail_enabled=True)

                    # Print collected results
                    total_time = time.time() - start
                    node_load = [str(round((x / total_time) * 100, 2)) + "%" for x in kube_job_manager.node_load]
                    f.write("Slack %f " % kube_job_manager.slack)
                    f.write("Runtime %d " % (total_time))
                    f.write("Dropped tasks %d " % kube_job_manager.dropped)
                    f.write("Value %d " % kube_job_manager.value)
                    f.write("Node load " + str(node_load))
                    f.write("\n")

    f.close()


if __name__ == "__main__":
    main()
