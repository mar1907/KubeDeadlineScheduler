from kubernetes import client, config, watch
import threading
import time

config.load_kube_config()
v1 = client.CoreV1Api()
waiting_pods = []
lock = threading.Lock()
nodes = 2
running_pods = {x : [] for x in range(nodes)}


# Checks if any "node" is free by checking each list in the running_pods dictionary
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
            return

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

# the scheduling algorithm is called here
def reoreder_list():
    # EDF
    reorder_edf()

    # SJF
    # reorder_sjf()

    # MSF
    # reoreder_msf()

    #MinSF
    # reoreder_minsf()

def schedule(name):
    print(running_pods)
    node = v1.list_node().items[0].metadata.name
    target = client.V1ObjectReference()
    target.kind = "Node"
    target.apiVersion = "v1"
    target.name = node
    meta = client.V1ObjectMeta()
    meta.name = name
    body = client.V1Binding(target=target)
    body.metadata = meta
    try:
        print("Scheduled pod %s on node %s" % (name, node))
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

                waiting_pods.append(event['object'].metadata)
                reoreder_list()

                print("Added " + event['object'].metadata.name)

                # if nothing is running - schedule a pod
                if nodes_free():
                    new_pod = waiting_pods.pop().name
                    nodes_append(new_pod)
                    schedule(new_pod)
                lock.release()

        elif event['object'].status.phase == "Succeeded" and event['object'].spec.scheduler_name == "custom-scheduler":
            # trigger pod scheduling
            lock.acquire()

            if nodes_contain(event['object'].metadata.name):

                nodes_remove(event['object'].metadata.name)

                # if a pod is waiting to be scheduled - do it
                if waiting_pods:
                    new_pod = waiting_pods.pop().name
                    nodes_append(new_pod)
                    schedule(new_pod)

            lock.release()


if __name__ == '__main__':
    main()
