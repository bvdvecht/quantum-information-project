sh $NETSIM/run/startAll.sh -nd "Alice Bob"

python "delegate-alice.py" &
python "delegate-bob.py" &