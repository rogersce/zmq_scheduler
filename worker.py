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
    print('got this ',request)
    #do some work
    socket.send_multipart([address,b'',b'WORK_RESPONSE'])
