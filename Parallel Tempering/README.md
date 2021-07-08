# Parallel Tempering

### Description of the algorithm

Parallel Tempering (PT, a.k.a. replica exchange Markov-chain Monte Carlo) is a simulation method aimed at improving the dynamic property of SA, or Markov-chain Monte Carlo methods in general. There are multiple replicas of the same system annealing at different constant temperatures. At each iteration, in addition to proposing a flip, the algorithm also proposes a replica exchange between neighboring replicas according to Metropolis criterion. If accepted, the configuration of the two replicas are swapped [1].

Excerpted from Wikipedia [2]: "The parallel tempering method can be used as a super simulated annealing that does not need restart, since a system at high temperature can feed new local optimizers to a system at low temperature, allowing tunneling between metastable states and improving convergence to a global optimum."

### Notes

(to be filled)

### Questions

(to be filled)

### References

1. https://doi.org/10.1103/PhysRevLett.57.2607; see also: https://doi.org/10.1039/b509983h and https://www.tweag.io/blog/2020-10-28-mcmc-intro-4/
2. https://en.wikipedia.org/wiki/Parallel_tempering
