# A Protocol for Blind Quantum Computing

This repository contains the implementation of the blind quantum computing protocol based on iterated gate teleportation, as described in https://link.aps.org/doi/10.1103/PhysRevLett.114.220502.

The `bqc` folder contains the implementation of the protocols. The `tests` folder contains a variety of test scripts. Each test consists of 3 files: the script for Alice, the script for Bob, and a shell script starting both Alice's and Bob's scripts each in a separate process. The names of the tests combined with the comments in the test files should indicate their purpose. The `-p2` extension on some test names means that here the parameter `P` as defined in the paper is 2  (meaning Alice only has a 1-qubit memory, but still runs the multi-qubit computation).

All tests have been successfully run on Windows systems, and for this a slightly modified version of SimulaQron was needed: https://github.com/bvdvecht/SimulaQron. Also, the `killAllProc.sh` script in the current repository needs to be run in between test cases on Windows. On Linux systems, everything *should* simply work, but this has not been tested.

Authors:
Bart van der Vecht
Boris Joukovsky