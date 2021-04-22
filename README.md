# Annealing-Algorithms

This repo aims at collecting various annealing algorithms for future use. Each algorithm should ideally consist of:
1. A brief description of the algorithm that explains the main idea
2. Notes, including strengths/weaknesses analysis and, preferably, executable code
3. Questions
4. References

Some of the algorithms that are planned to be curated:
1. Simulated Annealing (SA)
2. Simulated Quantum Annealing (SQA)
3. Thermodynamic Simulated Annealing (TSA)
4. Digital Annealing (DA)
5. Momentum Annealing (MA)
6. Simulated Bifurcation Machine (SBM)
7. Parallel Tempering (PT)

Notes:
1. To investigate the inner workings of each algorithm beyond treating them as blackboxes, it is paramount for us to have access to the runtime states, energies and parameters. Therefore, a piece of working (not necessarily high-performing) code that is easily modifiable is very important for every algorithm.
2. To benchmark the performance of each algorithm, (i) Number Partitioning and (ii) Max-Cut problems are the most suitable for the rich literatures and natural mapping to Ising (QUBO) formulation. For the best practices behind comparing optimization algorithms, see: https://doi.org/10.1007/s11081-017-9366-1.
3. Data sets for Max-Cut: http://biqmac.uni-klu.ac.at/biqmaclib.html
4. Shall we wish to study the dynamics of state evolution in a black box annealer, we can "quench" the system by abruptly lowering the temperature to 0 in the middle of annealing, provided that we have control over the full annealing process.
