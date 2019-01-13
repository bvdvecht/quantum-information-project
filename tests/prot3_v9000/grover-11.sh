#!/usr/bin/env bash
sh $NETSIM/run/startAll.sh -nd "Alice Bob" &

python "grover-11-alice.py" -u &
python "grover-11-bob.py" -u &