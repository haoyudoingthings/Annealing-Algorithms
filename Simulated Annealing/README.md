# Simulated Annealing

### Despcription of the algorithm
Simulated Annealing (SA) is a Markov-chain Monte Carlo method that solves optimization problems by simulating classical thermal annealing. At each step, the algorithm explores a neighboring state (by proposing one spin flip) and decides whether to move to it or stay in the current state by Metropolis criterion. <br>

The temperature parameter starts off large to allow escape from local minima, and slowly converges to a very small value by the end of the algorithm, just like annealing in the real world. A log-inverse temperature schedule is shown to guarantee convergence to ground state in the adiabatic limit, but other faster temperature schedule may also provide convergence to ground state depending on the problem instance.

### Notes
(to be filled)

### Questions
1. Are there any real-world application where SA is the state-of-the-art heuristic for it?

### References
(to be filled)
