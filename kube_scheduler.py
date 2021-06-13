from kubernetes import client, config, watch
import threading
import time
import test_script
import os

config.load_kube_config()
v1 = client.CoreV1Api()
waiting_pods = []
lock = threading.Lock()
nodes = 4
running_pods = {x: [] for x in range(nodes)}
dropped_tasks = 0
DROP = True
ALGO = "edf"


# Set DROP value
def set_drop(drop):
    global DROP
    DROP = drop

# Set ALGO value
def set_algo(algo):
    global ALGO
    ALGO = algo

# Checks if any node is free by checking each list in the running_pods dictionary
def nodes_free():
    global running_pods
    for i in range(nodes):
        if not running_pods[i]:
            return True

    return False


def nodes_append(name):
    global running_pods
    for i in range(nodes):
        if not running_pods[i]:
            running_pods[i].append(name)
            return i


def nodes_remove(name):
    global running_pods
    for i in range(nodes):
        if name in running_pods[i]:
            running_pods[i].remove(name)


def nodes_contain(name):
    global running_pods
    for i in range(nodes):
        if name in running_pods[i]:
            return True

    return False


# Earliest deadline first
def reorder_edf():
    global waiting_pods
    waiting_pods.sort(key=lambda x: float(x.annotations["deadline"]))


# Shortest job first
def reorder_sjf():
    global waiting_pods
    waiting_pods.sort(key=lambda x: float(x.annotations["runtime"]))


# Maximum slack first
def reoreder_msf():
    global waiting_pods
    now = time.time()
    waiting_pods.sort(key=lambda x: -(float(x.annotations["deadline"]) - (now + float(x.annotations["runtime"]))))


# Minimum slack first
def reoreder_minsf():
    global waiting_pods
    now = time.time()
    waiting_pods.sort(key=lambda x: -(float(x.annotations["deadline"]) - (now + float(x.annotations["runtime"]))))

# Shortest job "adjusted" first
def reorder_sjaf():
    global waiting_pods
    def adjust(runtime, fail):
        total_runtime = runtime
        fail_rate = fail / 100
        while fail_rate*runtime > 1:
            total_runtime += fail_rate*runtime
            fail_rate *= fail_rate
        
        return total_runtime

    waiting_pods.sort(key=lambda x: adjust(float(x.annotations["runtime"]), float(x.annotations["failure"])))
    print("[")
    for w in waiting_pods:
        print(w.name, w.annotations["runtime"], adjust(float(w.annotations["runtime"]), float(w.annotations["failure"])))
    print("]")

# Largest failure (rate) first
def reorder_lff():
    global waiting_pods
    waiting_pods.sort(key=lambda x: -float(x.annotations["failure"]))


# the scheduling algorithm is called here
def reoreder_list():
    global ALGO
    type = ALGO
    if type == "edf":
        reorder_edf()
    elif type == "sjf":
        reorder_sjf()
    elif type == "msf":
        reorder_sjf()
    elif type == "sjaf":
        reorder_sjaf()
    elif type == "lff":
        reorder_lff()


def grep_jobs(job):
    log = os.popen('kubectl get jobs').read().split("\n")
    for line in log:
        if job in line:
            return True

    return False


def get_or_drop_pods():
    global waiting_pods, dropped_tasks, DROP

    if not DROP:
        return waiting_pods.pop(0)

    pod = waiting_pods.pop(0)
    while time.time() + float(pod.annotations["runtime"]) > float(pod.annotations["deadline"]):
        # delete from kubernetes
        job = pod.owner_references[0].name
        if grep_jobs(job):
            os.popen('kubectl delete job ' + job)
            dropped_tasks += 1

        if not waiting_pods:
            return None
        else:
            pod = waiting_pods.pop(0)

    return pod


def schedule(name, node_index):
    node = v1.list_node().items[node_index].metadata.name
    target = client.V1ObjectReference()
    target.kind = "Node"
    target.apiVersion = "v1"
    target.name = node
    meta = client.V1ObjectMeta()
    meta.name = name
    body = client.V1Binding(target=target)
    body.metadata = meta
    try:
        # print("Scheduled pod %s on node %s" % (name, node))
        v1.create_namespaced_binding("default", body)
    except:
        pass


def main():
    global lock, waiting_pods, running_pods

    w = watch.Watch()
    for event in w.stream(v1.list_namespaced_pod, "default"):
        if event['object'].status.phase == "Pending" and event['object'].spec.scheduler_name == "custom-scheduler":
            if not event['object'].metadata.name in [x.name for x in waiting_pods] and not nodes_contain(event['object'].metadata.name):
                # add to list, trigger pod reordering
                lock.acquire()

                # print("Added " + event['object'].metadata.name)

                waiting_pods.append(event['object'].metadata)
                reoreder_list()

                # if nothing is running - schedule a pod
                if nodes_free():
                    new_pod = get_or_drop_pods()
                    if new_pod is not None:
                        node_index = nodes_append(new_pod.name)
                        print("Schedule %s %d" % (new_pod.name, node_index))
                        schedule(new_pod.name, node_index)
                lock.release()

        elif (event['object'].status.phase == "Succeeded" or event['object'].status.phase == "Failed") and event['object'].spec.scheduler_name == "custom-scheduler":
            # trigger pod scheduling
            lock.acquire()

            if nodes_contain(event['object'].metadata.name):

                nodes_remove(event['object'].metadata.name)

                # if a pod is waiting to be scheduled - do it
                if waiting_pods:
                    new_pod = get_or_drop_pods()
                    if new_pod is not None:
                        node_index = nodes_append(new_pod.name)
                        print("Schedule %s %d" % (new_pod.name, node_index))
                        schedule(new_pod.name, node_index)

            lock.release()


if __name__ == '__main__':
    main()
