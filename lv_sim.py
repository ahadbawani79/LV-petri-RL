
import random

import matplotlib.pyplot as plt
import snakes.plugins
import snakes_spn.plugin as spn_plugin

from snakes.nets import *

snakes.plugins.load(
    [spn_plugin, "gv"],
    "snakes.nets",
    "snk",
)

from snk import (
    PetriNet,
    Place,
    Transition,
    Expression,
    Variable,
)

from spn_tools.run_simulation import run_simulation


class LV_SIM:

    def __init__(self, x0=(50, 150, 10)):

        self.x0 = x0        

        self.expression_functions = {            
            "hunt_rate": lambda x, y: 0.002 * x * y,
            "predator_death_rate": lambda y: 0.3 * y,
            "prey_birth_rate": lambda x: 0.5 * x,
            
            "superpredator_hunts_predator_rate": (
                lambda y, z: 0.001 * y * z
            ),
            
            "superpredator_hunts_prey_rate": (
                lambda x, z: 0.0005 * x * z
            ),
            
            "superpredator_death_rate": lambda z: 0.2 * z,
        }

        self.lv_cpn = PetriNet("Hunt and Prey Theory with Superpredator")

        self.lv_cpn.add_place(Place("Predator", x0[0]))
        self.lv_cpn.add_place(Place("Prey", x0[1]))
        self.lv_cpn.add_place(Place("Superpredator", x0[2]))

        # Predators hunts prey
        rate = Expression("abs(hunt_rate(x, y))")
        rate.globals["hunt_rate"] = (
            self.expression_functions["hunt_rate"]
        )

        transition = Transition(
            "Predator hunts prey",
            rate_function=rate,
        )
        self.lv_cpn.add_transition(transition)

        self.lv_cpn.add_input(
            "Predator", transition.name, Variable("y")
        )
        self.lv_cpn.add_input(
            "Prey", transition.name, Variable("x")
        )

        self.lv_cpn.add_output(
            "Predator", transition.name, Expression("y + 1")
        )
        self.lv_cpn.add_output(
            "Prey", transition.name, Expression("x - 1")
        )
        
        # Predator dies
        rate = Expression("abs(predator_death_rate(y))")
        rate.globals["predator_death_rate"] = (
            self.expression_functions["predator_death_rate"]
        )

        transition = Transition(
            "Predator dies",
            rate_function=rate,
        )
        self.lv_cpn.add_transition(transition)

        self.lv_cpn.add_input(
            "Predator", transition.name, Variable("y")
        )
        self.lv_cpn.add_output(
            "Predator", transition.name, Expression("y - 1")
        )
        
        
        # Prey reproduces
        rate = Expression("abs(prey_birth_rate(x))")
        rate.globals["prey_birth_rate"] = (
            self.expression_functions["prey_birth_rate"]
        )

        transition = Transition(
            "Prey born",
            rate_function=rate,
        )
        self.lv_cpn.add_transition(transition)

        self.lv_cpn.add_input(
            "Prey", transition.name, Variable("x")
        )
        self.lv_cpn.add_output(
            "Prey", transition.name, Expression("x + 1")
        )
        
        # Superpredator hunts Predator
        rate = Expression(
            "abs(superpredator_hunts_predator_rate(y, z))"
        )
        rate.globals["superpredator_hunts_predator_rate"] = (
            self.expression_functions[
                "superpredator_hunts_predator_rate"
            ]
        )

        transition = Transition(
            "Superpredator hunts Predator",
            rate_function=rate,
        )
        self.lv_cpn.add_transition(transition)

        self.lv_cpn.add_input(
            "Predator", transition.name, Variable("y")
        )
        self.lv_cpn.add_input(
            "Superpredator", transition.name, Variable("z")
        )

        self.lv_cpn.add_output(
            "Predator", transition.name, Expression("y - 1")
        )
        self.lv_cpn.add_output(
            "Superpredator", transition.name, Expression("z + 1")
        )
        
        # Superpredator hunts Prey
        rate = Expression(
            "abs(superpredator_hunts_prey_rate(x, z))"
        )
        rate.globals["superpredator_hunts_prey_rate"] = (
            self.expression_functions[
                "superpredator_hunts_prey_rate"
            ]
        )

        transition = Transition(
            "Superpredator hunts Prey",
            rate_function=rate,
        )
        self.lv_cpn.add_transition(transition)

        self.lv_cpn.add_input(
            "Prey", transition.name, Variable("x")
        )
        self.lv_cpn.add_input(
            "Superpredator", transition.name, Variable("z")
        )

        self.lv_cpn.add_output(
            "Prey", transition.name, Expression("x - 1")
        )
        self.lv_cpn.add_output(
            "Superpredator", transition.name, Expression("z + 1")
        )
        
        # Superpredator dies
        rate = Expression("abs(superpredator_death_rate(z))")
        rate.globals["superpredator_death_rate"] = (
            self.expression_functions["superpredator_death_rate"]
        )

        transition = Transition(
            "Superpredator dies",
            rate_function=rate,
        )
        self.lv_cpn.add_transition(transition)

        self.lv_cpn.add_input(
            "Superpredator", transition.name, Variable("z")
        )
        self.lv_cpn.add_output(
            "Superpredator", transition.name, Expression("z - 1")
        )
        

    def run_sim(
        self,
        max_time=300,
        max_steps=10000,
        seed=42,
        plot=False,
    ):

        random.seed(seed)
        
        sim = run_simulation(
            self.lv_cpn,
            max_steps=max_steps,
            max_time=max_time,
        )

        print("Simulation completed.")
        print("Available simulation data:", sim.keys())

        if plot:

            plt.figure(figsize=(12, 7))

            plt.plot(
                sim["time"],
                sim["Predator"],
                label="Predator",
            )

            plt.plot(
                sim["time"],
                sim["Prey"],
                label="Prey",
            )

            plt.plot(
                sim["time"],
                sim["Superpredator"],
                label="Superpredator",
            )

            plt.xlabel("Time")
            plt.ylabel("Population")

            plt.title(
                "Hunt and Prey Theory with Superpredator"
            )

            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()

            plt.savefig(
                "superpredator_simulation.png",
                dpi=300,
                bbox_inches="tight",
            )

            print(
                "Graph saved as superpredator_simulation.png"
            )

        return (
            sim,
            ("Predator", "Prey", "Superpredator"),
            "time",
        )


if __name__ == "__main__":

    model = LV_SIM(
        x0=(50, 150, 10)
    )

    simulation, populations, time_key = model.run_sim(
        max_time=300,
        max_steps=10000,
        seed=42,
        plot=True,
    )

    plt.show()