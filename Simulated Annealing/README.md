# Simulated Annealing

### Despcription of the algorithm

Simulated Annealing (SA) is a Markov-chain Monte Carlo method that solves combinatorial optimization problems by simulating classical thermal annealing. At each step, the algorithm explores a neighboring state (by proposing one spin flip) and decides whether to move to it or stay in the current state by Metropolis criterion [1].

The temperature parameter starts off large to allow escape from local minima, and slowly converges to a very small value by the end of the algorithm, just like annealing in the real world. A log-inverse temperature schedule is shown to guarantee convergence to ground state in the adiabatic limit [2], but other faster temperature schedule may also provide convergence to ground state depending on the problem instance.

### Notes

1. An implementation of SA is available at http://dx.doi.org/10.17632/y5nybjdshn.1

### Questions

1. Are there any real-world applications for which SA (or some variant of it) is the state-of-the-art heuristic?

### References

1. https://en.wikipedia.org/wiki/Simulated_annealing
2. https://doi.org/10.1109/TPAMI.1984.4767596; see also: https://doi.org/10.1214/ss/1177011077
