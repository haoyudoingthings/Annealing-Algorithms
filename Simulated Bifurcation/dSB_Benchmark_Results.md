# dSB Benchmark Results

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

### TODO

- [x] Insert graphs to this file
- [ ] Statistics on confidence of result, i.e. rate (%) of result within % of optimal result
- [ ] Provide test cases of 2K node (sparse and dense)
- [ ] Parameter tuning – extend range for dt, c0, and experiment on a(t)
- [ ] Use FPGA to speed up simulation and compare it with software version – Justin will provide the support