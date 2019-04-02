#!/usr/bin/env bash

export PYTHONPATH=/home/ivan/Workspace/PyCharm/blockswarm/sources

python3 robot_swarm/Miner.py 10000 &
python3 robot_swarm/Robot.py 10000

#python3 robot_swarm/Miner.py $1 $2 $3