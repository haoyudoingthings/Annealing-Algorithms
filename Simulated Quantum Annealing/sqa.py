# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# This notebook aims to recreate an annealer machine running simulated quantum annealing.
# 
# See https://doi.org/10.1109/ICRC.2017.8123652

# %%
import numpy as np
import scipy as sp
import numba as nb
import time
import matplotlib.pyplot as plt
from scipy.sparse import bsr_matrix


# %%
#@nb.njit(parallel=False)
def one_SQA_run(J, trans_fld_sched, M, T, ansatz_state=None):
    """
    One simulated quantum annealing run over the full transverse field strength schedule.
    The goal is to find a state such that sum(J[i, i]*state[i]) + sum(J[i, j]*state[i]*state[j]) is minimized.
    
    Parameters:
        J (2-D array of float): The matrix representing the local and coupling field of the problem.
                                Local fields should be on the diagonal of the input matrix.
        trans_fld_sched (list[float]): The transeverse field strength schedule for QA.
                                       The number of iterations is implicitly the length of trans_fld_schedule.
        M (int): Number of Trotter replicas. Larger M leads to higher probability of finding ground state.
        T (float): Temperature parameter. Smaller T leads to higher probability of finding ground state.
        ansatz_state (1-D array of bool, default=None): The boolean vector representing the initial state.
                                                        If None, a random state is chosen.
    
    Return: final_state (1-D array of bool)
    """
    
    # J and Q are block sparse matrices with block size of (N, N)
    N = J.shape[0]
    J = 0.5*(J + J.T) # making sure J is symmetric
    J = np.kron(np.eye(M), J/M) # block diagonal of J, repeated M times and divided by M
    Jp_terms = np.eye(N*M, k=N) + np.eye(N*M, k=N*(1-M))
    Jp_terms = 0.5*(Jp_terms + Jp_terms.T)
    
    Q = 4*J - 6*np.diag(np.diag(J)) + 4*np.diag(np.sum(J, axis=0))
    Qp_terms = 4*Jp_terms + 4*np.eye(N*M)
    
    if ansatz_state is None:
        state = (np.random.binomial(1, 0.5, N*M) == 1)
    else:
        state = np.tile(ansatz_state, M)
    
    
    for Gamma in trans_fld_sched:
        Jp_coef = -0.5 * T * np.log(np.tanh(Gamma / M / T))
        
        # Local move
        flip = np.random.randint(N*M)
        delta_E = 2 * (1 - 2*state[flip]) * np.sum((Q - Jp_coef * Qp_terms)[flip][state]) + Q[flip, flip]
        if np.random.binomial(1, np.minimum(np.exp(-delta_E/T), 1.)):
            state[flip] ^= True
        
        # Global move
        flip = (np.arange(N*M) % N == np.random.randint(N))
        delta_E = np.sum(2 * (1 - 2*state[flip]) * np.sum(Q[flip][:, state], axis=1) + Q[flip, flip])
        if np.random.binomial(1, np.minimum(np.exp(-delta_E/T), 1.)):
            state ^= flip
        
        state_history.append(state.copy())
    
    return state

# %% [markdown]
# In the local move section,
# 
# - If the coupling between replicas appears to be (Q - Jp_coef * Qp_terms), then the resulting state has a tendency to be biased towards +1 (True).
# - If the coupling between replicas appears to be (Q + Jp_coef * Qp_terms), then the resulting state has a tendency to be biased towards -1 (False).
# 
# (Q - Jp_coef * Qp_terms) should be the correct one if the goal is to minimize the inner product over J.
# %% [markdown]
# According to https://doi.org/10.1103/PhysRevB.66.094203, M\*T should be on the order of coupling strengths |J|, but not smaller.

# %%
J = np.array([[-1., 0., 0., 0.], [0., 1., 0., 0.], [0., 0., 1., 0.], [0., 0., 0., 1.]])
N = J.shape[0]
ansatz = np.zeros(J.shape[0], dtype=np.bool_)

M = 40
T = 0.05

steps = 10**4
Gamma0 = 3
#schedule = [Gamma0 / (1 + a) for a in range(steps)]
schedule = np.linspace(Gamma0, 10**(-8), num=steps)


# %%
np.random.seed(0)
start_time = time.time()
ans = one_SQA_run(J, schedule, M)
total_time = time.time() - start_time
print(f'time: {total_time} s')


# %%
for i in range(N):
    print(f"Percentage of +1 for spin {i+1}: {np.sum(ans[i::N])/M:.1%}")


# %%
np.sum(np.reshape(ans, (M, N)), axis=0) > 0.5*M

# %% [markdown]
# Evolution of spins when (Q - Jp_coef * Qp_terms)

# %%
state_history = []

np.random.seed(0)
start_time = time.time()
ans = one_SQA_run(J, schedule, M, T)
total_time = time.time() - start_time
print(f'time: {total_time} s')


# %%
true_percent = []
for i in range(N):
    true_percent.append([np.sum(a[i::N])/M for a in state_history])


# %%
fig = plt.figure(dpi=120)
x = np.arange(steps)
#y = [sum(ans_dict[b].values())/3 for b in sorted(args_lst, key=lambda a: sum(ans_dict[a].values()))]

for i in range(N):
    plt.plot(x, true_percent[i], label=f"spin {i+1}")
plt.legend()


# %%
Jp = [-0.5 * T * np.log(np.tanh(Gamma / M / T)) for Gamma in schedule]


# %%
Jp[:5]


# %%
Jp[-5:]

# %% [markdown]
# Evolution of spins with ansatz = all False

# %%
state_history = []

np.random.seed(0)
start_time = time.time()
ans = one_SQA_run(J, schedule, M, T, ansatz_state=ansatz)
total_time = time.time() - start_time
print(f'time: {total_time} s')


# %%
true_percent = []
for i in range(N):
    true_percent.append([np.sum(a[i::N])/M for a in state_history])


# %%
fig = plt.figure(dpi=120)
x = np.arange(steps)
#y = [sum(ans_dict[b].values())/3 for b in sorted(args_lst, key=lambda a: sum(ans_dict[a].values()))]

for i in range(N):
    plt.plot(x, true_percent[i], label=f"spin {i+1}")
plt.legend()

# %% [markdown]
# Results when SQA is running natively with spin variables ($s_i = \pm 1$)

# %%
#@nb.njit(parallel=False)
def one_SQA_run_Ising(J, trans_fld_sched, M, T, ansatz_state=None):
    """
    One simulated quantum annealing run over the full transverse field strength schedule.
    The goal is to find a state such that sum(J[i, i]*state[i]) + sum(J[i, j]*state[i]*state[j]) is minimized.
    
    Parameters:
        J (2-D array of float): The matrix representing the local and coupling field of the problem.
                                Local fields should be on the diagonal of the input matrix.
        trans_fld_sched (list[float]): The transeverse field strength schedule for QA.
                                       The number of iterations is implicitly the length of trans_fld_schedule.
        M (int): Number of Trotter replicas. Larger M leads to higher probability of finding ground state.
        T (float): Temperature parameter. Smaller T leads to higher probability of finding ground state.
        ansatz_state (1-D array of bool, default=None): The boolean vector representing the initial state.
                                                        If None, a random state is chosen.
    
    Return: final_state (1-D array of bool)
    """
    
    # J and Q are block sparse matrices with block size of (N, N)
    N = J.shape[0]
    J = 0.5*(J + J.T) # making sure J is symmetric
    J = np.kron(np.eye(M), J/M) # block diagonal of J, repeated M times and divided by M
    
    h = np.diag(J).copy() # separate local terms from couplings
    np.fill_diagonal(J, 0)
    
    Jp_terms = np.eye(N*M, k=N) + np.eye(N*M, k=N*(1-M))
    Jp_terms = 0.5*(Jp_terms + Jp_terms.T)
    
    #Q = 4*J - 6*np.diag(np.diag(J)) + 4*np.diag(np.sum(J, axis=0))
    #Qp_terms = 4*Jp_terms + 4*np.eye(N*M)
    
    if ansatz_state is None:
        state = 2 * np.random.binomial(1, 0.5, N*M) - 1
    else:
        state = np.tile(ansatz_state, M)
    
    
    for Gamma in trans_fld_sched:
        Jp_coef = -0.5 * T * np.log(np.tanh(Gamma / M / T))
        
        # Local move
        flip = np.random.randint(N*M)
        delta_E = -4 * (J - Jp_coef * Jp_terms)[flip].dot(state) * state[flip] - 2 * h[flip] * state[flip]
        if np.random.binomial(1, np.minimum(np.exp(-delta_E/T), 1.)):
            state[flip] *= -1
        
        # Global move
        flip = (np.arange(N*M) % N == np.random.randint(N))
        delta_E = -4 * J[flip].dot(state).dot(state[flip]) - 2 * h[flip].dot(state[flip])
        if np.random.binomial(1, np.minimum(np.exp(-delta_E/T), 1.)):
            state[flip] *= -1
        
        state_history.append(state.copy())
    
    return state


# %%
J = np.array([[-1., 0., 0., 0.], [0., 1., 0., 0.], [0., 0., 1., 0.], [0., 0., 0., 1.]])
N = J.shape[0]
ansatz = np.zeros(J.shape[0], dtype=np.bool_)

M = 40
T = 0.05

steps = 10**4
Gamma0 = 3
#schedule = [Gamma0 / (1 + a) for a in range(steps)]
schedule = np.linspace(Gamma0, 10**(-8), num=steps)


# %%
state_history = []

np.random.seed(0)
start_time = time.time()
ans = one_SQA_run_Ising(J, schedule, M, T)
total_time = time.time() - start_time
print(f'time: {total_time} s')


# %%
np.sum(np.reshape(ans, (M, N)), axis=0)


# %%
true_percent = []
for i in range(N):
    true_percent.append([0.5*(np.sum(a[i::N])/M + 1) for a in state_history])


# %%
fig = plt.figure(dpi=120)
x = np.arange(steps)
#y = [sum(ans_dict[b].values())/3 for b in sorted(args_lst, key=lambda a: sum(ans_dict[a].values()))]

for i in range(N):
    plt.plot(x, true_percent[i], label=f"spin {i+1}")
plt.legend()


# %%



