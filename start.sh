#!/usr/bin/env bash

tmux new-session -d -s scheduler
tmux new-window -t scheduler:1 'ssh node1 -t "python -m scheduler.scheduler"'
tmux new-window -t scheduler:2 'ssh node1 -t "python -m scheduler.worker 1"'
tmux new-window -t scheduler:3 'ssh node1 -t "python -m scheduler.worker 2"'
tmux new-window -t scheduler:4 'ssh node1 -t "python -m scheduler.worker 3"'
