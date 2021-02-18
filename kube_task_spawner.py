import kube_job_manager
import test_case
import jinja2
import time
import os

test_array = test_case.test_array

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template("sleep.yaml.j2")

kube_job_manager.init_manager()

for i in range(0, min(len(test_array), 10)):
    triple = test_array[i]
    filename = "sleep" + str(i)
    print("Pushing task %s" % filename)
    time.sleep(triple[0])
    outputText = template.render(deadline=triple[2] + time.time(), runtime=triple[1], number=i)

    f = open(filename + ".yaml", "w")
    f.write(outputText)
    f.close()

    kube_job_manager.add_job(filename)

while True:
    time.sleep(10)
    if not os.popen('kubectl get pods').read().split() :
        break

# read file with data

# for each data point
#   wait a bit
#   generate yaml file (with jinja2)
#   call into job manager with the file