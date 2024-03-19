import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import lu_factor, lu_solve
import scipy.linalg

# Task conditions
c_a = c_b = 2  # mg/m^3
Q_a = 200  # m^3/h
Q_b = 300  # m^3/h
Q_c = 150  # m^3/h
Q_d = 350  # m^3/h
W_s = 1500  # mg/h
W_g = 2500  # mg/h
E_12 = 25  # m^3/h
E_23 = 50  # m^3/h
E_34 = 50  # m^3/h
E_35 = 25  # m^3/h

# Matrix A
A = np.array([
    [-E_12, E_12, 0, 0, 0],
    [E_12, -(E_12 + E_23), E_23, 0, 0],
    [0, E_23, -(E_23 + E_35 + E_34), E_34, E_35],
    [0, 0, E_34, -(Q_c+E_34), 0],
    [0, 0, E_35, 0, -(Q_d+E_35)]
])

# Vector b
b = np.array([
    -W_s-Q_a*c_a,
    -Q_b * c_b,
    0,
    0,
    -W_g
])

# Performing LU decomposition of matrix A
lu, piv = lu_factor(A)

n = A.shape[0]
A_inv = np.eye(n)
# Processing each column of the identity matrix
for i in range(A.shape[0]):
    A_inv[:, i] = lu_solve((lu, piv), A_inv[:, i])

print("Inverse matrix A: \n", A_inv)

# Solving the system of equations Ac = b, finding vector c
c = lu_solve((lu, piv), b)

print("\n", c)
for i in range(5):
    print("The concentration value in room number", i+1, "is:", c[i])

total = c[3]
# Now calculating the percentage contribution of each source in the children's room
co_smoking = (A_inv[3][0] * W_s / total) * 100
co_grill = (A_inv[3][4] * W_g / total) * 100
co_outside = (A_inv[3][0] * Q_a * c_a / total) * 100 + (A_inv[3][1] * Q_b * c_b / total) * 100

print("\nPercentage from smokers in the children's room:", -co_smoking)
print("Percentage from the grill in the children's room:", -co_grill)
print("Percentage from the street in the children's room:", -co_outside)

fig, axs = plt.subplots(1, 3, figsize=(18, 6))
# Matrix A
cax1 = axs[0].matshow(A, cmap='viridis')
fig.colorbar(cax1, ax=axs[0])
axs[0].set_title('Matrix A')

# Inverse of A
cax2 = axs[1].matshow(A_inv, cmap='viridis')
fig.colorbar(cax2, ax=axs[1])
axs[1].set_title('Inverse of A')

# Vector b
cax3 = axs[2].matshow(b.reshape(-1, 1), cmap='viridis')
fig.colorbar(cax3, ax=axs[2])
axs[2].set_title('Vector b')

W_s = 800  # mg/h
W_g = 1200  # mg/h

b = np.array([
    -W_s-Q_a*c_a,
    -Q_b * c_b,
    0,
    0,
    -W_g
])

# Solving the system of equations with the new vector b, using the previously obtained LU decomposition
c2 = lu_solve((lu, piv), b)

print("\n\nAfter changing values:\n\n")
print(c2)
for i in range(5):
    print("The concentration value in room number", i+1, "is:", c2[i])

total = c2[3]
# Now calculating the percentage contribution of each source
co_smoking = (A_inv[3][0] * W_s / total) * 100
co_grill = (A_inv[3][4] * W_g / total) * 100
co_outside = (A_inv[3][0] * Q_a * c_a / total) * 100 + (A_inv[3][1] * Q_b * c_b / total) * 100

print("\nPercentage from smokers in the children's room:", -co_smoking)
print("Percentage from the grill in the children's room:", -co_grill)
print("Percentage from the street in the children's room:", -co_outside)

fig, axs = plt.subplots(1, 3, figsize=(18, 6))
# Matrix A
cax1 = axs[0].matshow(A, cmap='viridis')
fig.colorbar(cax1, ax=axs[0])
axs[0].set_title('Matrix A')

# Inverse of A
cax2 = axs[1].matshow(A_inv, cmap='viridis')
fig.colorbar(cax2, ax=axs[1])
axs[1].set_title('Inverse of A')

# Vector b
cax3 = axs[2].matshow(b.reshape(-1, 1), cmap='viridis')
fig.colorbar(cax3, ax=axs[2])
axs[2].set_title('Vector b')

bar_width = 0.35
rooms = np.arange(1, 6)  # Room numbers 1 through 5

plt.figure(figsize=(10, 6))

# Plotting the original and updated c values as bars
plt.bar(rooms - bar_width/2, c, width=bar_width, label='Original c Values')
plt.bar(rooms + bar_width/2, c2, width=bar_width, label='Updated c Values')

plt.title('Comparison of CO Concentration Values Before and After Input Changes')
plt.xlabel('Room Number')
plt.ylabel('CO Concentration')
plt.xticks(rooms)
plt.legend()
plt.grid(axis='y')
plt.show()