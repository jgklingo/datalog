from typing import Callable as function
# Note: Despite their names, these are not actually FSAs, they're FSMs...


class FSA:
    def __init__(self) -> None:
        self.start_state: function = self.s0
        self.current_state: function = self.s0
        self.accept_states: set[function] = set()

        self.input_string: str = ""
        self.fsa_name: str = "UNDEFINED"
        self.num_chars_read: int = 0
        self.chars_in_token: int = 0

    def s0(self) -> function:
        raise NotImplementedError()

    def s_err(self) -> function:
        current_input = self._get_current_input()
        next_state: function = self.s_err
        return next_state
    
    def run(self, input_string: str) -> int:
        # Remember input_string
        self.input_string = input_string
        # Set current state to start state
        self.current_state: function = self.start_state
        # Call current state, which starts the FSA
        while self.num_chars_read < len(self.input_string):
            self.current_state = self.current_state()
        # If accept state not reached, show failure by setting value to 0
        if self.current_state not in self.accept_states:
            self.chars_in_token = 0
        return self.chars_in_token

    def reset(self) -> None:
        self.num_chars_read = 0
        self.chars_in_token = 0

    def get_name(self) -> str:
        return self.fsa_name

    def set_name(self, FSA_name) -> None:
        self.fsa_name = FSA_name

    def _get_current_input(self) -> str:  # Removed second underscore to allow inheritance
        current_input: str = self.input_string[self.num_chars_read]
        if self.current_state not in self.accept_states:
            self.chars_in_token += 1
        self.num_chars_read += 1
        return current_input
