#!/usr/bin/env python

import sys
import os
import zmq
import dill as pickle

task_id = os.getenv('SLURM_ARRAY_TASK_ID').rjust(5,'0').encode('ascii')

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.setsockopt(zmq.IDENTITY,task_id)
socket.connect('tcp://node1:5056')
socket.send(b'READY')

while True:
    address, empty, request = socket.recv_multipart()
    f,args = pickle.loads(request)
    result = f(*args)
    socket.send_multipart([address,b'',pickle.dumps(result)])
