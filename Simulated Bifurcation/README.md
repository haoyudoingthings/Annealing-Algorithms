# Simulated Bifurcation
### Description of the algorithm

Simulated Bifurcation (SB) is an combinatorial optimization method that approximates a coherent Ising machine (CIM) [1, 2]. The algorithm numerically solves a set of time-dependent differential equations, of which the underlying energy landscape has its equilibrium bifurcate into multiple equilibria corresponding to the eigenstates when the time-dependent pump strngth exceeds threshold. Therefore, the eigenstate with the lowest eigenvalue (ground state) will bifurcate first and (hopefully) the system will be trapped in the minimum when the algorithm ends.

### Notes

1. There is a commercial implementation of SB by Toshiba, see: [https://www.global.toshiba/ww/products-solutions/ai-iot/sbm.html](https://www.global.toshiba/ww/products-solutions/ai-iot/sbm.html)
2. Benchmark results of dSB with MaxCut problems can be found [here](dSB_Benchmark_Results.md).

### Questions

1. What is the best configuration of parameters such as dt, c0 and a(t)?
2. What kinds of problems are suitable for SB to solve?
3. Why does my implementation of dSB seemingly behave differently from the results in [2]?

### References

1. https://doi.org/10.1126/sciadv.aav2372
2. https://doi.org/10.1126/sciadv.abe7953
