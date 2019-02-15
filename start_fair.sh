#!/usr/bin/env bash

tmux new-session -d -s scheduler
tmux setw remain-on-exit on
tmux new-window -t scheduler:1 'ssh node1 -N -R 5055:localhost:5055'
tmux setw remain-on-exit on
tmux new-window -t scheduler:2 'ssh node1 -N -R 5056:localhost:5056'
tmux setw remain-on-exit on
tmux new-window -t scheduler:3 'ssh node1 -N -R 5057:localhost:5057'
tmux setw remain-on-exit on
tmux new-window -t scheduler:4 'ssh node1 -N -R 5058:localhost:5058'
tmux setw remain-on-exit on
tmux new-window -t scheduler:5 'ssh node1 -t "python -m scheduler.fair_scheduler 12"'
tmux setw remain-on-exit on
tmux new-window -t scheduler:6 'python -m scheduler.fair_scheduler 4'
tmux setw remain-on-exit on
