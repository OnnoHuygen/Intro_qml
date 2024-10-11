import numpy as np
from spinstates import *

## In this exercise, we will work with spin-1/2 particles as a representation of qubits.
## Up and down states in the z-direction:
up = np.array([[1.], [0.]])
down = np.array([[0.], [1.]])

## Measurement operators in the x, y, and z directions:
sigma_z = np.array([[1., 0], [0., -1.]])
sigma_x = np.array([[0, 1], [1, 0]])
sigma_y = np.array([[0, 0-1j], [0+1j, 0]])


## --------------- Superposition ---------------
# Since the state 'down' is not in a superposition in the z-direction, that means the observable 'Spin in the z-direction' has a definite value. So, for the observable 'spin in the z-direction', a particle in the up state is not in a superposition.

# 1. What is the spin in the z-direction of a particle in the down state? and what is the spin value in the z-direction for a particle in the up state?
spin_z = up.T @ sigma_z @ up

## 2. What is the expectation value of 'spin in the x-direction' of a particle in the up-state? And what is the expectation value of 'spin in the x-direction' of a particle in the down state?
spin_x_down = down.T @ sigma_x @ down
spin_x_up = up.T @ sigma_x @ up

## We will now simulate doing a single spin measurement in the x-direction of a particle in the up state. First, we can check what the possible outcomes of a measurement in the x-direction are.
(eigvals, eigvecs) = np.linalg.eig(sigma_x)
possible_outcomes = eigvals
## As you can see, the possible outcomes are 1 and -1, which is the same as the spin in the z-direction. This better be the case, as there is no inherent asymmetry in the universe that prefers the z-direction we defined over any other direction.


## 3. Create a state that is an equal superposition of an up particle and a down particle by making a linear combination of (1/sqrt(2)) up and adding (1/sqrt(2)) down.
created_state = (1/np.sqrt(2))*up + (1/np.sqrt(2))*down

## 4. Do you have an idea what the probability is that we measure 1, or 'up', in the z-direction if we do a measurement on this state?
## The state we created is a linear combination of both the up and down states in the z-direction. Using Born's rule of probability, we know that we have a (1/2) probability of measuring 1, or 'up', and a (1/2) probability of measuring -1, or 'down'.

## Below, there is some code to simulate doing measurements of the observable 'operator' on some state.
def measure(state, operator, n_times=10):
    (eigvals, eigvecs) = np.linalg.eig(operator)
    n = operator.shape[0]
    probs = np.array([(eigvecs[:,i].reshape(n,1).T @ state)[0][0] * (state.T @ eigvecs[:,i].reshape(n,1))[0][0] for i in range(n)])
    return eigvals[np.random.choice(range(n), p=probs, size=n_times)]

## 4. Do 1000 measurements in the z-direction on the state you just created. How many times did you get the outcome 1? And how many times did you get the outcome -1?
outcomes = measure(created_state, sigma_z, n_times=1000)
nr_up = len([i for i in outcomes if i == 1])

## 5. It is possible to calculate the probability of measuring 'up', or 1, in this state directly from Born's rule of probability.
## Compute the probability to measure 'up' and 'down' when measuring in the z-direction on your created state.
prob_up = np.float(np.real(np.conj(up.T) @ created_state * np.conj(created_state.T) @ up))
prob_down = np.float(np.real(np.conj(down.T) @ created_state * np.conj(created_state.T) @ down))
## The state is indeed in a superposition in the z-direction.

## 6. Now do 1000 measurements in the x-direction on the state you created. How many times did you get the outcome 1? And how many times did you get the outcome -1?
outcomes_x = measure(created_state, sigma_x, n_times=1000)
nr_up = len([i for i in outcomes_x if i == 1])
## All measurements return a 1. This means it is very likely that the created state is actually a spin state in the x-direction. So in this direction, it is not in superposition.

## Import the package spinstates without reading the contents.
from spinstates import *
## In this script, we defined some state called 'mystery_state'.
## 7. Using the code from above, perform 1000 measurements in the z-direction of this state. Using the results, make a guess of what the state might have been. You do not have enough information to get the exact state, but you can get the absolute values of the linear combination exact.
outcomes_mystery = measure(mystery_state, sigma_z, n_times=1000)
nr_up = len([i for i in outcomes_mystery if i == 1])
guess = np.sqrt(nr_up/1000)*up + (np.sqrt((1000 - nr_up)/1000)) * down

## 8. Now you may look at the mystery state. Did you get a good estimate?

## ------------------- Entanglement ---------------------------
## Let's build a two-particle state. Previously, we worked in a two-dimensional vector space: we were dealing with a single spin-1/2 particle, and a spin measurement on that particle can yield only up or down.
## Now we are working with two spin-1/2 particles. A spin measurement on both particles can now yield four different outcomes (up-up, up-down, down-up, and down-down). Thus, it might be no surprise that we should now be working in a four-dimensional vector space.
## We can construct states of two particles by taking a kronecker product. You do not need to know how this works in detail.
up_up = np.kron(up, up)
up_down = np.kron(up, down)
down_up = np.kron(down, up)
down_down = np.kron(down, down)

## 1. Consider the up_up state.
sate_1 = up_up
## Is this an entangled state? Why (not)?
## The up-up state is not an entangled state: either particle is always in the up-state regardless of what we measure on the other particle.

## 2. Consider the state:
state_2 = (1/np.sqrt(2))*up_up + (1/np.sqrt(2))*down_down
## Is this an entangled state? Why (not)?
## Yes, this is an entangled state. Suppose we perform a measurement on the first particle, and see that it is in the 'down' state. From Born's rule, we see that the only option must have been that the system collapsed to the down_down position, as the down_up position has a coefficient of 0 in the state. Therefore, if we measure the state of the first particle, we also know the state of the second particle.

## 3. What do you think the entanglement entropy of both states above are?
## In words: The first state is not entangled, and has an entropy of zero. For the second state, if we perform a measurement on either particle, we know the state of the other particle with certainty. Before a measurement, we always had a 50/50 to get up or down on either particle. So after measuring one particle, we have gained exactly one bit of information on the other particle.
