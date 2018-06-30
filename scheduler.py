#!/usr/bin/env python

import zmq

context = zmq.Context()
frontend = context.socket(zmq.ROUTER)
frontend.bind('ipc://frontend.ipc')
backend = context.socket(zmq.ROUTER)
backend.bind('ipc://backend.ipc')

workers = []
poller = zmq.Poller()

poller.register(backend,zmq.POLLIN)

while True:
    sockets = dict(poller.poll())
    if backend in sockets:
        print('got a backend poll request')
        request = backend.recv_multipart()
        worker, empty, client = request[:3]
        if not workers:
            poller.register(frontend, zmq.POLLIN)
        workers.append(worker)

        if client != b'READY' and len(request) > 3:
            empty, reply = request[3:]
            frontend.send_multipart([client,b'',reply])

    if frontend in sockets:
        print('got a frontend poll request')
        client, empty, request = frontend.recv_multipart()
        worker = workers.pop(0)
        backend.send_multipart([worker, b'', client, b'', request])
        if not workers:
            poller.unregister(frontend)

backend.close()
frontend.close()
context.term()
