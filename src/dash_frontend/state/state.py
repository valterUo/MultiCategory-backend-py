class State:

    def __init__(self, initial_state, possible_states):
        self.possible_states = possible_states
        self.state = self.possible_states[initial_state]

    def get_current_state(self):
        return self.state

    def get_possible_states(self):
        return self.possible_states

    def change_state(self, new_state):
        self.state = self.possible_states[new_state]

    def update_possible_states(self, key, new_state):
        self.possible_states[key] = new_state

    def get_state_with_key(self, key):
        return self.possible_states[key]