#!/usr/bin/env python

import zmq
import sys
import dill as pickle

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect('tcp://node1:5056')
socket.send(b'READY')

while True:
    address, empty, request = socket.recv_multipart()
    request = pickle.loads(request)
    print('got request ',request)
    f, args = request
    result = f(*args)
    socket.send_multipart([address,b'',pickle.dumps(result)])
