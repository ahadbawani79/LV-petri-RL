import sys
import os
import matplotlib.pyplot as plt

from serialization.deserializer import load_and_deserialize
from engine.simulation import run_simulation


# =========================================
# Get JSON Filename
# =========================================

def get_filename():

    if len(sys.argv) > 1:

        return sys.argv[1]

    filename = input(
        "Enter JSON filename (e.g. espresso_machine.json): "
    ).strip()

    return filename


# =========================================
# Run Model
# =========================================

def run_model(filename):

    print("\n===================================")
    print("       PETRI NET SIMULATOR")
    print("===================================\n")

    # Check file extension
    if not filename.endswith(".json"):

        raise ValueError(
            "Please provide a JSON filename."
        )

    # Check JSON file exists
    project_folder = os.path.dirname(
        os.path.abspath(__file__)
    )

    file_path = os.path.join(
        project_folder,
        "data",
        filename
    )

    if not os.path.isfile(file_path):

        raise FileNotFoundError(
            f"Model file not found: {file_path}"
        )

    # =====================================
    # Deserialize Model
    # =====================================

    model = load_and_deserialize(filename)

    print("\n========== MODEL INFORMATION ==========")

    print("Model Name:", model.name)

    print("Model Type:", model.model_type)

    print("Places:", len(model.places))

    print("Transitions:", len(model.transitions))

    print("Arcs:", len(model.arcs))

    # =====================================
    # Display Initial Markings
    # =====================================

    print("\n========== INITIAL MARKINGS ==========")

    for place in model.places:

        print(
            place.name,
            ":",
            place.initial_marking
        )

    # =====================================
    # Run Simulation
    # =====================================

    print("\n========== SIMULATION ==========")

    max_time = 100

    seed = 42

    history = run_simulation(
        model,
        max_time=max_time,
        seed=seed
    )

    print("Simulation completed!")

    print("Simulation time:", history["time"][-1])

    print(
        "Total events:",
        len(history["time"]) - 1
    )

    # =====================================
    # Display Final Markings
    # =====================================

    print("\n========== FINAL MARKINGS ==========")

    for place in model.places:

        final_value = history[place.name][-1]

        print(
            place.name,
            ":",
            final_value
        )

    # =====================================
    # Plot Simulation
    # =====================================

    plt.figure(figsize=(12, 7))

    for place in model.places:

        plt.step(
            history["time"],
            history[place.name],
            where="post",
            label=place.name
        )

    plt.xlabel("Simulation Time")

    plt.ylabel("Tokens")

    plt.title(model.name + " Simulation")

    plt.legend()

    plt.grid(True, alpha=0.3)

    plt.tight_layout()

    plt.show()


# =========================================
# Main
# =========================================

if __name__ == "__main__":

    try:

        filename = get_filename()

        if not filename:

            raise ValueError(
                "No JSON filename provided."
            )

        run_model(filename)

    except (ValueError, FileNotFoundError, KeyError) as error:

        print("\nERROR:", error)

    except Exception as error:

        print("\nUnexpected error:", error)