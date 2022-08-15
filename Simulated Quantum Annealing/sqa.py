# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# This notebook aims to recreate an annealer machine running simulated quantum annealing.
# 
# There are two designs present. One employs sequential update on the spins without global moves, and the other updates randomly and incorporates global moves.
# Reference to the first design: [OpenCL-based design of an FPGA accelerator for quantum annealing simulation](https://link.springer.com/article/10.1007%2Fs11227-019-02778-w)
# Reference to the second design: [Quantum annealing by the path-integral Monte Carlo method: The two-dimensional random Ising model](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.66.094203)
# 
# Another method of simulating quantum annealing using classical spin dynamics (ditching quantum entanglements) is also presented.
# Reference 1: [Classical signature of quantum annealing](https://arxiv.org/abs/1305.4904)
# Reference 2: [How "Quantum" is the D-Wave Machine?](https://arxiv.org/abs/1401.7087)

# %%
import numpy as np
from scipy.sparse import block_diag


# %%
def one_SQA_run(J, h, trans_fld_sched, M, T, sd=None, init_state=None, return_pauli_z=False, return_z_hist=False):
    """
    One path-integral Monte Carlo simulated quantum annealing run over the full transverse field strength schedule.
    The goal is to find a state such that sum(J[i, j]*state[i]*state[j]) + sum(h[i]*state[i]) is minimized.
    
    Parameters:
        J (2-D array of float): The matrix representing the coupling field of the problem.
        h (1-D array of float): The vector representing the local field of the problem.
        trans_fld_sched (list[float]): The transeverse field strength schedule for QA.
                                       The number of iterations is implicitly the length of trans_fld_schedule.
        M (int): Number of Trotter replicas. To simulate QA precisely, M should be chosen such that T M / Gamma >> 1.
        T (float): Temperature parameter. Smaller T leads to higher probability of finding ground state.
        sd (default=None): Seed for numpy.random.default_rng().
        init_state (1-D array of int, default=None): The boolean vector representing the initial state.
                                                     If None, a random state is chosen.
        return_pauli_z (bool, default=False): If True, returns a N-spin state averaged over the imaginary time dimension.
                                              If False, returns the raw N*M-spin state.
    
    Return: final_state (1-D array of int)
    """
    rng = np.random.default_rng(seed=sd)

    # if np.any(np.diag(J)):
    #     raise ValueError("Diagonal elements of J should be 0")

    # J: block sparse matrices with block size of (N, N)
    N = J.shape[0]
    j = 0.5*(J + J.T) # making sure J is symmetric
    # j = np.kron(np.eye(M), j/M) # block diagonal of J, repeated M times and divided by M
    j = block_diag([j/M]*M) # block diagonal of J, repeated M times and divided by M
    
    h_extended = np.repeat(h/M, M)

    Jp_terms = np.eye(N*M, k=N) + np.eye(N*M, k=N*(1-M))
    Jp_terms = 0.5*(Jp_terms + Jp_terms.T)
    
    if init_state is None:
        state = 2 * rng.binomial(1, 0.5, N*M) - 1
    else:
        state = np.tile(init_state, M)
    
    if return_z_hist:
        z_hist = []
    
    # print(j.shape[0])

    for Gamma in trans_fld_sched:
        Jp_coef = -0.5 * T * np.log(np.tanh(Gamma / M / T))
        
        # First design (Tohoku)
        for flip in range(N*M): # can be parallelized
            delta_E = -4 * (j - Jp_coef * Jp_terms)[flip].dot(state) * state[flip] - 2 * h_extended[flip] * state[flip]
            if rng.binomial(1, np.minimum(np.exp(-delta_E/T), 1.)):
                state[flip] *= -1

        # # Second design (PRB.66.094203)
        # # Local move
        # flip = np.random.randint(N*M)
        # delta_E = -4 * (J - Jp_coef * Jp_terms)[flip].dot(state) * state[flip] - 2 * h[flip] * state[flip]
        # if np.random.binomial(1, np.minimum(np.exp(-delta_E/T), 1.)):
        #     state[flip] *= -1
        
        # # Global move
        # flip = (np.arange(N*M) % N == np.random.randint(N))
        # delta_E = -4 * J[flip].dot(state).dot(state[flip]) - 2 * h[flip].dot(state[flip])
        # if np.random.binomial(1, np.minimum(np.exp(-delta_E/T), 1.)):
        #     state[flip] *= -1
        
        # state_history.append(state.copy())

        if return_z_hist:
            z_hist.append(np.sum(np.reshape(np.array(state), (M, -1)), axis=0) / M)
    
    if return_z_hist:
        return z_hist
    if return_pauli_z:
        return np.sum(np.reshape(np.array(state), (M, -1)), axis=0) / M
    else:
        return state


# %%
def one_CTQMC_run(J, h, trans_fld_sched, T, sd=None, init_state=None, return_z_history=False):
    """
    One SQA run with continuous-time Monte Carlo method.

    Return: pauli_z observables
    """
    def find_seg_ind(a, x, lo=0, hi=None):
        """
        Find the index of the segment that contains x.
        If all elements of a are larger than x, -1 is returned.
        """
        if lo < 0:
            raise ValueError('lo must be non-negative')
        if hi is None:
            hi = len(a)
        # if x < a[0]:
        #     return -1
        while lo < hi:
            mid = (lo + hi)//2
            if x < a[mid]:
                hi = mid
            else:
                lo = mid + 1
        return lo
    
    def sum_spin(i, t0=0, t1=None):
        """
        Integrate value of spin i over the imaginary time range (t0, t1)
        If t0 > t1, the time range is (t0, beta) + (0, t1)
        """
        if t1 is None:
            t1 = beta
        
        if t0 > t1:
            return sum_spin(i, t0, beta) + sum_spin(i, 0, t1)

        if len(cuts_pos[i]) == 0 or len(cuts_pos[i]) == 1:
            if t1 == t0:
                return beta * cuts_val[i][0]
            else:
                return (t1 - t0) * cuts_val[i][0]

        lo = find_seg_ind(cuts_pos[i], t0)
        hi = find_seg_ind(cuts_pos[i], t1, lo=lo)
        
        if lo == hi:
            return (t1 - t0) * cuts_val[i][lo-1]

        output = (cuts_pos[i][lo] - t0) * cuts_val[i][lo-1] + (t1 - cuts_pos[i][hi-1]) * cuts_val[i][hi-1]
        for seg in range(lo+1, hi):
            output += (cuts_pos[i][seg] - cuts_pos[i][seg-1]) * cuts_val[i][seg-1]
        # mean /= t1 - t0

        return output
    
    rng = np.random.default_rng(seed=sd)
    N = J.shape[0]
    beta = 1/T

    # Poisson process:
    # No events for a time interval t: Pr(N(t)=0) = e^(-r*t)
    # Let T1 be the time of the first event. Then, Pr(T1>t) = Pr(N(t)=0) = e^(-r*t)
    # N(t) is a Poisson process of rate r: Pr(N(t)=k) = e^(-r*t) * (r*t)^k / k!
    
    # Initialization
    # generate new cuts
    cuts_pos = [sorted(rng.uniform(0, beta, rng.poisson(trans_fld_sched[0] * beta)).tolist()) for _ in range(N)]
    cuts_val = [[(1 - 2 * rng.binomial(1, 0.5)) for _ in range(max(len(cuts_pos[i]), 1))] for i in range(N)]
    # cuts_pos = [sorted(rng.uniform(0, beta, rng.poisson(trans_fld_sched[0] * beta) // 2 * 2).tolist()) for _ in range(N)]
    # cuts_val_0 = 1 - 2 * rng.binomial(1, 0.5)
    # cuts_val = [[cuts_val_0 * (-1)**j for j in range(max(len(cuts_pos[i]), 1))] for i in range(N)]

    # clean up needless cuts
    for i in range(N):
        for j in range(len(cuts_pos[i])-1, -1, -1):
            if cuts_val[i][j] == cuts_val[i][j-1]:
                cuts_pos[i].pop(j)
                if len(cuts_val[i]) > 1:
                    cuts_val[i].pop(j)
    
    if return_z_history:
        z_hist = []

    for Gamma in trans_fld_sched:
        for i in range(N):
            # Is the length of imaginary time 1 or beta? -> beta

            # generate new cuts
            new_cuts_num = rng.poisson(Gamma * beta)
            new_cuts = rng.uniform(0, beta, new_cuts_num)
            new_cuts.sort()

            # inserts into original cuts
            lo = 0
            for new_cut in new_cuts:
                if len(cuts_pos[i]) == 0:
                    cuts_pos[i].append(new_cut)
                else:
                    lo = find_seg_ind(cuts_pos[i], new_cut, lo=lo)
                    cuts_pos[i].insert(lo, new_cut)
                    cuts_val[i].insert(lo, cuts_val[i][lo-1])

            # check if cuts_pos[i] is sorted
            # if not all([cuts_pos[i][x] <= cuts_pos[i][x+1] for x in range(len(cuts_pos[i])-1)]):
            #     print(f"cuts_pos[{i}] is not sorted")

            # update segment values
            if len(cuts_pos[i]) <= 1:
                sum_spins = np.zeros(N)
                for k in range(N): # parallelizable
                    if k != i and J[i, k] != 0:
                        sum_spins[k] = sum_spin(k)
                delta_E = -2 * cuts_val[i][j] * (J[i].dot(sum_spins) + h[i] * beta)
                if rng.binomial(1, min(1, np.exp(-delta_E))/2):
                    cuts_val[i][0] *= -1
            else:
                for j in range(len(cuts_pos[i])): # parallelizable
                    sum_spins = np.zeros(N)
                    if j == len(cuts_pos[i])-1:
                        for k in range(N): # parallelizable
                            if k != i and J[i, k] != 0:
                                sum_spins[k] = sum_spin(k, cuts_pos[i][j], cuts_pos[i][0])
                        delta_E = -2 * cuts_val[i][j] * (J[i].dot(sum_spins) + h[i] * (beta - cuts_pos[i][j] + cuts_pos[i][0]))
                    else:
                        for k in range(N): # parallelizable
                            if k != i and J[i, k] != 0:
                                sum_spins[k] = sum_spin(k, cuts_pos[i][j], cuts_pos[i][j+1])
                        delta_E = -2 * cuts_val[i][j] * (J[i].dot(sum_spins) + h[i] * (cuts_pos[i][j+1] - cuts_pos[i][j]))
                    # for k in range(N): # parallelizable
                    #     if k != i:
                    #         sum_spins[k] = sum_spin(k, cuts_pos[i][j-1], cuts_pos[i][j])
                    # delta_E = -2 * cuts_val[i][j-1] * (J[i].dot(sum_spins) + h[i] * (cuts_pos[i][j] - cuts_pos[i][j-1]))
                    if rng.binomial(1, min(1, np.exp(-delta_E))/2):
                        cuts_val[i][j] *= -1
            
            # clean up unnecessary cuts
            for j in range(len(cuts_pos[i])-1, -1, -1):
                if cuts_val[i][j] == cuts_val[i][j-1]:
                    cuts_pos[i].pop(j)
                    if len(cuts_val[i]) > 1:
                        cuts_val[i].pop(j)
        
        if return_z_history:
            z_hist.append(np.array([sum_spin(i)/beta for i in range(N)]))
    
    if return_z_history:
        return z_hist
    return np.array([sum_spin(i)/beta for i in range(N)])


# %%
def one_SD_run(J, h, trans_fld_sched, T, sd=None, return_x_history=False, dt=0.1):
    """
    One annealing based on classical spin dynamics run over the full transverse field strength schedule.
    Each spin is represented as a classical spin on the x-z plane. The state variables are the inclination angles with the z-axis.
    The goal is to find a state such that sum(J[i, i]*cos(state[i])) + sum(J[i, j]*cos(state[i])*cos(state[j])) is minimized.
    
    Parameters:
        J (2-D array of float): The matrix representing the coupling field of the problem.
        h (1-D array of float): The vector representing the local field of the problem.
        trans_fld_sched (list[float]): The transeverse field strength schedule for QA.
                                       The number of iterations is implicitly the length of trans_fld_schedule.
        T (float): Temperature parameter. Smaller T leads to higher probability of finding ground state.
                   If T=0, the solution is numerically obtained by the equations of motion.
                   Otherwise (T>0), the solution is obtained by Metropolis algorithm.
        sd (default=None): Seed for numpy.random.
        return_x_history (bool, default=False): True to return history of x additionally.
        dt (float, default=0.1): The time step. Only in use when T=0.
    
    Return: final_state (1-D array of int)
    """
    np.random.seed(sd)

    if np.any(np.diag(J)):
        raise ValueError("Diagonal elements of J should be 0")
    
    N = J.shape[0]
    j = 0.5*(J + J.T) # making sure J is symmetric

    state = 1.5 * np.pi * np.ones(N)
    
    x_history = []
    # Numerical solution to the equations of motion
    # if T == 0:
    #     ang_v = np.zeros(N)
    #     for Gamma in trans_fld_sched:
    #         ang_v += (Gamma * np.cos(state) - (h + 2 * j.dot(np.cos(state))) * np.sin(state)) * dt
    #         state += ang_v * dt
    #         state %= 2 * np.pi
    #         x_history.append(state.copy())

    # Metropolis-type update
    # else:
    for Gamma in trans_fld_sched:
        new_state = 2 * np.pi * np.random.rand(N)
        delta_E = (j.dot(np.cos(state)) + h) * (np.cos(new_state) - np.cos(state)) + Gamma * (np.sin(new_state) - np.sin(state))
        accepted = np.random.binomial(1, np.minimum(np.exp(-delta_E/T), 1.))
        state = new_state * accepted + state * (1 - accepted)
        x_history.append(state.copy())
    
    if return_x_history:
        return np.sign(np.cos(state)), x_history
    return np.sign(np.cos(state))


# %%
def main():
    """
    A simple showcase
    """
    import time
    import matplotlib.pyplot as plt

    sd = 7

    num_par = [80, 68, 32, 15, 5]
    N = len(num_par)

    J = np.outer(num_par, num_par)
    offset = sum(np.diag(J))
    np.fill_diagonal(J, 0)
    h = np.zeros(N)

    norm_coef = np.sqrt(J.shape[0] / (np.sum(J**2) + 0.5 * np.sum(h**2))) # normalization
    J = J * norm_coef
    h = h * norm_coef

    M = 8
    T = 0.1

    steps = 1000
    Gamma0 = 10
    Gamma1 = 1e-8
    decay_rate = (Gamma1 / Gamma0)**(1/(steps-1))
    schedule = [Gamma0 * decay_rate**i for i in range(steps)]

    # state_history = []

    start_time = time.time()
    ans1 = one_SQA_run(J, h, schedule, M, T, sd=sd, return_pauli_z=True)
    total_time1 = time.time() - start_time

    print(f'number partition: {num_par}')
    print("simulated quantum annealing")
    print(f"ground state: {ans1}; time: {total_time1} s")

    # start_time = time.time()
    # ans2 = one_CTQMC_run(J, h, schedule, T, sd=sd)
    # total_time2 = time.time() - start_time

    # print(f"ground state (continuous time): {ans2}; time: {total_time2} s")


    # true_percent = []
    # for i in range(N):
    #     true_percent.append([0.5*(np.sum(a[i::N])/M + 1) for a in state_history])


    # fig = plt.figure(dpi=120)
    # x = np.arange(steps)
    # #y = [sum(ans_dict[b].values())/3 for b in sorted(args_lst, key=lambda a: sum(ans_dict[a].values()))]

    # for i in range(N):
    #     plt.plot(x, true_percent[i], label=f"spin {i+1}")
    # plt.legend()


# %%
if __name__ == "__main__":
    main()


# %%
