# Simulated Quantum Annealing
### Description of the algorithm
Simulated Quantum Annealing (SQA, a.k.a. Quantum Monte Carlo, QMC) is a classical algorithm that utilizes path-integral Monte Carlo (PIMC) method to numerically simulate Quantum Annealing (QA) [1]. <br>

In SQA, the time-dependent transverse field is replaced with coupling between Ising spins of adjacent replicas. Periodic boundary condition is assumed. <br>

The precision to which SQA can reproduce quantum mechanical behavior depends on the number of Trotter replicas.

### Notes
1. For the purpose of simulating QA, a large number of Trotter replicas is essential. <br>
   However, if the goal is to use SQA as an optimization algorithm, many conditions can be relaxed, such as the number of Trotter replicas or the periodic boundary condition.
2. An implementation of SQA is available at https://github.com/shinmorino/sqaod/wiki

### Questions
1. What role does the "temperature" parameter in SQA play? It isn't obvious what it corresponds to in the QA counterpart.
2. According to the benchmark done by Google [2], SQA seems to have scaling advantage similar to QA, albeit with a very hefty overhead. Does this mean that QA has no intrinsic advantage over classical machines?
3. There is a commercial FPGA/ASIC implementation of SQA by Hitachi [3]. The weakness is obvious: the connectivity is sparse (king's graph). Is there any difficulty to implement fully connected SQA on the hardware level?

### References
1. https://doi.org/10.1103/PhysRevB.66.094203
2. https://doi.org/10.1103/PhysRevX.6.031015; see also: https://doi.org/10.1109/FOCS.2016.81
3. https://doi.org/10.1109/ICRC.2017.8123652
