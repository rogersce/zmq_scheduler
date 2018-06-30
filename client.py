#!/usr/bin/env python

import zmq
import sys
import dill as pickle

context = zmq.Context()
socket = context.socket(zmq.DEALER)
socket.connect('tcp://node1:5055')

work = [b'a',b'b',b'c']

for w in work:
    print('sending')
    socket.send_multipart([b'',w])

for w in work:
    msg = socket.recv_multipart()
    print('got this ',msg)
