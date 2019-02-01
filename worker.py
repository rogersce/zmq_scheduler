#!/usr/bin/env python

import sys
import os
import zmq
import dill as pickle
import signal

def sigint_handler(sig, frame):
    print('Stopping worker...')
    socket.send(b'DISCONNECT')
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

sched_hostname = sys.argv[1]
task_id = '1'.rjust(5,'0').encode('ascii')
#task_id = os.getenv('SLURM_ARRAY_TASK_ID').rjust(5,'0').encode('ascii')

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.setsockopt(zmq.IDENTITY,task_id)
socket.setsockopt(zmq.REQ_RELAXED,1)
socket.connect('tcp://{0}:5056'.format(sched_hostname))
socket.send(b'CONNECT')

while True:
    address, empty, request = socket.recv_multipart()
    f,args,kwargs = pickle.loads(request)
    result = f(*args,**kwargs)
    socket.send_multipart([address,b'',pickle.dumps(result)])
