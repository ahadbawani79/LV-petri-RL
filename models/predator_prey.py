from core.petri_net import PetriNet, Place, Transition, Arc


# =========================================
# Create Predator-Prey Model
# =========================================

def create_predator_prey_model():

    model = PetriNet(
        name="Predator Prey Model",
        model_type="SPN"
    )

    # =====================================
    # Places
    # =====================================

    model.add_place(
        Place("p1", "Prey", 150, "prey")
    )

    model.add_place(
        Place("p2", "Predators", 50, "predators")
    )

    # =====================================
    # Transitions
    # =====================================

    model.add_transition(
        Transition(
            "t1",
            "Prey Reproduction",
            rate="0.5 * prey"
        )
    )

    model.add_transition(
        Transition(
            "t2",
            "Predator Hunting",
            rate="0.002 * predators * prey",
            guard="prey > 10 and predators > 0"
        )
    )

    model.add_transition(
        Transition(
            "t3",
            "Predator Death",
            rate="0.3 * predators"
        )
    )

    # =====================================
    # Prey Reproduction Arcs
    # =====================================

    model.add_arc(
        Arc("p1", "t1", weight=1)
    )

    model.add_arc(
        Arc("t1", "p1", weight=2)
    )

    # =====================================
    # Predator Hunting Arcs
    # =====================================

    model.add_arc(
        Arc("p1", "t2", weight=1)
    )

    model.add_arc(
        Arc("p2", "t2", weight=1)
    )

    model.add_arc(
        Arc("t2", "p2", weight=2)
    )

    # =====================================
    # Predator Death Arcs
    # =====================================

    model.add_arc(
        Arc("p2", "t3", weight=1)
    )

    return model