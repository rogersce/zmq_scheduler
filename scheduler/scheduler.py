#!/usr/bin/env python

def map(f,params,verbose=False,*args,**kwargs):
    import zmq
    import dill as pickle

    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.connect('tcp://localhost:5055')

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

def main():
    import zmq

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
            backend_addr, empty, msg = request[:3]

            if msg == b'DISCONNECT':
                workers = [w for w in workers if w != backend_addr]
                if not workers:
                    poller.unregister(frontend)
            elif msg == b'CONNECT':
                if not workers:
                    poller.register(frontend, zmq.POLLIN)
                workers.append(backend_addr)
            else:
                if not workers:
                    poller.register(frontend, zmq.POLLIN)
                workers.append(backend_addr)

                frontend_addr = msg
                empty, msg_to_frontend = request[3:]
                frontend.send_multipart([frontend_addr,b'',backend_addr,msg_to_frontend])

            print('Backend poll request. There are {0} workers available'.format(len(workers)))


        if frontend in sockets:
            client, empty, request = frontend.recv_multipart()

            worker = workers.pop(0)
            if not workers:
                poller.unregister(frontend)

            backend.send_multipart([worker, b'', client, b'', request])

            print('Frontend poll request. There are {0} workers available'.format(len(workers)))

    backend.close()
    frontend.close()
    context.term()

if __name__ == '__main__':
    main()


