#!/usr/bin/env bash
sh $NETSIM/run/startAll.sh -nd "Alice Bob"

python "deutsch-3QBbalanced-alice.py" -u &
python "deutsch-3QBbalanced-bob.py" -u &