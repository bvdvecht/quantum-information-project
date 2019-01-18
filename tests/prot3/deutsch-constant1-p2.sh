#!/usr/bin/env bash
sh $NETSIM/run/startAll.sh -nd "Alice Bob"

python "deutsch-constant1-alice-p2.py" -u &
python "deutsch-constant1-bob-p2.py" -u &