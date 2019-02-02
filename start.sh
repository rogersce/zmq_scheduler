#!/usr/bin/env bash

tmux new-session -d -s scheduler
tmux new-window -t scheduler:1 'ssh node1 -N -L 5055:localhost:5055'
tmux new-window -t scheduler:2 'ssh node1 -N -L 5056:localhost:5056'
tmux new-window -t scheduler:3 'ssh node1 -t "python -m scheduler.scheduler"'
tmux new-window -t scheduler:4 'ssh node1 -t "python -m scheduler.worker 1"'
tmux new-window -t scheduler:5 'ssh node1 -t "python -m scheduler.worker 2"'
tmux new-window -t scheduler:6 'ssh node1 -t "python -m scheduler.worker 3"'
