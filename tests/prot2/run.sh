sh $NETSIM/run/startAll.sh -nd "Alice Bob"
#python $NETSIM/run/startNode.py "Alice" &
#python $NETSIM/run/startNode.py "Bob" &
#python $NETSIM/run/startCQC.py "Bob" &
#python $NETSIM/run/startCQC.py "Alice" &

python "alice.py" &
python "bob.py" &