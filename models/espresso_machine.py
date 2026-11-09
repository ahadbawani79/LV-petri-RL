from core.petri_net import PetriNet, Place, Transition, Arc


# =========================================
# Create Espresso Machine Model
# =========================================

def create_espresso_model():

    model = PetriNet(
        name="Espresso Machine",
        model_type="SPN"
    )

    # Places
    model.add_place(
        Place("p1", "Coffee Beans", 100, "coffee_beans")
    )

    model.add_place(
        Place("p2", "Milk", 100, "milk")
    )

    model.add_place(
        Place("p3", "Espresso", 0, "espresso")
    )

    model.add_place(
        Place("p4", "Cappuccino", 0, "cappuccino")
    )

    # Transitions
    model.add_transition(
        Transition(
            "t1",
            "Make Espresso",
            rate="0.5 * coffee_beans"
        )
    )

    model.add_transition(
        Transition(
            "t2",
            "Make Cappuccino",
            rate="0.003 * coffee_beans * milk"
        )
    )

    # Make Espresso arcs
    model.add_arc(Arc("p1", "t1"))
    model.add_arc(Arc("t1", "p3"))

    # Make Cappuccino arcs
    model.add_arc(Arc("p1", "t2"))
    model.add_arc(Arc("p2", "t2"))
    model.add_arc(Arc("t2", "p4"))

    return model