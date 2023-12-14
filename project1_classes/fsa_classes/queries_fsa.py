from project1_classes.fsa_classes.fsa import FSA
from typing import Callable as function


class QueriesFSA(FSA):
    def __init__(self) -> None:
        super().__init__()
        self.fsa_name = "QUERIES"
        self.accept_states.add(self.s7)

    def s0(self) -> function:
        current_input = self._get_current_input()
        next_state: function
        if current_input == 'Q':
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
        if current_input == 'e':
            next_state = self.s3
        else:
            next_state = self.s_err
        return next_state

    def s3(self) -> function:
        current_input = self._get_current_input()
        next_state: function
        if current_input == 'r':
            next_state = self.s4
        else:
            next_state = self.s_err
        return next_state

    def s4(self) -> function:
        current_input = self._get_current_input()
        next_state: function
        if current_input == 'i':
            next_state = self.s5
        else:
            next_state = self.s_err
        return next_state

    def s5(self) -> function:
        current_input = self._get_current_input()
        next_state: function
        if current_input == 'e':
            next_state = self.s6
        else:
            next_state = self.s_err
        return next_state

    def s6(self) -> function:
        current_input = self._get_current_input()
        next_state: function
        if current_input == 's':
            next_state = self.s7
        else:
            next_state = self.s_err
        return next_state

    def s7(self) -> function:
        current_input = self._get_current_input()
        next_state: function = self.s7
        return next_state
