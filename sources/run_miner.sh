#!/usr/bin/env bash

export PYTHONPATH=/home/ivan/Workspace/PyCharm/blockswarm/sources

python3 robot_swarm/Miner.py 10000 &
PIDS=($!)

python3 robot_swarm/Miner.py 20000 &
PIDS+=($!)

python3 robot_swarm/Miner.py 30000 &
PIDS+=($!)

python3 robot_swarm/Miner.py 40000 &
PIDS+=($!)

python3 robot_swarm/Robot.py http://127.0.0.1:10000 -i 1 &
PIDS+=($!)

python3 robot_swarm/Robot.py http://127.0.0.1:20000 -i 2 -p http://138.100.156.21:10000 &
PIDS+=($!)

python3 robot_swarm/Robot.py http://127.0.0.1:30000 -i 3 -p http://138.100.156.21:10000 &
PIDS+=($!)

python3 robot_swarm/Robot.py http://127.0.0.1:40000 -i 4 -p http://138.100.156.21:30000 &
PIDS+=($!)

sleep 15

for i in "${PIDS[*]}"; do kill ${i}; done


