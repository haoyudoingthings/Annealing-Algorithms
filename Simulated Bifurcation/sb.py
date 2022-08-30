# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# ### Note: Possibility of improvements over the choices of p(t), c0
# %% [markdown]
# This notebook aims to showcase Ising solvers running simulated bifurcation.
# Objective: Minimize J.dot(state).dot(state) + h.dot(state)
# 
# References:
# 1. https://advances.sciencemag.org/content/5/4/eaav2372
# 2. https://advances.sciencemag.org/content/7/6/eabe7953

# %%
import numpy as np


# %%
def one_aSB_run(J, PS, dt, c0, Kerr_coef=1., h=None, init_y=None, sd=None, return_x_history=False):
    """
    One (adiabatic) simulated bifurcation run over the full pump schedule.
    Angular frequency (a0) is set to 1 and absorbed into PS, dt and c0.
    Objective: Minimize J.dot(state).dot(state) + h.dot(state)
    
    Parameters:
        J (2-D array of float): The matrix representing the coupling field of the problem.
        PS (list[float]): The pump strength at each step. Number of iterations is implicitly len(PS).
        dt (float): Time step for the discretized time.
        c0 (float): Positive coupling strength scaling factor.
        Kerr_coef (float, default=1.): The Kerr coefficient.
        h (1-D array of float or None, default=None): The vector representing the local field of the problem.
        init_y (1-D array of float or None, default=None): Initial y. If None, then random numbers between 0.1 and -0.1 are chosen.
        sd (int or None, default=None): Seed for rng of init_y.
        return_x_history (bool, default=False): True to return history of x additionally.
    
    Return: final_state (1-D array of float)
    """
    
    if h is None:
        j = J
    else:
        j = np.zeros((J.shape[0]+1, J.shape[1]+1))
        j[:-1, :-1] = J
        j[:-1, -1] = 0.5*h
        j[-1, :-1] = 0.5*h.T
    
    x = np.zeros(j.shape[0])

    if init_y is None:
        np.random.seed(sd)
        y = np.random.uniform(-0.1, 0.1, j.shape[0])
    else:
        y = init_y.copy()
    
    if return_x_history:
        x_history = []
        for a in PS:
            x += y * dt
            y -= (Kerr_coef * x**3 + (1 - a) * x + 2 * c0 * j.dot(x)) * dt
            x_history.append(x.copy()) # for analysis purposes
            
        if h is None:
            return np.sign(x), x_history
        else:
            return np.sign(x[:-1]) * np.sign(x[-1]), x_history

    for a in PS:
        x += y * dt
        y -= (Kerr_coef * x**3 + (1 - a) * x + 2 * c0 * j.dot(x)) * dt
    
    if h is None:
        return np.sign(x)
    else:
        return np.sign(x[:-1]) * np.sign(x[-1])


# %%
def one_bSB_run(J, PS, dt, c0, h=None, init_y=None, sd=None, return_x_history=False):
    """
    One ballistic simulated bifurcation run over the full pump schedule.
    Angular frequency (a0) is set to 1 and absorbed into PS, dt and c0.
    Objective: Minimize J.dot(state).dot(state) + h.dot(state)
    
    Parameters:
        J (2-D array of float): The matrix representing the coupling field of the problem.
        PS (list[float]): The pump strength at each step. Number of iterations is implicitly len(PS).
        dt (float): Time step for the discretized time.
        c0 (float): Positive coupling strength scaling factor.
        h (1-D array of float or None, default=None): The vector representing the local field of the problem.
        init_y (1-D array of float or None, default=None): Initial y. If None, then random numbers between 0.1 and -0.1 are chosen.
        sd (int or None, default=None): Seed for rng of init_y.
        return_x_history (bool, default=False): True to return history of x additionally.
    
    Return: final_state (1-D array of float)
    """
    
    if h is None:
        j = J
    else:
        j = np.zeros((J.shape[0]+1, J.shape[1]+1))
        j[:-1, :-1] = J
        j[:-1, -1] = 0.5*h
        j[-1, :-1] = 0.5*h.T
    
    x = np.zeros(j.shape[0])

    if init_y is None:
        np.random.seed(sd)
        y = np.random.uniform(-0.1, 0.1, j.shape[0])
    else:
        y = init_y.copy()
    
    if return_x_history:
        x_history = []
        for a in PS:
            x += y * dt
            y -= ((1 - a) * x + 2 * c0 * j.dot(x)) * dt
            for i in range(j.shape[0]): # parallelizable
                if np.abs(x[i]) > 1:
                    x[i] = np.sign(x[i])
                    y[i] = 0
            x_history.append(x.copy()) # for analysis purposes

        if h is None:
            return np.sign(x), x_history
        else:
            return np.sign(x[:-1]) * np.sign(x[-1]), x_history
    
    for a in PS:
        x += y * dt
        y -= ((1 - a) * x + 2 * c0 * j.dot(x)) * dt
        for i in range(j.shape[0]): # parallelizable
            if np.abs(x[i]) > 1:
                x[i] = np.sign(x[i])
                y[i] = 0

    if h is None:
        return np.sign(x)
    else:
        return np.sign(x[:-1]) * np.sign(x[-1])


# %%
def one_dSB_run(J, PS, dt, c0, h=None, init_y=None, sd=None, return_x_history=False):
    """
    One discrete simulated bifurcation run over the full pump schedule.
    Angular frequency (a0) is set to 1 and absorbed into PS, dt and c0.
    Objective: Minimize J.dot(state).dot(state) + h.dot(state)
    
    Parameters:
        J (2-D array of float): The matrix representing the coupling field of the problem.
        PS (list[float]): The pump strength at each step. Number of iterations is implicitly len(PS).
        dt (float): Time step for the discretized time.
        c0 (float): Positive coupling strength scaling factor.
        h (1-D array of float or None, default=None): The vector representing the local field of the problem.
        init_y (1-D array of float or None, default=None): Initial y. If None, then random numbers between 0.1 and -0.1 are chosen.
        sd (int or None, default=None): Seed for rng of init_y.
        return_x_history (bool, default=False): True to return history of x additionally.
    
    Return: final_state (1-D array of float)
    """
    
    if h is None:
        j = J
    else:
        j = np.zeros((J.shape[0]+1, J.shape[1]+1))
        j[:-1, :-1] = J
        j[:-1, -1] = 0.5*h
        j[-1, :-1] = 0.5*h.T
    
    x = np.zeros(j.shape[0])

    if init_y is None:
        np.random.seed(sd)
        y = np.random.uniform(-0.1, 0.1, j.shape[0])
    else:
        y = init_y.copy()
    
    if return_x_history:
        x_history = []
    
    for a in PS:
        # PS = [a0*i/(steps-1) for i in range(steps)]
        y -= ((1 - a) * x + 2 * c0 * j.dot(np.sign(x))) * dt
        x += y * dt
        for i in range(j.shape[0]): # parallelizable
            if np.abs(x[i]) > 1:
                x[i] = np.sign(x[i])
                y[i] = 0
        
        if return_x_history:
            x_history.append(x.copy()) # for analysis purposes

    if return_x_history:
        if h is None:
            return np.sign(x), x_history
        else:
            return np.sign(x[:-1]) * np.sign(x[-1]), x_history
    
    if h is None:
        return np.sign(x)
    else:
        return np.sign(x[:-1]) * np.sign(x[-1])


# %%
def main():
    """
    A simple showcase
    """
    import time

    sd = 7

    num_par = [80, 68, 32, 15, 5]
    N = len(num_par)

    J = np.outer(num_par, num_par)
    offset = sum(np.diag(J))
    np.fill_diagonal(J, 0)
    h = np.zeros(N)

    norm_coef = np.sqrt(J.shape[0] / (np.sum(J**2) + 0.5 * np.sum(h**2))) # normalization
    c0 = 0.5 * norm_coef
    n = 1000
    dt = 200/n
    PS = [i/n for i in range(n)]

    # print(f"problem: {J}")
    # print(f"n: {n}, dt: {dt}, c0: {c0}")

    print(f'number partition: {num_par}')
    print("simulated bifurcation")

    # x_history_a = []
    start_time = time.time()
    ans = one_aSB_run(J, PS, dt, c0, sd=sd)
    total_time = time.time() - start_time
    print(f'aSB ground state: {ans}; time: {total_time} s')

    # x_history_a = np.asarray(x_history_a)
    # plt.figure(dpi=100)
    # plt.scatter(x_history_a[:, 0], x_history_a[:, 1], s=.1)


    # x_history_b = []
    start_time = time.time()
    ans = one_bSB_run(J, PS, dt, c0, sd=sd)
    total_time = time.time() - start_time
    print(f'bSB ground state: {ans}; time: {total_time} s')

    # x_history_b = np.asarray(x_history_b)
    # plt.figure(dpi=100)
    # plt.scatter(x_history_b[:, 0], x_history_b[:, 1], s=.1)


    # x_history_d = []
    start_time = time.time()
    ans = one_dSB_run(J, PS, dt, c0, sd=sd)
    total_time = time.time() - start_time
    print(f'dSB ground state: {ans}; time: {total_time} s')

    # x_history_d = np.asarray(x_history_d)
    # plt.figure(dpi=100)
    # plt.scatter(x_history_d[:, 0], x_history_d[:, 1], s=.1)


# %%
if __name__ == "__main__":
    main()


# %%
