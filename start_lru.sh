#!/usr/bin/env bash

#ssh-agent
#ssh-add

tmux new-session -d -s scheduler
tmux setw remain-on-exit on
tmux new-window -t scheduler:1 'ssh node1 -N -L 5055:localhost:5055'
tmux setw remain-on-exit on
tmux new-window -t scheduler:2 'ssh node1 -N -L 5056:localhost:5056'
tmux setw remain-on-exit on
tmux new-window -t scheduler:3 'ssh node1 -t "python -m scheduler.scheduler"'
tmux setw remain-on-exit on

#tmux new-window -t scheduler:4 'ssh localhost -t "python -m scheduler.worker 1"'
#tmux setw remain-on-exit on
#tmux new-window -t scheduler:5 'ssh localhost -t "python -m scheduler.worker 2"'
#tmux setw remain-on-exit on
#tmux new-window -t scheduler:6 'ssh localhost -t "python -m scheduler.worker 3"'
#tmux setw remain-on-exit on
#tmux new-window -t scheduler:7 'ssh localhost -t "python -m scheduler.worker 4"'
#tmux setw remain-on-exit on
#tmux new-window -t scheduler:8 'ssh localhost -t "python -m scheduler.worker 5"'
#tmux setw remain-on-exit on
#tmux new-window -t scheduler:9 'ssh localhost -t "python -m scheduler.worker 6"'
#tmux setw remain-on-exit on
tmux new-window -t scheduler:10 'ssh node1 -t "python -m scheduler.worker 7"'
tmux setw remain-on-exit on
tmux new-window -t scheduler:11 'ssh node1 -t "python -m scheduler.worker 8"'
tmux setw remain-on-exit on
tmux new-window -t scheduler:12 'ssh node1 -t "python -m scheduler.worker 9"'
tmux setw remain-on-exit on
tmux new-window -t scheduler:13 'ssh node1 -t "python -m scheduler.worker 10"'
tmux setw remain-on-exit on
tmux new-window -t scheduler:14 'ssh node1 -t "python -m scheduler.worker 11"'
tmux setw remain-on-exit on
tmux new-window -t scheduler:15 'ssh node1 -t "python -m scheduler.worker 12"'
tmux setw remain-on-exit on
