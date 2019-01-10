#!/usr/bin/env bash
sh $NETSIM/run/startAll.sh -nd "Alice Bob"

python "deutsch-not-alice-p2.py" -u &
python "deutsch-not-bob-p2.py" -u &