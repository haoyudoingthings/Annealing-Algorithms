# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# This notebook aims to recreate an annealer machine running simulated annealing.

# %%
import numpy as np
import numba as nb
import time


# %%
def default_temp_schedule(num_iter, temp_start, decay_rate, mode='EXPONENTIAL'):
    """
    Generates a list of temperatures for annealing algorithms.
    
    Parameters:
        num_iter (int): Length of the list.
        temp_start (number): Value of the first element in the returned list.
        decay_rate (number): Multiplier for changing the temperature during annealing.
        mode (string, default='EXPONENTIAL'):
            Three modes are possible. Note the accepted ranges for decay_rate are different.
            'EXPONENTIAL':  T[i+1] = T[i] * (1 - decay_rate)           # 0 <= decay_rate < 1
            'INVERSE':      T[i+1] = T[i] * (1 - decay_rate * T[i])    # 0 <= decay_rate < 1/temp_start
            'INVERSE_ROOT': T[i+1] = T[i] * (1 - decay_rate * T[i]**2) # 0 <= decay_rate < 1/temp_start**2
    
    Return: temp_schedule (list[number])
    """
    
    if mode == 'EXPONENTIAL':
        if 0 <= decay_rate < 1:
            TS = [temp_start]
            for _ in range(num_iter - 1):
                TS.append(TS[-1] * (1 - decay_rate))
            return TS
        else:
            raise ValueError("decay_rate out of accepted range")
    elif mode == 'INVERSE':
        if 0 <= decay_rate < 1/temp_start:
            TS = [temp_start]
            for _ in range(num_iter - 1):
                TS.append(TS[-1] * (1 - decay_rate * TS[-1]))
            return TS
        else:
            raise ValueError("decay_rate out of accepted range")
    elif mode == 'INVERSE_ROOT':
        if 0 <= decay_rate < 1/temp_start**2:
            TS = [temp_start]
            for _ in range(num_iter - 1):
                TS.append(TS[-1] * (1 - decay_rate * TS[-1]**2))
            return TS
        else:
            raise ValueError("decay_rate out of accepted range")
    else:
        raise ValueError("mode not supported")


# %%
@nb.njit(parallel=False)
def one_SA_run(Q, temp_schedule, ansatz_state=None):
    """
    One simulated annealing run over the full temperature schedule.
    
    Parameters:
        Q (2-D array of float64): The matrix representing the local and coupling field of the problem.
        temp_schedule (list[float64]): The annealing temperature schedule.
                                       The number of iterations is implicitly the length of temp_schedule.
        ansatz_state (1-D array of bool, default=None): The boolean vector representing the initial state.
                                                        If None, a random state is chosen.
    
    Return: final_state (1-D array of bool)
    """
    
    # Q_coef[i][j]: local field of i if i==j; coupling strength if i!=j
    Q = 0.5*(Q + Q.T) # making sure Q is symmetric
    N = Q.shape[0]
    
    if ansatz_state is None:
        state = (np.random.binomial(1, 0.5, N) == 1)
    else:
        state = ansatz_state
    
    for temp in temp_schedule:
        flip = np.random.randint(N)
        delta_E = 2 * (1 - 2*state[flip]) * np.sum(Q[flip][state]) + Q[flip, flip]
        if np.random.binomial(1, np.minimum(np.exp(-delta_E/temp), 1.)):
            state[flip] ^= True
    
    return state


# %%
Q = np.array([[-1., 0., 0., 0.], [0., 1., 0., 0.], [0., 0., 1., 0.], [0., 0., 0., 1.]])
ansatz = np.zeros(4, dtype=np.bool_)
TS = default_temp_schedule(10000, 300., 0.001)


# %%
# With numba, not parallelized, first pass
np.random.seed(0)
start_time = time.time()
ans = one_SA_run(Q, TS, ansatz_state=ansatz)
total_time = time.time() - start_time
print(f'ground state: {ans}; time: {total_time} s')


# %%
# With numba, not parallelized, second pass
np.random.seed(0)
start_time = time.time()
ans = one_SA_run(Q, TS, ansatz_state=ansatz)
total_time = time.time() - start_time
print(f'ground state: {ans}; time: {total_time} s')


# %%



