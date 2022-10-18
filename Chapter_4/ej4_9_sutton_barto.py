# -*- coding: utf-8 -*-
"""ej4.9_sutton_barto.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NCg0ITE7ZEf0U0G5oZL2TxgL8fl-E_3G

Ejercicio 4.9 del libro Reinforcement Learning : Aplicar value iteration al gambler's proble usando p=0.25 y p=0.55
----------------------------------------------
"""

import numpy as np
import matplotlib.pyplot as plt

"""Primero definimos la función que nos devuelve todas las acciones disponibles para cada estado:"""

def get_action_space(s):
    return np.arange(1, min(s, 100-s)+1)

"""Después definimos una función para la ecuación de Bellman, con $\gamma=1$:"""

def bellman_update(s, a, r, v, p_heads, gamma):
    return p_heads * (r[s+a] + gamma*v[s+a]) + (1-p_heads) * (r[s-a] + gamma*v[s-a])

"""Y también vamos a encapsular el código que se encarga de hacer el one-step lookahead dentro de value iteration:"""

def one_step_lookahead(s, r, v, p_heads, gamma):
    v_max = -1000
    for a in get_action_space(s):
        v_a = bellman_update(s, a, r, v, p_heads, gamma)
        v_max = v_a if v_a > v_max else v_max
    return v_max

"""Añadimos la porción de código que obtiene la política óptima y ya tenemos el algoritmo completo:"""

def gambler_value_iteration(p_heads, theta=1e-30, gamma=1.0):
    # States and rewards definitions
    states = np.arange(1,100) # this looks like [1,2,...,99]
    r = np.zeros(101)
    r[100] = 1.0
    # Value function initialization with two dummy states
    v = np.zeros(101)

    # Converge to optimal values:
    finished = False
    while not finished:
        delta = 0.0
        for s in states:
            value = v[s] # dump previous v[s] on temporal variable
            v[s] = one_step_lookahead(s, r, v, p_heads, gamma)
            delta = max(delta, np.abs(value - v[s]))
        print(delta)
        finished = True if delta < theta else False

    # Obtain optimal policy:
    pi = np.zeros(100)
    for s in states:
        actions = get_action_space(s)
        pi[s] = np.argmax([bellman_update(s, a, r, v, p_heads, gamma) for a in actions])+1
    return pi, v

"""Y ahora probamos:"""

policy, v = gambler_value_iteration(0.4)

print(policy)

print(v)

# Plotting Final Policy (action stake) vs State (Capital)

# x axis values
x = range(100)
# corresponding y axis values
y = v[:100]
 
# plotting the points 
plt.plot(x, y)
 
# naming the x axis
plt.xlabel('Capital')
# naming the y axis
plt.ylabel('Value Estimates')
 
# giving a title to the graph
plt.title('Final Policy (action stake) vs State (Capital)')
 
# function to show the plot
plt.show()

# Plotting Capital vs Final Policy

# x axis values
x = range(100)
# corresponding y axis values
y = np.round(policy, 5)
 
# plotting the bars
plt.bar(x, y, align='center', alpha=0.5)
 
# naming the x axis
plt.xlabel('Capital')
# naming the y axis
plt.ylabel('Final policy (stake)')
 
# giving a title to the graph
plt.title('Capital vs Final Policy')
 
# function to show the plot
plt.show()

"""Conclusiones
------------


Es muy importante definir bien los estados y las acciones disponibles.
Comencé usando un espacio con estados entre 0 y 100 (es decir, 101), y con 
acciones que incluían no apostar nada. Ésto no convergía a la solución correcta, ya que al estar metiendo los 'dummy states' en los cálculos, entraba en un bucle. Lo que debo hacer es jugar sólo son V[s] para $s$ entre 1 y 99, y dejar V[0] y V[100] quietitos y con valor = 0. Lo mismo con los rewards: genero un vector de 101 recompensas pero en la práctica sólo uso las 99 que no están en los extremos. Otro punto importante es en la obtención de la política óptima: dado que lo estoy haciendo con vectores de acciones que defino sin tener en cuenta los estados 0 y 101, cuando hago argmax() debo volver a tenerlos en cuenta! (Por eso sumo +1.0)
"""