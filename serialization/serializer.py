import json
import os


# =========================================
# Serialize PetriNet into Python Dictionary
# =========================================

def serialize_model(model):

    model_data = {

        "model": {
            "name": model.name,
            "type": model.model_type
        },

        "places": [],

        "transitions": [],

        "arcs": []

    }

    # =====================================
    # Serialize Places
    # =====================================

    for place in model.places:

        place_data = {

            "id": place.id,

            "name": place.name,

            "variable_name": place.variable_name,

            "initial_marking": place.initial_marking

        }

        model_data["places"].append(place_data)

    # =====================================
    # Serialize Transitions
    # =====================================

    for transition in model.transitions:

        transition_data = {

            "id": transition.id,

            "name": transition.name,

            "rate": transition.rate,

            "guard": transition.guard

        }

        model_data["transitions"].append(transition_data)

    # =====================================
    # Serialize Arcs
    # =====================================

    for arc in model.arcs:

        arc_data = {

            "source": arc.source,

            "target": arc.target,

            "weight": arc.weight,

            "type": arc.arc_type

        }

        model_data["arcs"].append(arc_data)

    return model_data


# =========================================
# Save Model as JSON
# =========================================

def save_model(model, filename):

    model_data = serialize_model(model)

    # Locate data folder
    project_folder = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    data_folder = os.path.join(
        project_folder,
        "data"
    )

    os.makedirs(data_folder, exist_ok=True)

    file_path = os.path.join(
        data_folder,
        filename
    )

    # Save JSON
    with open(file_path, "w", encoding="utf-8") as file:

        json.dump(
            model_data,
            file,
            indent=4
        )

    print("\nModel successfully serialized!")

    print("File saved at:", file_path)

    return file_path