from project1_classes.fsa_classes.fsa import FSA
from typing import Callable as function


class CommentFSA(FSA):
    def __init__(self) -> None:
        super().__init__()
        self.fsa_name = "COMMENT"
        self.accept_states.add(self.s1)
        self.accept_states.add(self.s2)

    def s0(self) -> function:
        current_input = self._get_current_input()
        next_state: function
        if current_input == '#':
            next_state = self.s1
        else:
            next_state = self.s_err
        return next_state

    def s1(self) -> function:
        current_input = self._get_current_input()
        next_state: function
        if current_input == '\n':
            next_state = self.s2
        else:
            next_state = self.s1
            self.chars_in_token += 1  # hard-coded, not great
        return next_state

    def s2(self) -> function:
        current_input = self._get_current_input()
        next_state: function = self.s2
        return next_state
