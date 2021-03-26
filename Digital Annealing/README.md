# Digital Annealing

### Description of the algorithm

Digital Annealing (DA) is an improved version of SA that expedites state exploration through parallelization. At each iteration, the algorithm samples all the neighboring states in parallel (instead of just one in SA) and moves to whichever is accepted. If there are multiple states accepted, the algorithm chooses one of them at random [1].

The inclusion of an increasing energy offset is another technique employed to help overcome energy barriers that trap the current state in a local minimum.

### Notes

1. DA speeds up the exploration of state space by increasing the direction that the algorithms look into. If these annealing algorithms are exploring a rugged terrain, SA is a short-sighted algorithm that only looks at the place where he is considering to take the next step. On the other hand, DA looks around him and chooses the best direction to go, albeit he still walks one step at a time and cannot look beyond where he can feasibly set his foot on (still short-sighted).
2. There is a commercial ASIC implementation by Fujitsu, see: https://www.fujitsu.com/global/services/business-services/digital-annealer/

### Questions

(to be filled)

### References

1. https://doi.org/10.3389/fphy.2019.00048
