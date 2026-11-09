# Petri Net Simulation Engine

A Python-based simulation engine for creating, serializing, deserializing, and simulating Stochastic Petri Nets (SPNs).

## Features
- Places, transitions, and weighted arcs.
- Transition rates and guards.
- JSON serialization and deserialization.
- Stochastic simulation using the Gillespie algorithm.
- Simulation graphs using Matplotlib.
- Universal runner for different Petri Net models.

## Installation

1. Clone the repository:

   git clone -b test https://github.com/ahadbawani79/LV-petri-RL.git

2. Navigate to the project:

   cd LV-petri-RL

3. Create a virtual environment:

   python -m venv .venv

4. Activate the virtual environment (Windows):

   .venv\Scripts\activate

5. Install dependencies:

   pip install matplotlib

## Run the Simulation

Use the universal simulation runner:

    python run_model.py traffic_light.json

Other available models:

    python run_model.py espresso_machine.json

    python run_model.py predator_prey.json

You can also run without arguments and enter the JSON filename when prompted.

## Example Models

- Espresso Machine: Resource consumption and production.
- Predator-Prey: Population dynamics and transition guards.
- Traffic Light: Cyclic transitions and token movement.

## Future Development

- Colored Petri Nets (CPNs).
- Color sets and typed tokens.
- Arc inscriptions.
- Advanced simulation and validation.