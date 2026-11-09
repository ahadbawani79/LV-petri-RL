import json
import os

from core.petri_net import PetriNet, Place, Transition, Arc

# =========================================
# Load JSON File
# =========================================

def load_model(filename):

    project_folder = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    file_path = os.path.join(
        project_folder,
        "data",
        filename
    )

    with open(file_path, "r", encoding="utf-8") as file:

        model_data = json.load(file)

    print("JSON successfully loaded:", file_path)

    return model_data


# =========================================
# Reconstruct PetriNet
# =========================================

def deserialize_model(model_data):

    model_info = model_data["model"]

    model = PetriNet(
        name=model_info["name"],
        model_type=model_info["type"]
    )

    # =====================================
    # Reconstruct Places
    # =====================================

    for place_data in model_data["places"]:

        place = Place(
            place_id=place_data["id"],
            name=place_data["name"],
            initial_marking=place_data["initial_marking"],
            variable_name=place_data["variable_name"]
        )

        model.add_place(place)

    # =====================================
    # Reconstruct Transitions
    # =====================================

    for transition_data in model_data["transitions"]:

        transition = Transition(
            transition_id=transition_data["id"],
            name=transition_data["name"],
            rate=transition_data["rate"],
            guard=transition_data["guard"]
        )

        model.add_transition(transition)

    # =====================================
    # Reconstruct Arcs
    # =====================================

    for arc_data in model_data["arcs"]:

        arc = Arc(
            source=arc_data["source"],
            target=arc_data["target"],
            weight=arc_data["weight"],
            arc_type=arc_data["type"]
        )

        model.add_arc(arc)

    print("PetriNet successfully reconstructed!")

    return model


# =========================================
# Load and Reconstruct in One Function
# =========================================

def load_and_deserialize(filename):

    model_data = load_model(filename)

    model = deserialize_model(model_data)

    return model