#!/usr/bin/env python

import zmq
import time
from functools import partial
import numpy as np
from scheduler.fair_scheduler import Client

def f(x):
    return x*x

def load_data(x):
    print('HERE')
    return True

n_nodes = 2
client = Client(n_nodes)

future_f = [client.send(f,args=(x,)) for x in np.linspace(0,1,20)]
results = client.wait_for_completed(future_f)
           
future_f = client.broadcast(load_data,args=(1,))
bcast_results = client.wait_for_completed(future_f)
