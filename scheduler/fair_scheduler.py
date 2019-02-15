#!/usr/bin/env python

import zmq
import dill as pickle

class Client:
    def __init__(self,n_nodes):
        self.n_nodes = n_nodes
        self.dangling_results = []

        self.context = zmq.Context()
        self.pub_socket = self.context.socket(zmq.PUB)
        self.pub_socket.bind('tcp://*:5055')

        self.pub_sync_socket = self.context.socket(zmq.PULL)
        self.pub_sync_socket.bind('tcp://*:5056')

        self.push_socket = self.context.socket(zmq.PUSH)
        self.push_socket.bind('tcp://*:5057')

        self.pull_socket = self.context.socket(zmq.PULL)
        self.pull_socket.bind('tcp://*:5058')

        self.wait_for_subscribers()

    def wait_for_subscribers(self):
        import time

        synced = set()
        while len(synced) < self.n_nodes:
            self.pub_socket.send_multipart([b'SYNC',b''])
            while True:
                try:
                    node_id = pickle.loads(self.pub_sync_socket.recv(zmq.DONTWAIT))
                    synced.add(node_id)
                except zmq.Again:
                    break
            time.sleep(0.1)

    def send(self,f,args=(),kwargs={}):
        import uuid
        jobid = uuid.uuid1()
        self.push_socket.send(pickle.dumps((jobid,f,args,kwargs)))
        return jobid

    def broadcast(self,f,args=(),kwargs={},to='node'):
        import uuid
        jobid = uuid.uuid1()

        if to == 'node':
            self.pub_socket.send_multipart([b'NODE',pickle.dumps((jobid,f,args,kwargs))])
            return [jobid]*self.n_nodes
        else: 
            raise ValueError('Unknown broadcast destination')

    def wait_for_completed(self, joblist):
        results = []

        to_remove = []
        for jobid,result in self.dangling_results:
            if jobid in joblist:
                joblist.remove(jobid)
                results.append(result)
                to_remove.append(result)

        [self.dangling_results.remove(x) for x in to_remove]

        while joblist:
            jobid, result, args, kwargs = pickle.loads(self.pull_socket.recv())
            result = {'args':args,'kwargs':kwargs,'f_x':result}
            try:
                joblist.remove(jobid)
                results.append(result)
            except ValueError:
                dangling_results.append((jobid,result))

        return results

def worker_thread(context):

    pull_socket = context.socket(zmq.PULL)
    pull_socket.connect('tcp://localhost:5057')

    push_socket = context.socket(zmq.PUSH)
    push_socket.connect('tcp://localhost:5058')
    while True:
        jobid, f, args, kwargs = pickle.loads(pull_socket.recv())
        push_socket.send(pickle.dumps((jobid,f(*args,**kwargs),args,kwargs)))
    socket.close()

def master_thread(n_workers):
    from threading import Thread
    import uuid

    nodeid = uuid.uuid1()

    context = zmq.Context()

    sub_socket = context.socket(zmq.SUB)
    sub_socket.connect('tcp://localhost:5055')
    sub_socket.setsockopt(zmq.SUBSCRIBE, b'SYNC')
    sub_socket.setsockopt(zmq.SUBSCRIBE, b'NODE')

    sub_vent = context.socket(zmq.PUSH)
    sub_vent.connect('tcp://localhost:5056')

    push_socket = context.socket(zmq.PUSH)
    push_socket.connect('tcp://localhost:5058')

    for n in range(n_workers):
        Thread(target=worker_thread, args=(context,)).start()

    while True:
        [topic, msg] = sub_socket.recv_multipart()

        if topic == b'SYNC':
            sub_vent.send(pickle.dumps(nodeid))
        elif topic == b'NODE':
            jobid, f, args, kwargs = pickle.loads(msg)
            push_socket.send(pickle.dumps((jobid,f(*args,**kwargs),args,kwargs)))
        else:
            raise ValueError('Unknown PUBSUB topic')

    sub_socket.close()
    sub_vent.close()
    push_socket.close()
    context.term()

if __name__ == '__main__':
    import sys
    master_thread(int(sys.argv[1]))


