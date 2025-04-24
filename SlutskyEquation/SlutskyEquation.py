import os
# Using Manim Community!!! (v 0.18.0)
from manim import *
from math import sqrt
import matplotlib.pyplot as plt
import numpy as np


def CobbDouglasUtility(x, y, alpha):
    return x**alpha * y**(1-alpha)


def IndifferenceCurve_Y(x, alpha, utility_level):
    '''
    Inverting utility wrt y.
    '''
    return (utility_level/x**alpha)**(1/(1-alpha))


def BudgetLine(x, price_x, price_y, income):
    '''
    Gives budget constraint of optimization problem for utility.

    x*px + y*py = income
    <=> y = income/py - (px/py)*x 
    '''
    return income/price_y - (price_x/price_y) * x


def WalrasianDemand_X(price_x, income, alpha):
    '''
    Optimal demand of X, given budget constraint.
    '''

    return alpha * income / price_x


def WalrasianDemand_Y(price_y, income, alpha):
    '''
    Optimal demand of Y, given budget constraint.
    '''

    return (1-alpha) * income / price_y


def IndirectUtility(price_x, price_y, income, alpha):
    '''
    (Maximal) utility achieved at Walrasian demand.

    Is algebraically equal to:
    (alpha / price_x)**alpha * ((1-alpha) / price_y)**(1-alpha) * income
    '''
    return CobbDouglasUtility(WalrasianDemand_X(price_x, income, alpha),
                              WalrasianDemand_Y(price_y, income, alpha),
                              alpha
                              )


def HicksianDemand_X(price_x, price_y, utility, alpha):
    '''
    Compensated demand for X, such as to guarantee given some utility.
    '''
    return utility * ((alpha * price_y) / ((1-alpha) * price_x))**(1-alpha)


def TotalSlutskyEffect_X(price_x, income, alpha):
    '''
    Derivative of Walrasian demand (of x) wrt price.

    Is what's empirically observed.
    '''  
    return -alpha * income / (price_x)**2


def IncomeEffect_X(price_x, income, alpha):
    '''
    Walrasian demand (of x) times derivative of Walrasian demand (of x) wrt income.
    '''
    return (alpha/price_x)**2 * income


def SubstitutionEffect_X(price_x, income, alpha):
    '''
    Partial derivative of Hicksian demand (of x) wrt price (of x). 

    Not empirically observable.
    '''
    return alpha*(alpha-1) * income / (price_x)**2


INITIAL_PRICE_X = 5 / 10
INITIAL_PRICE_Y = 2 / 10
INITIAL_INCOME = 50 / 10
ALPHA = 0.65
ORIGINAL_WALRASIAN_X = WalrasianDemand_X(INITIAL_PRICE_X, INITIAL_INCOME, ALPHA)
ORIGINAL_WALRASIAN_Y = WalrasianDemand_Y(INITIAL_PRICE_Y, INITIAL_INCOME, ALPHA)

class SlutskyEquation_SingleVariable(Scene):
    def construct(self):
        # Variables: prices
        price_x = ValueTracker(INITIAL_PRICE_X)
        price_y = INITIAL_PRICE_Y
        
        # (Necessary) Income will change alongside prices
        income = INITIAL_INCOME

        # Walrasian demands
        x_star = WalrasianDemand_X(price_x.get_value(), income, ALPHA)
        y_star = WalrasianDemand_Y(price_y, income, ALPHA)

        # Achieved utility levels
        # utility = IndirectUtility(price_x.get_value(), price_y, income, ALPHA)
        
        # Create axes
        axes = Axes(x_range=[0.5*income/price_x.get_value(), 
                             income/price_x.get_value()], 
                    y_range=[0.5, income/price_y])

        # Original information
        original_budget_line = axes.plot(
            lambda x: BudgetLine(x,
                                 INITIAL_PRICE_X,
                                 INITIAL_PRICE_Y,
                                 INITIAL_INCOME),
            color=RED.lighter())
        
        original_budget_line = DashedVMobject(original_budget_line,
                                              dashed_ratio=0.8)
        

        original_indifference_curve = axes.plot(
            lambda x: IndifferenceCurve_Y(x,
                                          ALPHA,
                                          IndirectUtility(INITIAL_PRICE_X, INITIAL_PRICE_Y, INITIAL_INCOME, ALPHA)),
            color=GREEN.lighter())
        
        original_indifference_curve = DashedVMobject(original_indifference_curve,
                                                     dashed_ratio=0.8)

        
        original_walrasian_demand = always_redraw(
            lambda: Dot().move_to(
                axes.c2p(ORIGINAL_WALRASIAN_X,
                         ORIGINAL_WALRASIAN_Y)
            )
        )

        # Plotting Budget Constraint and Indifference Curve
        budget_line = always_redraw(
            lambda: axes.plot(lambda x: BudgetLine(x,
                                                   price_x.get_value(),
                                                   price_y,
                                                   income),
                              color=RED)
        )
        
        indifference_curve = always_redraw(
            lambda: axes.plot(lambda x: IndifferenceCurve_Y(x,
                                                            ALPHA,
                                                            IndirectUtility(price_x.get_value(), price_y, income, ALPHA)),
                             color=GREEN)
        )

        walrasian_demand = always_redraw(
            lambda: Dot().move_to(
                axes.c2p(WalrasianDemand_X(price_x.get_value(), income, ALPHA),
                         WalrasianDemand_Y(price_y, income, ALPHA))
            )
        )

        # Calculating Slutsky effects
        total_effect = TotalSlutskyEffect_X(price_x.get_value(),
                                            income,
                                            ALPHA)
        
        shifted_demand = always_redraw(
            lambda: Dot().move_to(
                axes.c2p(ORIGINAL_WALRASIAN_X + total_effect*(price_x.get_value() - INITIAL_PRICE_X),
                         ORIGINAL_WALRASIAN_Y*0.7)
            )
        )

        income_effect = IncomeEffect_X(price_x.get_value(),
                                       income,
                                       ALPHA)

        substitution_effect = SubstitutionEffect_X(price_x.get_value(),
                                                   income,
                                                   ALPHA)

        # Plotting it all
        self.add(axes, 
                 original_budget_line,
                 original_indifference_curve,
                 original_walrasian_demand,
                 budget_line,
                 indifference_curve,
                 walrasian_demand,
                 shifted_demand
                 )

        self.play(price_x.animate.set_value(INITIAL_PRICE_X+0.05),
                  run_time=2)