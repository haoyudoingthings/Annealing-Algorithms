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

**This conclusion does not make much sense. See Aug. 2 results for more clarification.**

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

## Aug. 2 results

I've (i) benchmarked our dSB algorithm with G22 problem (sparse 2K node problem), (ii) benchmarked [Toshiba SBM](https://aws.amazon.com/marketplace/pp/prodview-f3hbaz4q3y32y) with BiqMac g05 problem set and G22, and (iii) perhaps discovered the importance of a0.

### G22 results

![Aug2-1](https://raw.githubusercontent.com/haoyudoingthings/Annealing-Algorithms/main/Simulated%20Bifurcation/fig/aug2-1.png)

#### Observations

1. Seems like the optimal value of c0 is very different from the g05 cases. Perhaps the optimal value of c0 is related to the density of problem matrix?
2. Most of the results are within 99% of optimal cut value, but none of them reaches ground state.

### Toshiba SBM results

The results are all obtained with preset parameters and loops = 3 (960 runs in total per problem instance).

1. BiqMac g05
    - Target = 100% of optimal cut
        - N=60: 1167/9600, 12.2% success rate
        - N=80: 642/9600, 6.7% success rate
        - N=100: 123/9600, 1.3% success rate
    - Target = 99.5% of optimal cut
        - N=60: 3011/9600, 31.4% success rate
        - N=80: 1932/9600, 20.1% success rate
        - N=100: 1212/9600, 12.6% success rate
    - Target = 99.0% of optimal cut
        - N=60: 4963/9600, 51.7% success rate
        - N=80: 3569/9600, 37.2% success rate
        - N=100: 2632/9600, 27.4% success rate
2. G22
    - Target = 100%: 5/960, 0.5% success rate
    - Target = 99.5%: 960/960, 100.0% success rate
    - Target = 99.0%: 960/960, 100.0% success rate

#### Observations

1. The preset parameters are very good at solving G22, but not great at solving g05. Perhaps they are good for sparse problems only?

#### Note

There is an article about benchmarking the performance of [Toshiba SBM](https://aws.amazon.com/marketplace/pp/prodview-f3hbaz4q3y32y) with Gset problems ([link](https://medium.com/toshiba-sbm/benchmarking-the-max-cut-problem-on-the-simulated-bifurcation-machine-e26e1127c0b0)). They did not mention any form of distribution or success rate though.

### Importance of a0

Assuming the pump schedule a(t) is linear, it can be written as

$$a(t) = a_0 \frac{t}{T}, 0 \leq t \leq T$$

So there are two parameters: maximum pump strength `a0` and total time `T`. Previous experiments all assumed `a0=1` is sufficient. Now let's see what effect these two coefficients have on the trajectories.

#### (a0, T) = (1.0, 150)

![Aug2-2](https://raw.githubusercontent.com/haoyudoingthings/Annealing-Algorithms/main/Simulated%20Bifurcation/fig/aug2-2.png)

#### (a0, T) = (1.0, 100)

![Aug2-4](https://raw.githubusercontent.com/haoyudoingthings/Annealing-Algorithms/main/Simulated%20Bifurcation/fig/aug2-4.png)

#### (a0, T) = (1.5, 150)

![Aug2-3](https://raw.githubusercontent.com/haoyudoingthings/Annealing-Algorithms/main/Simulated%20Bifurcation/fig/aug2-3.png)

#### (a0, T) = (1.5, 100)

![Aug2-5](https://raw.githubusercontent.com/haoyudoingthings/Annealing-Algorithms/main/Simulated%20Bifurcation/fig/aug2-5.png)

#### Observations

1. Comparing (a0, T) = (1.5, 150) to (1.0, 150), we can see that as a0 increases, the algorithm converges sooner.
2. Comparing (a0, T) = (1.5, 100) to (1.5, 150), we can see that the convergence comes even faster.
3. Comparing (a0, T) = (1.5, 150) to (1.0, 100), we can see that the trajectories are virtually identical. This is because the slope of a(t) is the same, so the only difference between the two cases is that (1.0, 100) terminates sooner than (1.5, 150) (notice the scale of x-axis is different).

## Aug. 9 results

### WK2000 results

![Aug9-1](https://raw.githubusercontent.com/haoyudoingthings/Annealing-Algorithms/main/Simulated%20Bifurcation/fig/aug9-wk2000.png)

The problem has too many edges to be tested on Toshiba SBM (max. 1,000,000 edges).

#### Observations

1. The result is significantly worse than previous test cases.
2. Optimal c0 is around 0.5 and probably smaller. This contradicts my speculation that denser and larger problem leads to larger optimal c0. Perhaps we also have to take edge weights into account?

### FPGA validation

We obtained different results on our FPGA implementation and python implementation. The behavior is vastly different from the very first iteration. There are a few differences in the algorithm:

1. When taking `sign(x)`, the function is valued at -1 when x=0 in FPGA while it is valued at 0 in python. This difference makes a notable difference in the very first step of the algorithm when x is initialized at 0, but it shouldn't affect the overall behavior.
2. Floating point is single precision in FPGA while it is whatever is used in python. This may lead to a little inconsistencies but the overall behavior shouldn't change too much.

We later realized the hardware synthesis part is corrupted, and also verified that the software simulation of FPGA implementation has largely the same behavior as my python script.

## Aug. 16 results

### WK2000 results

![Aug16](https://raw.githubusercontent.com/haoyudoingthings/Annealing-Algorithms/main/Simulated%20Bifurcation/fig/aug16.png)

Benchmarked on a wider range of parameters.

#### Observation

Doesn't seem like there is a smooth change in success rate as the smaller problems. Or perhaps the change is over a much smaller region of c0?

### FPGA validation

Tested on `g05_60.0` with y initialized at 0.01 for every spin. The first step has exactly the same value, but the end result is different. This is probably due to the difference in floating point precision.

Also, even when initial y is randomized (between -0.01 and 0.01), the 1000 runs for each problem always result in the same cut value. Justin theorized the reason might be that the local minima are close enough that the precision problem caused them to always result in the same solution.

## Aug. 23 results

### FPGA validation

The problem of every run obtaining the same results has been solved. As it turned out, my dumbass wrote the random initialization outside of the for-loop.

After the fix, the results can finally be compared. The following tests use the settings `dt=0.25` and `c0=3.5, 4.5, 6` for `N=60, 80, 100` respectively:

#### Python implementation

```
Target: 100% of optimal cut value
N=60 success rate: 42.8%
N=80 success rate: 34.9%
N=100 success rate: 13.8%
```

#### FPGA implementation

```
Target: 100% of optimal cut value
N=60 success rate: 0.0%
N=80 success rate: 0.0%
N=100 success rate: 0.0%
```

The results do not match at all.

There are two obvious differences between the python and FPGA implementation:

1. Convention of `sign(x)` when `x=0`
2. Floating point number precision
3. Padding the number of variables to multiples of 64 is needed for the FPGA implementation

After modifying the python implementation to control for the first two factors and making sure the padded variables are all 0, the problem still remains (in the results above, all factors are controlled).

#### Case study

The history for x in the `(N, ins)=(60, 0)` instance:

- Python

![](https://github.com/haoyudoingthings/Annealing-Algorithms/blob/main/Simulated%20Bifurcation/fig/aug23-2.png?raw=true)

- FPGA

![](https://github.com/haoyudoingthings/Annealing-Algorithms/blob/main/Simulated%20Bifurcation/fig/aug23.png?raw=true)

Clearly there is something wrong with the FPGA implementation.

Since the behavior in the first ~30 steps is very similar, I suspect the problem might be boundary checking. Further testings are needed.

## TODO

- [x] Insert graphs to this file
- [x] Statistics on confidence of result, i.e. rate (%) of result within % of optimal result
- [x] Provide test cases of 2K nodes (sparse)
- [x] Provide test cases of 2K nodes (dense)
- [x] Parameter tuning - extend range for dt, c0
- [x] Parameter tuning - further extend range for smaller dt
- [ ] Parameter tuning - identify the region in which dt is too large for our numerical method
- [ ] Parameter tuning - experiment on a(t)
- [x] Use FPGA to speed up simulation and compare it with software version – Justin will provide the support
- [ ] Figure out what is causing the inconsistent behavior between the python and FPGA implementation
- [x] Benchmark the same problem sets on [Toshiba SBM](https://aws.amazon.com/marketplace/pp/prodview-f3hbaz4q3y32y)
- [ ] Test dSB (and SQA) on a small MLB problem (problem qubo can be obtained in [this repo](https://github.com/bol-edu/mobile-load-balancing))