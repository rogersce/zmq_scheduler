#!/usr/bin/env python

def sigint_handler(sig, frame):
    import sys
    print('Stopping worker...')
    socket.send(b'DISCONNECT')
    sys.exit(0)

def main():
    import zmq
    import signal
    import dill as pickle

    global socket

    signal.signal(signal.SIGINT, sigint_handler)

    task_id = '1'.rjust(5,'0').encode('ascii')

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.setsockopt(zmq.IDENTITY,task_id)
    socket.setsockopt(zmq.REQ_RELAXED,1)
    socket.connect('tcp://localhost:5056')
    socket.send(b'CONNECT')

    while True:
        address, empty, request = socket.recv_multipart()
        f,args,kwargs = pickle.loads(request)
        result = f(*args,**kwargs)
        socket.send_multipart([address,b'',pickle.dumps(result)])

if __name__ == '__main__':
    main()
