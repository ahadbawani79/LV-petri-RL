# =========================================
# Place
# =========================================

class Place:

    def __init__(self, place_id, name, initial_marking, variable_name):

        self.id = place_id
        self.name = name
        self.initial_marking = initial_marking
        self.variable_name = variable_name


# =========================================
# Transition
# =========================================

class Transition:

    def __init__(self, transition_id, name, rate, guard="True"):

        self.id = transition_id
        self.name = name
        self.rate = rate
        self.guard = guard


# =========================================
# Arc
# =========================================

class Arc:

    def __init__(self, source, target, weight=1, arc_type="normal"):

        self.source = source
        self.target = target
        self.weight = weight
        self.arc_type = arc_type


# =========================================
# PetriNet
# =========================================

class PetriNet:

    def __init__(self, name, model_type="SPN"):

        self.name = name
        self.model_type = model_type

        self.places = []
        self.transitions = []
        self.arcs = []

    def add_place(self, place):

        self.places.append(place)

    def add_transition(self, transition):

        self.transitions.append(transition)

    def add_arc(self, arc):

        self.arcs.append(arc)