export NETSIM="C:\ProgramData\Anaconda3\lib\site-packages\SimulaQron"
sh $NETSIM/run/startAll.sh -nd "Alice Bob"
alias git-bash='/git-bash.exe'

git-bash -c 'sh alice.sh' &
git-bash -c 'sh bob.sh' &