from project1_classes.fsa_classes.fsa import FSA
from typing import Callable as function


class RightParenFSA(FSA):
    def __init__(self):
        FSA.__init__(self)
        self.fsa_name = "RIGHT_PAREN"
        self.accept_states.add(self.s1)

    def s0(self):
        current_input: str = self._get_current_input()
        next_state: function
        if current_input == ')':
            next_state: function = self.s1
        else:
            next_state: function = self.s_err
        return next_state

    def s1(self):
        current_input: str = self._get_current_input()
        next_state: function = self.s1
        return next_state

    def s_err(self):
        current_input: str = self._get_current_input()
        next_state: function = self.s_err
        return next_state


# testFSA = RightParenFSA()
# print(testFSA.run(")"))
