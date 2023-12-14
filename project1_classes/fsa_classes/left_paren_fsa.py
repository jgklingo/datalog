from project1_classes.fsa_classes.fsa import FSA
from typing import Callable as function


class LeftParenFSA(FSA):
    def __init__(self):
        FSA.__init__(self)  # You must invoke the __init__ of the parent class
        self.fsa_name = "LEFT_PAREN"
        self.accept_states.add(self.s1)  # Since self.accept_states is defined in parent class, I can use it here

    def s0(self):
        current_input: str = self._get_current_input()
        next_state: function
        if current_input == '(':
            next_state: function = self.s1
        else:
            next_state: function = self.s_err
        return next_state

    def s1(self):
        current_input: str = self._get_current_input()
        next_state: function = self.s1  # loop in state s1
        return next_state

    def s_err(self):
        current_input: str = self._get_current_input()
        next_state: function = self.s_err  # loop in state serr
        return next_state


# testFSA = LeftParenFSA()
# print(testFSA.run("("))
