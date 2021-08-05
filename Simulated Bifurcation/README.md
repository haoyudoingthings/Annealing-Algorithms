# Simulated Bifurcation
### Description of the algorithm

Simulated Bifurcation (SB) is an combinatorial optimization method that simulates coherent Ising machine (CIM) [1]. The algorithm numerically solves a set of time-dependent differential equations, of which the underlying energy landscape has its equilibrium bifurcate into multiple equilibria corresponding to the eigenstates when the time-dependent pump strngth exceeds threshold. Therefore, the eigenstate with the lowest eigenvalue (ground state) will bifurcate first and hopefully the particle will be trapped in that minimum until the algorithm ends.

### Notes

1. There are improved versions of the original (adiabatic) simulated bifurcation (aSB) called ballistic simulated bifurcation (bSB) and discrete simulated bifurcation (dSB). Their performances seem to be better than aSB [2].
2. There is a commercial implementation of SB by Toshiba, see: https://www.global.toshiba/ww/products-solutions/ai-iot/sbm.html

### Questions

1. What is the best configuration of parameters such as a0, c0 and p(t)?
2. What is the tolerance to the precision of numerical method (time-step size, symplectic Euler method, etc.) and coupling coefficients?
3. How harsh is the natural constraint of vanishing diagonal elements in problem Hamiltonian?

### References

1. https://doi.org/10.1126/sciadv.aav2372
2. https://doi.org/10.1126/sciadv.abe7953
