import kube_job_manager
import kube_scheduler
import test_case
import jinja2
import time
import os
import fail


templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template("sleep.yaml.j2")


def spawner(tasks, shape, nodes, fail_enabled=False):
    print("Start spawner")
    kube_job_manager.init_manager()
    imp = __import__(shape)
    test_array = imp.test_array

    fail_array = fail.fail_array

    for i in range(0, min(len(test_array), tasks)):
        triple = test_array[i]
        filename = "sleep" + str(i)
        time.sleep(triple[0] / nodes)
        # print("Pushing task %s" % filename)
        if fail_enabled:
            outputText = template.render(deadline=triple[2] + time.time(), runtime=triple[1], number=i, failure=fail_array[i])
        else:
            outputText = template.render(deadline=triple[2] + time.time(), runtime=triple[1], number=i)

        f = open(filename + ".yaml", "w")
        f.write(outputText)
        f.close()

        kube_job_manager.add_job(filename)

    while True:
        time.sleep(10)
        if not os.popen('kubectl get pods').read().split():
            break

    kube_job_manager.stop_manager()

    time.sleep(2)
