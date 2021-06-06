import _thread
import threading
import time
import os
import kube_scheduler
import multitimer

THREAD_STARTED = False
lock = threading.Lock()
add_list = []
watch_list = []
slack = 0
node_load = [0] * kube_scheduler.nodes


# Timer function check if node is busy, update load
def increase_load():
    global node_load
    for i in range(kube_scheduler.nodes):
        if kube_scheduler.running_pods[i]:
            node_load[i] += 1


timer = multitimer.MultiTimer(interval=1, function=increase_load)


def grep_pod(pod, x):
    pods = os.popen('kubectl get pods').read().split('\n')
    # print(pod, x, kube_scheduler.running_pods)
    for line in pods:
        if pod not in line:
            continue
        else:
            status = line.split()[x]
            return status
            
    return None


def init_manager():
    # print("FUNC: init_manager")
    global THREAD_STARTED, slack, node_load, timer
    slack = 0
    node_load = [0] * kube_scheduler.nodes
    timer = multitimer.MultiTimer(interval=1, function=increase_load)
    timer.start()
    THREAD_STARTED = True
    _thread.start_new_thread(loop, ())


def stop_manager():
    # print("FUNC: stop_manager")
    global THREAD_STARTED, timer
    timer.stop()
    THREAD_STARTED = False


def loop():
    global lock, add_list, watch_list, slack
    while THREAD_STARTED:
        time.sleep(1)  # maybe not

        # add new job
        if add_list:
            lock.acquire()

            for job in add_list:
                os.popen('kubectl apply -f ' + job + '.yaml')
                current_pod = grep_pod(job, 0)
                while current_pod is None:
                    current_pod = grep_pod(job, 0)
                # print("Append ", current_pod)
                watch_list.append(current_pod)

            add_list[:] = []

            lock.release()

        # delete finished jobs
        if watch_list:
            lock.acquire()
            for pod in list(watch_list):
                status = grep_pod(pod, 2)
                if status == None:
                    watch_list.remove(pod)
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
            lock.release()


# job -> name of the yaml file (without extension)
def add_job(job):
    if not THREAD_STARTED:
        return

    global lock, add_list

    lock.acquire()
    add_list.append(job)
    lock.release()