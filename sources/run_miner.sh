#!/usr/bin/env bash

export PYTHONPATH=/home/ivan/Workspace/PyCharm/blockswarm/sources

#python3 robot_swarm/Miner.py $1 $2 $3
#python3 robot_swarm/Miner.py 11000 -p http://127.0.0.1:10000 &

python3 robot_swarm/Miner.py 10000 &
python3 test.py 10000

