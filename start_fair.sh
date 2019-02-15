#!/usr/bin/env bash

tmux new-session -d -s scheduler
tmux setw remain-on-exit on

declare -a NODES=(node1 node2)
declare -a PORTS=(5055 5056 5057 5058)

#SSH TUNNELS
n=1
for node in ${NODES[@]}; do
    for port in ${PORTS[@]}; do
        tmux new-window -t scheduler:$n "ssh $node -N -R $port:localhost:$port"
        tmux setw remain-on-exit on
        tmux join-pane -s $((n+1)) -t $n
    done
    tmux select-layout tiled
    n=$((n+1))
done

#START WORKERS
for node in ${NODES[@]}; do
    tmux new-window -t scheduler "ssh $node -t 'python -m scheduler.fair_scheduler 12'"
    tmux setw remain-on-exit on
done

#LOCALHOST WORKER
#tmux new-window -t scheduler:9 'python -m scheduler.fair_scheduler 4'
#tmux setw remain-on-exit on
