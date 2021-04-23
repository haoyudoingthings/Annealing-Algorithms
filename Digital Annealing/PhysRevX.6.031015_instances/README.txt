The sign convention for the Hamiltonian in the instance files is
H =\sum_j h_j s_j + \sum_{jk} J_{jk} s_j s_k
where s_j denotes the value of spin j, h_j is the local field of spin
j, and J_{jk} is the coupling between spins j and k.

The format for each line in the instance files is
s_j s_j h_j
for the local field h_j of spin s_j, and
s_j s_k J_{jk} 
for the coupling J_{jk} between spins j and k.

The file exact_energies.csv contains the minimum energy for each
instance. 
