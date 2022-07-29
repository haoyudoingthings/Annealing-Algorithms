# dSB Benchmark Results

[![hackmd-github-sync-badge](https://hackmd.io/0Ln2BwGpTu6OwHMfdytj7A/badge)](https://hackmd.io/0Ln2BwGpTu6OwHMfdytj7A)

## Jul. 19 results

- Benchmarked on BiqMac g05 MaxCut problem sets (N=60, 80, 100 with 10 instances for each size)
- Parameter settings:
    - `dt` = 0.25, 0.5, 0.75, 1.0, 1.25
    - `c0` = 0.1, 0.2, 0.3, 0.4, 0.5 (after J is normalized)
    - `steps` = int(150/dt)
    - initial values of y: uniform(-0.01, 0.01)
    - a(t): linear from 0 to 1
- Whether to calculate the increments of x or y first in each step.

### Preliminary test on N=60, ins=0, dt=0.5, c0=0.2

![oscillatory behavior of x](https://raw.githubusercontent.com/haoyudoingthings/Annealing-Algorithms/main/Simulated%20Bifurcation/fig/output.png)

x reaches equilibrium only after t~125; therefore we shouldn't use any `steps` < 125/dt. We will use `steps` = int(150/dt) through out the benchmark experiments.

### Calculate increments of x first and then y
The sequence of calculating the increments of x and y might affect the result. We will test on it in this section.

#### Average cut values

![avg cut x->y](https://raw.githubusercontent.com/haoyudoingthings/Annealing-Algorithms/main/Simulated%20Bifurcation/fig/output2.png)

#### Times reaching the optimal cut value

![success rate x->y](https://raw.githubusercontent.com/haoyudoingthings/Annealing-Algorithms/main/Simulated%20Bifurcation/fig/output3.png)

Best:

- N=60: (dt, c0)=(0.25, 0.2), 37 successes
- N=80: (dt, c0)=(0.5, 0.4), (0.75, 0.2), (0.75, 0.5), 4 successes
- N=100: (dt, c0)=(0.75, 0.3), 1 success

#### Error rate of the best solution, averaged over 10 problem instances

![error rate x->y](https://raw.githubusercontent.com/haoyudoingthings/Annealing-Algorithms/main/Simulated%20Bifurcation/fig/output4.png)

Best:

- N=60: (dt, c0)=(0.75, 0.3)
- N=80: (dt, c0)=(0.25, 0.3)
- N=100: (dt, c0)=(0.75, 0.3)

### Calculate increments of y first and then x

#### Average cut values

![avg cut y->x](https://raw.githubusercontent.com/haoyudoingthings/Annealing-Algorithms/main/Simulated%20Bifurcation/fig/output5.png)

#### Times reaching the optimal cut value

![success rate y->x](https://raw.githubusercontent.com/haoyudoingthings/Annealing-Algorithms/main/Simulated%20Bifurcation/fig/output6.png)

Best:

- N=60: (dt, c0)=(1.25, 0.5), 80 successes
- N=80: (dt, c0)=(0.75, 0.5), (1.25, 0.5), 6 successes
- N=100: no successes

#### Error rate of the best solution, averaged over 10 problem instances
![error rate y->x](https://raw.githubusercontent.com/haoyudoingthings/Annealing-Algorithms/main/Simulated%20Bifurcation/fig/output7.png)

Best:
- N=60: (dt, c0)=(0.75, 0.5)
- N=80: (dt, c0)=(1.25, 0.5)
- N=100: (dt, c0)=(1.25, 0.5)


The performance of calculating y first seems to be better than the alternative. Most importantly, the parameters that produce the best results differs substantially, which seems to imply that they behave very differently.

We will use the variant that calculates increments of y first in the following experiments (unless stated otherwise).

## Jun. 25 results

![jun25](https://raw.githubusercontent.com/haoyudoingthings/Annealing-Algorithms/main/Simulated%20Bifurcation/fig/success_rate.png)

### Observations

1. Optimal c0 becomes larger as N increases, despite the fact that problem matrices have already been normalized by a factor of $$\sqrt{\frac{N-1}{\sum_{i, j} J_{ij}^2}}$$.
2. In some cases, there are sudden drops in success rate as c0 increases. The drops happen at the same c0 for each dt for every N (see: dt=0.5, c0=4.5-5.5; dt=0.75, c0=2.0-2.5).

### Guesses

1. The normalization factor is based on the [original paper](https://www.science.org/doi/10.1126/sciadv.aav2372), where the author said the choice was based on random matrix theory.
2. Since increasing c0 causes the oscillation frquency to increase, there might be a point where the oscillation is too violent for the numerical method to keep up, causing the sudden drop in success rate.

## Jun. 26 results

![99.5%](https://raw.githubusercontent.com/haoyudoingthings/Annealing-Algorithms/main/Simulated%20Bifurcation/fig/995_target_rate.png)

![99.0%](https://raw.githubusercontent.com/haoyudoingthings/Annealing-Algorithms/main/Simulated%20Bifurcation/fig/99_target_rate.png)

### Observations

1. Optimal setting of dt and c0 are the same for all three metrics (success rate, >99% target and >99.5% target rate), seems like there's no abnormal distribution of cut values.
2. The sudden drops in success/target rate are more pronounced when allowing for suboptimal solutions.

## Jul. 29 results

![jul29-100](https://raw.githubusercontent.com/haoyudoingthings/Annealing-Algorithms/main/Simulated%20Bifurcation/fig/jul29-100.png)

![jul29-995](https://raw.githubusercontent.com/haoyudoingthings/Annealing-Algorithms/main/Simulated%20Bifurcation/fig/jul29-995.png)

![jul29-99](https://raw.githubusercontent.com/haoyudoingthings/Annealing-Algorithms/main/Simulated%20Bifurcation/fig/jul29-99.png)

### Observations

1. The optimal value of c0 indeed increases as the problem size gets larger.
2. Smaller dt doesn;t improve the result too much as long as it's small enough.
3. The region where dt was too large for the numerical method seems to be the same for all settings and metrics. Maybe the region is general for all problems and we can identify it beforehand?
4. There's a small dip in target/success rate at (dt, c0) = (0.375, 0.5). I have no idea what might cause it or if it's important.

## TODO

- [x] Insert graphs to this file
- [x] Statistics on confidence of result, i.e. rate (%) of result within % of optimal result
- [ ] Provide test cases of 2K node (sparse and dense)
- [x] Parameter tuning - extend range for dt, c0
- [x] Parameter tuning - further extend range for smaller dt
- [ ] Parameter tuning - Identify the region in which dt is too large for our numerical method.
- [ ] Parameter tuning - experiment on a(t)
- [ ] Use FPGA to speed up simulation and compare it with software version – Justin will provide the support
- [ ] Benchmark the same problem sets on [Toshiba SBM](https://aws.amazon.com/marketplace/pp/prodview-f3hbaz4q3y32y)