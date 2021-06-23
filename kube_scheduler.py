from re import sub
from kubernetes import client, config, watch
import threading
import time
import _thread
import kube_job_manager
import pod_model
import os
import copy
import math

config.load_kube_config()
v1 = client.CoreV1Api()
waiting_pods = []
lock = threading.Lock()
nodes = 4
running_pods = {x: [] for x in range(nodes)}
node_queues = {x: [] for x in range(nodes)}
DROP = True
ALGO = "edf"
history = []
beta = 1 + math.sqrt(2)


# Set DROP value
def set_drop(drop):
    global DROP
    DROP = drop

# Set ALGO value
def set_algo(algo):
    global ALGO
    ALGO = algo

# Reset scheduler event history
def reset_history():
    global history
    history = []

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

# Highest value first
def reorder_hvf():
    global waiting_pods
    def compute_value(runtime, deadline):
        if time.time() + runtime > deadline:
            return deadline - (time.time() + runtime)
        else:
            return runtime
    
    waiting_pods.sort(key=lambda x: -compute_value(float(x.annotations["runtime"]), float(x.annotations["deadline"])))

# Highest value first w/ drop
def reorder_hvf_d():
    global waiting_pods
    def compute_value(runtime, deadline):
        val = 0
        if time.time() + runtime > deadline:
            return deadline - (time.time() + runtime)
        else:
            return runtime
    
    waiting_pods.sort(key=lambda x: compute_value(float(x.annotations["runtime"]), float(x.annotations["deadline"])))
    # print({p.name : compute_value(float(p.annotations["runtime"]), float(p.annotations["deadline"])) for p in waiting_pods})
    while waiting_pods:
        if compute_value(float(waiting_pods[0].annotations["runtime"]), float(waiting_pods[0].annotations["deadline"])) < 0:
            # print("Drop ", waiting_pods[0].name)
            _thread.start_new_thread(kube_job_manager.delete_job, (waiting_pods[0].name, 0))
            waiting_pods.pop(0)
        else:
            break
    waiting_pods.sort(key=lambda x: -compute_value(float(x.annotations["runtime"]), float(x.annotations["deadline"])))
    # print({p.name : compute_value(float(p.annotations["runtime"]), float(p.annotations["deadline"])) for p in waiting_pods})
            


# the scheduling algorithm is called here
def reorder_list():
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
    elif type == "hvf":
        reorder_hvf()
    elif type == "hvf_d":
        reorder_hvf_d()


def grep_jobs(job):
    log = os.popen('kubectl get jobs').read().split("\n")
    for line in log:
        if job in line:
            return True

    return False


def get_or_drop_pods():
    global waiting_pods, DROP

    if not DROP:
        return waiting_pods.pop(0)

    pod = waiting_pods.pop(0)
    while time.time() + float(pod.annotations["runtime"]) > float(pod.annotations["deadline"]):
        # delete from kubernetes
        job = pod.owner_references[0].name
        if grep_jobs(job):
            _thread.start_new_thread(kube_job_manager.delete_job, (waiting_pods[0].name, 0))

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


def create_affected_subset(queue, pod):
    latest_starttime = pod.get_latest_starttime()
    subset = []
    #going back through the queue
    for i in range(len(queue)-1, -1, -1):
        if queue[i].finish_time > latest_starttime:
            subset.append(queue[i])
        else:
            break

    return subset


def force_insert(queue, new_pod, affected_subset):
    print("Queue", queue)
    print("Subset", affected_subset)
    for pod in affected_subset:
        queue.remove(pod)

    queue.append(new_pod)
    new_pod.finish_time = new_pod.deadline + 2
    new_pod.value = new_pod.runtime

    affected_subset.sort(key=lambda x: x.deadline)
    resulting_affected_subset = []
    latest_starttime = queue[-1].finish_time
    # add to queue the affected pods which can still make their deadline
    for pod in affected_subset:
        if nodes_contain(pod.name):
            resulting_affected_subset.append(pod)
            continue
        if latest_starttime + pod.runtime < pod.deadline:
            queue.append(pod)
            pod.value = pod.runtime
            pod.finish_time = latest_starttime + pod.runtime + 2

            latest_starttime = queue[-1].finish_time
        else:
            resulting_affected_subset.append(pod)

    return resulting_affected_subset



def append_to_queues(pod):
    global node_queues, running_pods
    new_pod = pod_model.PodObject(pod.name, float(pod.annotations["runtime"]), float(pod.annotations["deadline"]))

    # if there's no way to meet the deadline, refuse
    if new_pod.get_latest_starttime() < time.time():
        print("Cannot meet deadline")
        return False
    
    # check the queue of each node
    for i in order_of_queue_length():
        print("Queue ", i)
        if not node_queues[i]:
            # if node queue is empty, schedule instantly
            print("Queue is empty")
            node_queues[i].append(new_pod)
            new_pod.finish_time = time.time() + new_pod.runtime + 2
            new_pod.value = new_pod.runtime
            # schedule(new_pod.name, i)
            return True
        else:
            # check if a peaceful schedule is possible
            last_pod = node_queues[i][-1]
            # check if the new pod can be started after the last pod in the queue
            if new_pod.get_latest_starttime() < last_pod.finish_time:
                print("Non-Peaceful schedule")
                # cannot schedule peacefully
                affected = create_affected_subset(node_queues[i], new_pod)
                # Split the decline profit into 2 parts, in order to only multiply the profit from the affected part
                # This is done because it is easier to compute the accept profit over the whole queue
                # profit from the queue w/o affected subset
                profit_decline_1 = 0
                # profit from the affected subset
                profit_decline_2 = 0
                for pod in node_queues[i]:
                    if pod in affected:
                        break
                    profit_decline_1 += pod.value
                for pod in affected:
                    profit_decline_2 += pod.value
                
                queue_copy = copy.deepcopy(node_queues[i])
                affected_copy = copy.deepcopy(affected)
                new_affected = force_insert(queue_copy, new_pod, affected_copy)
                profit_accept = 0
                for pod in queue_copy:
                    profit_accept += pod.value
                for pod in new_affected:
                    if nodes_contain(pod):
                        profit_accept -= pod.finish_time - time.time() -2
                    profit_accept -= pod.runtime

                # check profits
                print("Profits", profit_accept, (1 + beta) * profit_decline_2 + profit_decline_1)
                if profit_accept > (1 + beta) * profit_decline_2 + profit_decline_1:
                    print("Higher profits")
                    # accept the job and make the changes
                    node_queues[i] = queue_copy
                    for pod in new_affected:
                        for i in range(nodes):
                            if pod.name in running_pods[i]:
                                running_pods[i].remove(pod.name)
                                print("Running pods after remove", running_pods)
                                penalty = pod.finish_time - time.time() -2
                                _thread.start_new_thread(kube_job_manager.delete_job, (pod.name, -penalty))      
                                break  
                    _thread.start_new_thread(kube_job_manager.delete_job, (pod.name, -pod.runtime))

                    return True
                print("Lower profits")
                
            else:
                # peaceful schedule
                print("Peaceful schedule")
                node_queues[i].append(new_pod)
                new_pod.finish_time = last_pod.finish_time + new_pod.runtime + 2
                new_pod.value = new_pod.runtime
                return True

    # if no queue will accept the new pod, do not commit
    return False


def order_of_queue_length():
    global node_queues
    map = []
    for i in node_queues.keys():
        map.append((i, len(node_queues[i])))

    map.sort(key=lambda x: x[1])
    return [x[0] for x in map]



def main():
    global lock, waiting_pods, running_pods, history, node_queues

    w = watch.Watch()
    for event in w.stream(v1.list_namespaced_pod, "default"):
        if event['object'].status.phase == "Pending" and event['object'].spec.scheduler_name == "custom-scheduler":
            if not event['object'].metadata.name in [x.name for x in waiting_pods] and not nodes_contain(event['object'].metadata.name):
                # add to list, trigger pod reordering
                lock.acquire()

                # check if this event was already registered - if yes, ignore it
                event_tuple = ("Add", event['object'].metadata.name.split("-")[0])
                if event_tuple not in history:
                    
                    history.append(event_tuple)

                    # Prune history to keep the array short
                    if len(history) > 50:
                        history = history[len(history) - 50:]

                    # print("Added " + event['object'].metadata.name)
                    if "dsc" not in ALGO:
                        waiting_pods.append(event['object'].metadata)
                        reorder_list()

                        # if nothing is running - schedule a pod
                        if nodes_free() and waiting_pods:
                            new_pod = get_or_drop_pods()
                            if new_pod is not None:
                                node_index = nodes_append(new_pod.name)
                                print("Schedule %s %d" % (new_pod.name, node_index))
                                schedule(new_pod.name, node_index)
                    else:
                        print("Try ", event['object'].metadata.name)
                        if append_to_queues(event['object'].metadata):
                            print("Accepted ", node_queues)
                            print(running_pods)
                            # commit to this job
                        else:
                            print("Rejected ", node_queues)
                            # do not commit to this job, delete it
                            _thread.start_new_thread(kube_job_manager.delete_job, (event['object'].metadata.name, 0))

                        # check each node, if any is free scheduler a pod from the queue
                        print(order_of_queue_length())
                        for n in order_of_queue_length():
                            if not running_pods[n]:
                                # node free
                                if node_queues[n]:
                                    # queue has a node - schedule it
                                    print("Schedule %s %d" % (node_queues[n][0].name, n), "starts at: ", time.time(), "supposed to start at ", node_queues[n][0].get_latest_starttime())
                                    running_pods[n].append(node_queues[n][0].name)
                                    # print("Expected value ", node_queues[n][0].value)
                                    schedule(node_queues[n][0].name, n)

                lock.release()
                    

        elif (event['object'].status.phase == "Succeeded" or event['object'].status.phase == "Failed") and event['object'].spec.scheduler_name == "custom-scheduler":
            if nodes_contain(event['object'].metadata.name):
                # trigger pod scheduling
                lock.acquire()

                # check if this event was already registered - if yes, ignore it
                event_tuple = ("Delete", event['object'].metadata.name.split("-")[0])
                if event_tuple not in history:
                    
                    history.append(event_tuple)

                    # Prune history to keep the array short
                    if len(history) > 50:
                        history = history[len(history) - 50:]

                    if nodes_contain(event['object'].metadata.name):

                        nodes_remove(event['object'].metadata.name)

                    for i in range(nodes):
                        if node_queues[i]:
                            if node_queues[i][0].name == event['object'].metadata.name:
                                node_queues[i].pop(0)
                                break

                    if "dsc" not in ALGO:
                        # if a pod is waiting to be scheduled - do it
                        if waiting_pods:
                            new_pod = get_or_drop_pods()
                            if new_pod is not None:
                                node_index = nodes_append(new_pod.name)
                                print("Schedule %s %d" % (new_pod.name, node_index))
                                schedule(new_pod.name, node_index)
                    else:
                        print("After finish", event['object'].metadata.name, node_queues)
                        print(running_pods)
                        # check each node, if any is free scheduler a pod from the queue
                        print(order_of_queue_length())
                        for n in order_of_queue_length():
                            if not running_pods[n]:
                                # node free
                                if node_queues[n]:
                                    # queue has a node - schedule it
                                    print("Schedule %s %d" % (node_queues[n][0].name, n), "starts at: ", time.time(), "supposed to start at ", node_queues[n][0].get_latest_starttime())
                                    running_pods[n].append(node_queues[n][0].name)
                                    # print("Expected value ", node_queues[n][0].value)
                                    schedule(node_queues[n][0].name, n)

                lock.release()


if __name__ == '__main__':
    main()
