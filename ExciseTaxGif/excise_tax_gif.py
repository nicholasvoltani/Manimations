from manim import *
import numpy as np

MAX_EXCISE_TAX = 30

# Demand function intercept
MAX_PRICE = 60

# (ABS) Derivative of demand PRICE function wrt Q
DPDQ = 1

# Demand price function in terms of Q is
# p(Q) = MAX_PRICE - DPDQ * Q

# Demand function in terms of p is 
# Q(p) = MAX_PRICE/DPDQ - p/DPDQ

# Defining functions P(q) in terms of QUANTITY, NOT PRICE P,
# due to this stupid convention not helping to plot
def demand_function_P(q):
    return max(MAX_PRICE - DPDQ*q, 0)


def demand_function_Q(p):
    return max((MAX_PRICE - p) / DPDQ, 0)


def supply_function_P(q):
    return q


def supply_function_Q(p):
    return p


# Supply-Demand Equilibrium (without taxes)
EQUILIBRIUM_PRICE = MAX_PRICE / (DPDQ + 1)

EQUILIBRIUM_DEMAND = MAX_PRICE / (DPDQ + 1)


# Supply-Demand Equilibrium post excise tax
def equilibrium_price_post_tax(tax):
    return (MAX_PRICE + DPDQ*tax) / (1 + DPDQ)

def equilibrium_demand_post_tax(tax):
    return DPDQ* (MAX_PRICE - tax) / (1 + DPDQ)


# Calculating what would be the price with new demand but without tax
def would_be_demand(tax):
    return supply_function_Q(equilibrium_price_post_tax(tax))

def would_be_price(tax):
    return supply_function_P(equilibrium_demand_post_tax(tax))


class excise_tax_gif(Scene):
    def construct(self):
        a = Axes(x_range=[0, 80, 10],
                 y_range=[0, 80, 10])

        # Supply and demand curves
        demand_curve = a.plot(lambda q: demand_function_P(q), 
                              color=BLUE)

        supply_curve = a.plot(lambda q: supply_function_P(q),
                              color=GREEN)

        # Equilibrium price (plotted with dashed lines)
        equilibrium_price = a.plot(lambda q: EQUILIBRIUM_PRICE,
                                   [0, EQUILIBRIUM_PRICE], 
                                   color=WHITE)
        equilibrium_price = DashedLine(start=a.c2p(0, EQUILIBRIUM_PRICE),
                                       end=a.c2p(EQUILIBRIUM_DEMAND, EQUILIBRIUM_PRICE))

        # Equilibrium Quantity (plotted with dashed lines)
        equilibrium_q = DashedLine(start=a.c2p(EQUILIBRIUM_DEMAND, 0),
                                   end=a.c2p(EQUILIBRIUM_DEMAND, EQUILIBRIUM_PRICE))

        # Join equilibrium info into single VGroup
        equilibrium_point = VGroup(equilibrium_q, equilibrium_price)

        # Adding Excise Tax as a moving variable
        excise_tax = ValueTracker(0)

        # New Equilibrium points post tax
        shifted_supply_curve = always_redraw(
            lambda: a.plot(lambda q: excise_tax.get_value() + supply_function_P(q),
                           color=RED)
                           )
        
        new_price = always_redraw(lambda: DashedLine(color=RED,
                                                     start=a.c2p(0, 
                                                                 equilibrium_price_post_tax(excise_tax.get_value())
                                                                 ),
                                                     end=a.c2p(equilibrium_demand_post_tax(excise_tax.get_value()), 
                                                               equilibrium_price_post_tax(excise_tax.get_value())
                                                               )
                                                    )
                                )

        new_quantity = always_redraw(lambda: DashedLine(color=RED,
                                                     start=a.c2p(equilibrium_demand_post_tax(excise_tax.get_value()), 
                                                                 0
                                                                 ),
                                                     end=a.c2p(equilibrium_demand_post_tax(excise_tax.get_value()), 
                                                               equilibrium_price_post_tax(excise_tax.get_value())
                                                               )
                                                    )
                                )

        # Join new equilibrium info into single VGroup
        equilibrium_point_post_tax = VGroup(new_quantity, new_price)

        # Plotting "would-be price" for new demand but old (pre-tax) prices
        would_be_price_plot = always_redraw(lambda: DashedLine(color=GREEN,
                                                     start=a.c2p(0, 
                                                                 would_be_price(excise_tax.get_value())
                                                                 ),
                                                     end=a.c2p(equilibrium_demand_post_tax(excise_tax.get_value()), 
                                                               would_be_price(excise_tax.get_value())
                                                               )
                                                    )
                                )

        # Surpluses
        consumer_surplus = always_redraw(lambda: a.get_area(graph=demand_curve,
                                                       x_range=[0, equilibrium_demand_post_tax(excise_tax.get_value())],
                                                       color=RED,
                                                       opacity=0.5,
                                                       bounded_graph=a.plot(lambda p: equilibrium_price_post_tax(excise_tax.get_value())))
                                        )
        
        producer_surplus = always_redraw(lambda: a.get_area(graph=a.plot(lambda p: would_be_price(excise_tax.get_value())),
                                                       x_range=[0, equilibrium_demand_post_tax(excise_tax.get_value())],
                                                       color=GREEN,
                                                       opacity=0.5,
                                                       bounded_graph=supply_curve
                                                       ) 
                                        )
        
        government_surplus = always_redraw(lambda: a.get_area(graph=a.plot(lambda p: equilibrium_price_post_tax(excise_tax.get_value())),
                                                       x_range=[0, equilibrium_demand_post_tax(excise_tax.get_value())],
                                                       color=WHITE,
                                                       opacity=0.5,
                                                       bounded_graph=a.plot(lambda p: would_be_price(excise_tax.get_value())))
                                           )
        
        # Plotting Deadweight Loss
        deadweight_loss = always_redraw(lambda: a.get_area(graph=demand_curve,
                                                       x_range=[equilibrium_demand_post_tax(excise_tax.get_value()), EQUILIBRIUM_DEMAND],
                                                       color=GREY_BROWN,
                                                       opacity=0.5,
                                                       bounded_graph=supply_curve)
                                           )

        # Plotting it all
        self.add(a, 
                 demand_curve, 
                 supply_curve,
                 equilibrium_point,
                 shifted_supply_curve,
                 equilibrium_point_post_tax,
                 would_be_price_plot,
                 consumer_surplus,
                 producer_surplus,
                 government_surplus,
                 deadweight_loss
                 )

        self.play(excise_tax.animate.set_value(MAX_EXCISE_TAX), 
                  run_time=5)