# Thermodynamic Simulated Annealing

### Description of the algorithm

Thermodynamic Simulated Annealing (TSA) is an improved version of the classical SA. The annealing routines are mostly the same, except that the temperature schedule is determined dynamically in the algorithm, rather than _a priori_ [1]. The only hyperparameter is the annealing speed coefficient.

Temperature of the next move is measured through energy and (information) entropy, which are both state functions. Entropy differences are calculated by considering the information obtained in the reception of a message of probability P, and therefore always changes if the proposed flip would result in a higher energy state, even when the flip proposal is not accepted.

### Notes

(to be filled)

### Questions

(to be filled)

### References

1. https://doi.org/10.1016/j.physleta.2003.08.070; see also: https://patents.google.com/patent/US20030014225A1/en
