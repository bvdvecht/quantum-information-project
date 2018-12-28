#!/usr/bin/env bash
sh $NETSIM/run/startAll.sh -nd "Alice Bob"

python "deutsch-constant0-alice.py" -u &
python "deutsch-constant0-bob.py" -u &