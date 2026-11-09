import random
import math
from engine.expression import evaluate_expression, evaluate_condition

# =========================================
# Get Place
# =========================================

def get_place(model, place_id):

    for place in model.places:

        if place.id == place_id:
            return place

    raise ValueError(
        f"Place not found: {place_id}"
    )


# =========================================
# Check Transition Enabled
# =========================================

def is_transition_enabled(model, transition, state):

    # =====================================
    # Step 1: Evaluate Transition Guard
    # =====================================

    guard_result = evaluate_condition(
        transition.guard,
        state
    )

    if not guard_result:

        return False

    # =====================================
    # Step 2: Check Input Token Availability
    # =====================================

    input_arcs = [
        arc for arc in model.arcs
        if arc.target == transition.id
    ]

    for arc in input_arcs:

        place = get_place(
            model,
            arc.source
        )

        available_tokens = state[place.variable_name]

        if available_tokens < arc.weight:

            return False

    return True
    


# =========================================
# Calculate Transition Rates
# =========================================

def calculate_transition_rates(model, state):

    rates = {}

    for transition in model.transitions:

        if not is_transition_enabled(
            model,
            transition,
            state
        ):

            rates[transition.id] = 0
            continue

        rate = evaluate_expression(
            transition.rate,
            state
        )

        rates[transition.id] = max(
            0,
            rate
        )

    return rates


# =========================================
# Fire Transition
# =========================================

def fire_transition(model, transition, state):

    input_arcs = [
        arc for arc in model.arcs
        if arc.target == transition.id
    ]

    output_arcs = [
        arc for arc in model.arcs
        if arc.source == transition.id
    ]

    # Consume input tokens
    for arc in input_arcs:

        place = get_place(
            model,
            arc.source
        )

        state[place.variable_name] -= arc.weight

    # Produce output tokens
    for arc in output_arcs:

        place = get_place(
            model,
            arc.target
        )

        state[place.variable_name] += arc.weight


# =========================================
# Run Simulation
# =========================================

def run_simulation(model, max_time=100, seed=42):

    random.seed(seed)

    state = {

        place.variable_name: place.initial_marking

        for place in model.places

    }

    history = {

        "time": [0]

    }

    for place in model.places:

        history[place.name] = [

            state[place.variable_name]

        ]

    current_time = 0

    while current_time < max_time:

        rates = calculate_transition_rates(
            model,
            state
        )

        total_rate = sum(rates.values())

        if total_rate <= 0:

            break

        random_value = max(
            random.random(),
            1e-12
        )

        time_step = -math.log(
            random_value
        ) / total_rate

        if current_time + time_step > max_time:

            break

        current_time += time_step

        selection = random.random() * total_rate

        cumulative_rate = 0

        selected_transition = None

        for transition in model.transitions:

            cumulative_rate += rates[transition.id]

            if selection < cumulative_rate:

                selected_transition = transition

                break

        if selected_transition is None:

            continue

        fire_transition(
            model,
            selected_transition,
            state
        )

        history["time"].append(
            current_time
        )

        for place in model.places:

            history[place.name].append(
                state[place.variable_name]
            )

    return history