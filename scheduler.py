#!/usr/bin/env python

import zmq
import dill as pickle

#a client is just a zmq socket
def get_client(host):
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.connect('tcp://{0}:5055'.format(host))
    return socket

def run(socket,params,f,verbose=False,*args,**kwargs):
    n_sent = 0
    for p in params:
        work = (f,[p],kwargs)
        socket.send_multipart([b'',pickle.dumps(work)])
        n_sent += 1

    n_recv = 0
    results = []
    while n_recv < n_sent:
        empty, worker, result = socket.recv_multipart()
        result = pickle.loads(result)
        if verbose: print('received worker: {0}, result: {1}'.format(worker,result))
        results.append(result)
        n_recv += 1
    return results

if __name__ == '__main__':
    context = zmq.Context()
    frontend = context.socket(zmq.ROUTER)
    backend = context.socket(zmq.ROUTER)
    frontend.bind('tcp://*:5055')
    backend.bind('tcp://*:5056')

    workers = []
    poller = zmq.Poller()
    poller.register(backend,zmq.POLLIN)

    while True:
        sockets = dict(poller.poll())

        if backend in sockets:
            request = backend.recv_multipart()
            worker, empty, client = request[:3]
            if not workers:
                poller.register(frontend, zmq.POLLIN)
            workers.append(worker)
            print('Backend poll request. There are {0} workers available'.format(len(workers)))
            if client != b'READY' and len(request) > 3:
                empty, reply = request[3:]
                frontend.send_multipart([client,b'',worker,reply])

        if frontend in sockets:
            print('got a frontend poll request')
            client, empty, request = frontend.recv_multipart()
            worker = workers.pop(0)
            print('Frontend poll request. There are {0} workers available'.format(len(workers)))
            backend.send_multipart([worker, b'', client, b'', request])
            if not workers:
                poller.unregister(frontend)

    backend.close()
    frontend.close()
    context.term()
