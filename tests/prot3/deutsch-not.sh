#!/usr/bin/env bash
sh $NETSIM/run/startAll.sh -nd "Alice Bob"

python "deutsch-not-alice.py" -u &
python "deutsch-not-bob.py" -u &