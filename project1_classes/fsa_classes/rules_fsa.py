from project1_classes.fsa_classes.fsa import FSA
from typing import Callable as function


class RulesFSA(FSA):
    def __init__(self) -> None:
        super().__init__()
        self.fsa_name = "RULES"
        self.accept_states.add(self.s5)

    def s0(self) -> function:
        current_input = self._get_current_input()
        next_state: function
        if current_input == 'R':
            next_state = self.s1
        else:
            next_state = self.s_err
        return next_state

    def s1(self) -> function:
        current_input = self._get_current_input()
        next_state: function
        if current_input == 'u':
            next_state = self.s2
        else:
            next_state = self.s_err
        return next_state

    def s2(self) -> function:
        current_input = self._get_current_input()
        next_state: function
        if current_input == 'l':
            next_state = self.s3
        else:
            next_state = self.s_err
        return next_state

    def s3(self) -> function:
        current_input = self._get_current_input()
        next_state: function
        if current_input == 'e':
            next_state = self.s4
        else:
            next_state = self.s_err
        return next_state

    def s4(self) -> function:
        current_input = self._get_current_input()
        next_state: function
        if current_input == 's':
            next_state = self.s5
        else:
            next_state = self.s_err
        return next_state

    def s5(self) -> function:
        current_input = self._get_current_input()
        next_state: function = self.s5
        return next_state
