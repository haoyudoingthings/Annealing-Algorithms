# Momentum Annealing

### Description of the algorithm

Momentum Annealing (MA) is an improved version of SA that expedites exploration of the state space through parallelization. The problem topology of originally (in general) complete graph is mapped to a bipartite graph, with two sides being replicas of the same state. Spins on the same side are then decoupled and, therefore, allow for parallel update of the spins. Convergence of the two replicas are ensured by taking large enough couplings between the corresponding spins [1].

### Notes

1. An obvious advantage of MA (or other similar applications implemented on CPU/GPU) to most ASIC/FPGA annealing machines is its full connectivity. The mapping of dense problem topology to sparse solver topology introduces a heavy overhead.
2. There is a commercial implpementation of MA on GPU by Hitachi. See: https://www.hitachi.com/rd/news/topics/2019/1018.html

### Questions

(to be filled)

### References

1. https://doi.org/10.1103/PhysRevE.100.012111
