import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Define the system dynamics with three systems: S1, S2, S3
def system_dynamics(state, t, alpha, beta, gamma):
    S1, S2, S3 = state
    dS1_dt = f(S1) + alpha * g(S2, S1) + gamma * p(S3, S1)
    dS2_dt = h(S2) + beta * k(S1, S2) + gamma * q(S3, S2)
    dS3_dt = m(S3) + beta * r(S1, S3) + alpha * s(S2, S3)
    return [dS1_dt, dS2_dt, dS3_dt]

# Internal dynamics for each system
def f(S1):
    return 0.1 * S1 - 0.05 * S1**2

def h(S2):
    return 0.2 * S2 - 0.03 * S2**2

def m(S3):
    return 0.15 * S3 - 0.04 * S3**2

# Coupling functions between systems
def g(S2, S1):
    return 0.05 * (S2 - S1) / (1 + S1**2)

def k(S1, S2):
    return -0.03 * (S1 - S2) / (1 + S2**2)

def p(S3, S1):
    return 0.02 * (S3 - S1) / (1 + S1**2)

def q(S3, S2):
    return 0.04 * (S3 - S2) / (1 + S2**2)

def r(S1, S3):
    return 0.03 * (S1 - S3) / (1 + S3**2)

def s(S2, S3):
    return -0.05 * (S2 - S3) / (1 + S3**2)

# Parameters and initial conditions
alpha = 0.5
beta = 0.3
gamma = 0.4
initial_state = [1.0, 0.5, 0.7]  # Initial values for S1, S2, S3
time = np.linspace(0, 50, 300)

# Solve the differential equations
result = odeint(system_dynamics, initial_state, time, args=(alpha, beta, gamma))

# Extract the results
S1_values, S2_values, S3_values = result[:, 0], result[:, 1], result[:, 2]

# Plot the results
plt.figure(figsize=(12, 7))
plt.plot(time, S1_values, label='System S1 (Political)', color='blue')
plt.plot(time, S2_values, label='System S2 (Legal)', color='orange')
plt.plot(time, S3_values, label='System S3 (Economic)', color='green')
plt.xlabel('Time')
plt.ylabel('State')
plt.title('Coupled System Dynamics with Three Systems')
plt.legend()
plt.grid(True)
plt.show()