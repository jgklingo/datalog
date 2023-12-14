from project1_classes.fsa_classes.fsa import FSA
from typing import Callable as function

class MultiplyFSA(FSA):
    def __init__(self) -> None:
        super().__init__()
        self.fsa_name = "MULTIPLY"
        self.accept_states.add(self.s1)

    def s0(self) -> function:
        current_input = self._get_current_input()
        next_state: function
        if current_input == '*':
            next_state = self.s1
        else:
            next_state = self.s_err
        return next_state

    def s1(self) -> function:
        current_input = self._get_current_input()
        next_state: function = self.s1
        return next_state
