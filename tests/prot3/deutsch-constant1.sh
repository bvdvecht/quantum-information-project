#!/usr/bin/env bash
sh $NETSIM/run/startAll.sh -nd "Alice Bob"

python "deutsch-constant1-alice.py" -u &
python "deutsch-constant1-bob.py" -u &