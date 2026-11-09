from core.petri_net import PetriNet, Place, Transition, Arc


# =========================================
# Create Traffic Light Model
# =========================================

def create_traffic_light_model():

    model = PetriNet(
        name="Traffic Light",
        model_type="SPN"
    )

    # =====================================
    # Places
    # =====================================

    model.add_place(
        Place("p1", "Red", 1, "red")
    )

    model.add_place(
        Place("p2", "Green", 0, "green")
    )

    model.add_place(
        Place("p3", "Yellow", 0, "yellow")
    )

    # =====================================
    # Transitions
    # =====================================

    model.add_transition(
        Transition(
            "t1",
            "Red to Green",
            rate="1.0",
            guard="True"
        )
    )

    model.add_transition(
        Transition(
            "t2",
            "Green to Yellow",
            rate="1.0",
            guard="True"
        )
    )

    model.add_transition(
        Transition(
            "t3",
            "Yellow to Red",
            rate="1.0",
            guard="True"
        )
    )

    # =====================================
    # Red -> Green
    # =====================================

    model.add_arc(
        Arc("p1", "t1")
    )

    model.add_arc(
        Arc("t1", "p2")
    )

    # =====================================
    # Green -> Yellow
    # =====================================

    model.add_arc(
        Arc("p2", "t2")
    )

    model.add_arc(
        Arc("t2", "p3")
    )

    # =====================================
    # Yellow -> Red
    # =====================================

    model.add_arc(
        Arc("p3", "t3")
    )

    model.add_arc(
        Arc("t3", "p1")
    )

    return model