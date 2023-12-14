from project1_classes.fsa_classes.fsa import FSA
from typing import Callable as function


class ColonDashFSA(FSA):
    def __init__(self) -> None:
        super().__init__()
        self.fsa_name = "COLON_DASH"
        self.accept_states.add(self.s2)
    
    def s0(self) -> function:
        current_input = self._get_current_input()
        next_state: function
        if current_input == ':':
            next_state = self.s1
        else:
            next_state = self.s_err
        return next_state

    def s1(self) -> function:
        current_input = self._get_current_input()
        next_state: function
        if current_input == '-':
            next_state = self.s2
        else:
            next_state = self.s_err
        return next_state

    def s2(self) -> function:
        current_input = self._get_current_input()
        next_state: function = self.s2
        return next_state


# test_fsa = ColonDashFSA()
# print(test_fsa.run(":-ljn"))
