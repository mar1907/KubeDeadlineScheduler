import thread
import threading
import time
import os

THREAD_STARTED = False
lock = threading.Lock()
add_list = []
watch_list = []
slack = 0

def grep_pod(pod, x):
    pods = os.popen('kubectl get pods').read().split('\n')
    for line in pods:
        if pod not in line:
            continue
        else:
            status = line.split()[x]
            return status
            
    return None

def init_manager():
    global THREAD_STARTED
    THREAD_STARTED = True
    thread.start_new_thread(loop, ())

def loop():
    global lock, add_list, watch_list, slack
    while True:
        time.sleep(1) # maybe not

        # add new job
        if add_list:
            lock.acquire()

            for job in add_list:
                os.popen('kubectl apply -f ' + job + '.yaml')
                current_pod = grep_pod(job, 0)
                print("Append ", current_pod)
                watch_list.append(current_pod)

            add_list[:] = []

            lock.release()

        # delete finished jobs
        if watch_list:
            for pod in list(watch_list):
                status = grep_pod(pod, 2)
                if status != 'Completed':
                    continue

                log = os.popen('kubectl logs ' + pod).read().split("\n")
                slack += float(log[0]) - float(log[1])
                # logs.append(log) deal with logs!!
                os.popen('kubectl delete pod ' + pod)
                job = pod.split("-")[0]
                os.popen('kubectl delete job ' + job)

                watch_list.remove(pod)

                os.remove(job + ".yaml")

        print("Slack:" + str(slack))

# job -> name of the yaml file (without extension)
def add_job(job):
    if not THREAD_STARTED:
        return

    global lock, add_list

    lock.acquire()
    add_list.append(job)
    lock.release()