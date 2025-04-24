import os
# Using Manim Community!!! (v 0.18.0)
from manim import *
from math import pow, inf
import matplotlib.pyplot as plt
import numpy as np

def CES_Function(x1, x2, alpha, substitution_parameter):
    first_term = alpha*(pow(x1, substitution_parameter))
    second_term = (1-alpha)*(pow(x2, substitution_parameter))
    return pow(first_term + second_term, 1/substitution_parameter)


def ConstantUtility_CES_Y(x1, alpha, substitution_parameter, utility_level):
    numerator = np.pow(utility_level, substitution_parameter)
    numerator = numerator - alpha * np.pow(x1, substitution_parameter)
    numerator = numerator / (1-alpha)

    # `numerator` may be negative => exponentiation may yield complex number
    numerator = numerator**(1/substitution_parameter)
    numerator = numerator.real

    return numerator


def CobbDouglas_Function_Y(x1, alpha, utility_level):
    return (utility_level * x1**(-alpha))**(1/(1-alpha))



ALPHA = 0.5
INITIAL_SUBSTITUTION_PARAMETER = -1.0
UTILITY_LEVEL = 3

x = np.arange(0.5, 6, 0.05)
# for element in x:
#     print(ConstantUtility_CES_Y(element, ALPHA, -2.0, UTILITY_LEVEL))

# ces = ConstantUtility_CES_Y(x, ALPHA, INITIAL_SUBSTITUTION_PARAMETER, UTILITY_LEVEL)
cd = CobbDouglas_Function_Y(x, ALPHA, UTILITY_LEVEL)

plt.plot(x, [ConstantUtility_CES_Y(el, ALPHA, 1, UTILITY_LEVEL) for el in x])
# plt.plot(x, [ConstantUtility_CES_Y(el, ALPHA, -0.5, UTILITY_LEVEL) for el in x])
# plt.plot(x, [ConstantUtility_CES_Y(el, ALPHA, -1.0, UTILITY_LEVEL) for el in x])
# plt.plot(x, [ConstantUtility_CES_Y(el, ALPHA, -5.0, UTILITY_LEVEL) for el in x])
# plt.plot(x, [ConstantUtility_CES_Y(el, ALPHA, -50.0, UTILITY_LEVEL) for el in x])
plt.plot(x, ConstantUtility_CES_Y(x, ALPHA, 0.5, UTILITY_LEVEL))
plt.plot(x, ConstantUtility_CES_Y(x, ALPHA, 0.25, UTILITY_LEVEL))
plt.plot(x, ConstantUtility_CES_Y(x, ALPHA, 0.10, UTILITY_LEVEL))
plt.plot(x, ConstantUtility_CES_Y(x, ALPHA, 0.05, UTILITY_LEVEL))
plt.plot(x, cd, 'k')
# plt.plot(x, ConstantUtility_CES_Y(x, ALPHA, -0.25, UTILITY_LEVEL))
# plt.plot(x, ConstantUtility_CES_Y(x, ALPHA, -0.5, UTILITY_LEVEL))
# plt.plot(x, ConstantUtility_CES_Y(x, ALPHA, -1, UTILITY_LEVEL))
plt.legend([
    # "$\\rho = 1$", 
    # "$\\rho = -0.5$",
    # "$\\rho = -1.0$",
    # "$\\rho = -5.0$",
    # "$\\rho = -50.0$",  
    "$\\rho = 0.5$", 
    "$\\rho = 0.25$", 
    "$\\rho = 0.10$", 
    "$\\rho = 0.05$", 
    "Cobb-Douglas",
    # "$\\rho = -0.25$", 
    # "$\\rho = -0.5$", 
    # "\\rho = -1.0",
    ])
plt.show()
