import matplotlib.pyplot as plt

from models.espresso_machine import create_espresso_model
from engine.simulation import run_simulation

from serialization.serializer import save_model


# =========================================
# Create PetriNet
# =========================================

model = create_espresso_model()

print("Model created:", model.name)


# =========================================
# Run Original Simulation
# =========================================

history = run_simulation(
    model,
    max_time=100,
    seed=42
)

print("\nOriginal simulation completed!")

print("Total events:", len(history["time"]) - 1)


# =========================================
# Display Final Results
# =========================================

print("\n========== FINAL RESULTS ==========")

for place in model.places:

    print(
        place.name,
        ":",
        history[place.name][-1]
    )

print("===================================")


# =========================================
# Serialize Model
# =========================================

save_model(
    model,
    "espresso_machine.json"
)


# =========================================
# Plot Simulation
# =========================================

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

plt.title("Espresso Machine Simulation")

plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.show()