import os
# Using Manim Community!!! (v 0.18.0)
from manim import *
from math import pow
import matplotlib.pyplot as plt
import numpy as np

def CES_Function(x1, x2, alpha, substitution_parameter):
    first_term = alpha*(pow(x1, substitution_parameter))
    second_term = (1-alpha)*(pow(x2, substitution_parameter))
    return pow(first_term + second_term, 1/substitution_parameter)


def ConstantUtility_CES_Y(x1, alpha, substitution_parameter, utility_level):
    numerator = pow(utility_level, substitution_parameter)
    numerator = numerator - alpha * pow(x1, substitution_parameter)
    numerator = numerator / (1-alpha)
    numerator = pow(numerator, 1/substitution_parameter)

    return numerator


def CobbDouglas_Function_Y(x1, alpha, utility_level):
    return (utility_level * x1**(-alpha))**(1/(1-alpha))


ALPHA = 0.5
INITIAL_SUBSTITUTION_PARAMETER = 1
UTILITY_LEVEL = 3

class ConstantElasticityOfSubstitution_Leontief(Scene):
    def construct(self):
        # Basic things
        substitution_parameter = ValueTracker(INITIAL_SUBSTITUTION_PARAMETER)
        axes = Axes(x_range=[0.5, 5],
                    y_range=[0.5, 20])

        # Showing updated values of CES parameter
        def latex_label():
            value = substitution_parameter.get_value()
            return MathTex(r"\rho = ", f"{value:.2f}").to_corner(UR)

        value_shown = always_redraw(latex_label)

        # # Debugging: Values of CES and CD
        x1_fixed = 2
        fixed_label = (MathTex(r"\text{Dado }",
                               f"x_1 = {x1_fixed}",
                               r"\text{ fixo:}")
                       .next_to(value_shown, DOWN, aligned_edge=RIGHT)
                       )
        underline = Underline(fixed_label)

        # Show CES function output at a fixed point
        ces_value_label = always_redraw(lambda: MathTex(
            f"CES(x_1={x1_fixed}) = {ConstantUtility_CES_Y(x1_fixed, ALPHA, substitution_parameter.get_value(), UTILITY_LEVEL):.2f}")
            .next_to(fixed_label, DOWN, aligned_edge=RIGHT)
        )

        # ces_label_static = MathTex(r"CES(x_1 = 3) = ")

        # ces_value_dynamic = DecimalNumber(
        #     ConstantUtility_CES_Y(x1_fixed, ALPHA, substitution_parameter.get_value(), UTILITY_LEVEL),
        #     num_decimal_places=2,
        #     include_sign=False
        # )

        # # Position the value next to the static label
        # ces_value_dynamic.next_to(ces_label_static, RIGHT)

        # # Group them together
        # ces_value_label_group = (VGroup(ces_label_static, ces_value_dynamic)
        #                         .next_to(fixed_label, DOWN, aligned_edge=RIGHT)
        #                         )

        # # Add updater to ces_value_dynamic
        # ces_value_dynamic.add_updater(
        #     lambda m: m.set_value(
        #         ConstantUtility_CES_Y(x1_fixed, 
        #                             ALPHA, 
        #                             substitution_parameter.get_value(), 
        #                             UTILITY_LEVEL)
        # ))

        # Show Cobb-Douglas output at x1 = 2
        cd_value_label = always_redraw(lambda: MathTex(
            f"CD(x_1={x1_fixed}) = ",
            f"{CobbDouglas_Function_Y(x1_fixed, ALPHA, UTILITY_LEVEL):.2f}"
        ).next_to(ces_value_label, DOWN, aligned_edge=RIGHT))

        
        CES_indifference_curve_plot = always_redraw(
            lambda: axes.plot(lambda x1: ConstantUtility_CES_Y(x1, 
                                                              ALPHA, 
                                                              substitution_parameter.get_value(), 
                                                              UTILITY_LEVEL),
            color=GREEN,
            use_smoothing=False)
        )
        
        CobbDouglas_plot = axes.plot(lambda x1: CobbDouglas_Function_Y(x1,
                                                                       ALPHA,
                                                                       UTILITY_LEVEL),
                                    color=GREEN.lighter())
        
        CobbDouglas_plot = DashedVMobject(CobbDouglas_plot,
                                          dashed_ratio=0.8)

        self.add(axes,
                 CES_indifference_curve_plot,
                 value_shown,
                 CobbDouglas_plot,
                 fixed_label,
                 underline,
                 ces_value_label,
                #  ces_value_label_group,
                 cd_value_label
                 )

        # On rate_funcs: https://www.reddit.com/r/manim/comments/gzmnrp/manim_tip_rate_functions_when_playing_animation/?show=original        
        self.play(substitution_parameter.animate.set_value(-1.0),
                  run_time=2,
                  rate_func=rate_functions.smooth)