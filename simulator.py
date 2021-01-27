import numpy as np 
from body import Body
import matplotlib.pyplot as plt

# ========== Constants ==========
time_step = 0.01
n = 2
G = 6.6743 * (10**-11)

# ========== Functions ==========
def initialize(): 
    nbodies = np.empty(n,dtype=object)
    #masses = np.random.rand(n) * (10**10)
    #positions = np.random.rand(n, 3) * 2 - 1
    #velocities = np.random.rand(n, 3) * 1.0 - 0.5
    masses = np.array([10**11,10**11],dtype='float64')
    positions = np.array([[0,0,0],[1,1,0]],dtype='float64')
    velocities = np.array([[np.sqrt(masses[0]*G)/np.sqrt(4),0,0],[-np.sqrt(masses[0]*G)/np.sqrt(4),0,0]],dtype='float64')
    for i in range(n):
        nbodies[i] = Body(masses[i], positions[i], velocities[i])
    
    return nbodies

def update(nbodies, timestep):
    forces = np.zeros((nbodies.shape[0],3))
    energies = np.zeros(nbodies.shape[0])
    for i in range(nbodies.shape[0]):
        m1 = nbodies[i].mass
        p1 = nbodies[i].position
        for j in range(nbodies.shape[0]):
            if i != j:
                m2 = nbodies[j].mass
                p2 = nbodies[j].position
                
                forces[i] += (p2 - p1) * G * m1 * m2 / np.sum((p1 - p2)**2)**(3/2)
                energies[i] +=  -G * m1 * m2 / np.sqrt(np.sum((p1 - p2)**2))
                
        nbodies[i].position += (nbodies[i].velocity * timestep) + (0.5 * forces[i] * timestep**2 / m1)
        nbodies[i].velocity += forces[i] * timestep / m1
        nbodies[i].gpe = energies[i]
        nbodies[i].ke = 0.5 * nbodies[i].mass * np.sqrt(np.sum(nbodies[i].velocity ** 2))**2
        
def run_nbody(nbodies, iterations, timestep):
    """
    0: x
    1: y
    2: z
    3: GPE
    4: KE
    """
    history = np.zeros((iterations,nbodies.shape[0],5)) 
    for i in range(iterations):
        update(nbodies, timestep)
        for j in range(nbodies.shape[0]):
            history[i, j, :3] = nbodies[j].position
            history[i, j, 3] = nbodies[j].gpe
            history[i, j, 4] = nbodies[j].ke
    return history

def plot_history(history, iterations):
    cmaps = ['terrain','rainbow','ocean']
    skip=10
    for i in range(history.shape[1]):
        plt.scatter(history[:,i,0], history[:,i,1], s=1, c=np.arange(iterations),cmap=cmaps[i])
    plt.ylim(-5,5)
    plt.xlim(-5,5)
    plt.show()

def simulate(ts  = 0.01, iterations = 1000):
    global time_step
    time_step = ts
    global i
    i = iterations
    nbodies = initialize()
    history = run_nbody(nbodies, i, time_step)
    # plot_history(history, i)
    print('Simulated!')
    return history
    