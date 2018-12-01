#!/bin/bash

# ALL_PIDS=$(ps aux | grep python | grep -E "Test|setup|start" | awk {'print $2'})
# if [ "$ALL_PIDS" != "" ]
# then
#         kill -9 $ALL_PIDS
# fi

ALL_PIDS=$(wmic process get processid,commandline | grep python.exe | grep -E "Test|setup|start" | awk '{printf "//pid %s ",$NF}')
if [ "$ALL_PIDS" != "" ]
then
        taskkill -f $ALL_PIDS
fi