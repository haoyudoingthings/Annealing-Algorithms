# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# This notebook aims to recreate an annealer machine running parallel tempering (replica exchange MCMC).

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
#@nb.njit(parallel=False)
def one_PT_run(Q, num_iter, re_intv, temp_seq, ansatz_state=None):
    """
    One parallel tempering run over the specified number of steps.
    
    Parameters:
        Q (2-D array of float64): The matrix representing the local and coupling field of the problem.
        num_iter (int): The number of iteration performed in PT.
        re_intv (int): The number of local sampling iterations between replica exchanges.
                       If one replica exchange is attempted at iteration k, the next will be at iteration k + re_int.
        temp_seq (list[float64]): The annealing temperature sequence. Each temperature corresponds to a replica.
        ansatz_state (1-D array of bool, default=None): The boolean vector representing the initial state.
                                                        If None, a random state is chosen.
    
    Return: final state of the replica with lowest energy (1-D array of bool)
    """
    
    # Q_coef[i][j]: local field of i if i==j; coupling strength if i!=j
    Q = 0.5*(Q + Q.T) # making sure Q is symmetric
    N = Q.shape[0]
    M = len(temp_seq) # number of replicas
    
    if ansatz_state is None:
        state = (np.random.binomial(1, 0.5, N) == 1)
    else:
        state = ansatz_state
    
    replicas = [state.copy() for _ in range(M)] # all replicas start from the same initial state, can be changed
    energy = np.sum(Q.dot(state).dot(state))
    energies = [energy for _ in range(M)] # energies corresponding to replicas
    
    for i in range(num_iter):
        for r in range(M): # parallelizable
            state = replicas[r]
            flip = np.random.randint(N)
            delta_E = 2 * (1 - 2*state[flip]) * np.sum(Q[flip][state]) + Q[flip, flip]
            if np.random.binomial(1, np.minimum(np.exp(-delta_E/temp_seq[r]), 1.)): # local move
                state[flip] ^= True
                energies[r] += delta_E
        
        if (i+1) % re_intv == 0: # only happens once every re_intv iterations
            s = np.random.randint(M-1) # exchange between replicas s and s+1 are chosen randomly, can be changed
            if np.random.binomial(1, np.minimum(np.exp((energies[s] - energies[s+1]) * (1/temp_seq[s] - 1/temp_seq[s+1])), 1.)):
                replicas[s], replicas[s+1] = replicas[s+1], replicas[s]
                energies[s], energies[s+1] = energies[s+1], energies[s]
    
    return replicas[energies.index(min(energies))]


# %%
Q = np.array([[-1., 0., 0., 0.], [0., 1., 0., 0.], [0., 0., 1., 0.], [0., 0., 0., 1.]])
ansatz = np.zeros(4, dtype=np.bool_)

num_iter = 100
re_intv = 10
TS = default_temp_schedule(10, 100., 0.4)


# %%
np.random.seed(0)
start_time = time.time()
ans = one_PT_run(Q, num_iter, re_intv, TS, ansatz_state=ansatz)
total_time = time.time() - start_time
print(f'ground state: {ans}; time: {total_time} s')


# %%



