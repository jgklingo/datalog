from typing import List

from project1_classes.token import Token
from project1_classes.fsa_classes.colon_dash_fsa import *
from project1_classes.fsa_classes.colon_fsa import *
from project1_classes.fsa_classes.left_paren_fsa import *
from project1_classes.fsa_classes.right_paren_fsa import *
from project1_classes.fsa_classes.comma_fsa import *
from project1_classes.fsa_classes.period_fsa import *
from project1_classes.fsa_classes.q_mark_fsa import *
from project1_classes.fsa_classes.multiply_fsa import *
from project1_classes.fsa_classes.add_fsa import *
from project1_classes.fsa_classes.schemes_fsa import *
from project1_classes.fsa_classes.facts_fsa import *
from project1_classes.fsa_classes.rules_fsa import *
from project1_classes.fsa_classes.queries_fsa import *
from project1_classes.fsa_classes.ids_fsa import *
from project1_classes.fsa_classes.string_fsa import *
from project1_classes.fsa_classes.comment_fsa import *


# from typing import Callable as function


class LexerFSM:
    def __init__(self) -> None:
        self.tokens: list[Token] = []

        self.undefined_fsa: FSA = FSA()
        self.colon_dash_fsa: ColonDashFSA = ColonDashFSA()
        self.colon_fsa: ColonFSA = ColonFSA()
        self.right_paren_fsa: RightParenFSA = RightParenFSA()
        self.left_paren_fsa: LeftParenFSA = LeftParenFSA()
        self.comma_fsa: CommaFSA = CommaFSA()
        self.period_fsa: PeriodFSA = PeriodFSA()
        self.q_mark_fsa: QMarkFSA = QMarkFSA()
        self.multiply_fsa: MultiplyFSA = MultiplyFSA()
        self.add_fsa: AddFSA = AddFSA()
        self.schemes_fsa: SchemesFSA = SchemesFSA()
        self.facts_fsa: FactsFSA = FactsFSA()
        self.rules_fsa: RulesFSA = RulesFSA()
        self.queries_fsa: QueriesFSA = QueriesFSA()
        self.ids_fsa: IDsFSA = IDsFSA()
        self.string_fsa: StringFSA = StringFSA()
        self.comment_fsa: CommentFSA = CommentFSA()
        # import and create instances of all the other FSAs, then add them to self.fsa_keys

        self.line_number: int = 1

        # special keywords MUST come before IDs to avoid conflict
        self.fsa_keys: list = [self.colon_dash_fsa, self.colon_fsa, self.right_paren_fsa, self.left_paren_fsa,
                               self.comma_fsa, self.period_fsa, self.q_mark_fsa, self.multiply_fsa, self.add_fsa,
                               self.schemes_fsa, self.facts_fsa, self.rules_fsa, self.queries_fsa, self.ids_fsa,
                               self.string_fsa, self.comment_fsa]

        self.fsa_dict: dict = dict.fromkeys(self.fsa_keys, 0)

    def run(self, input_string: str) -> list[Token]:
        while len(input_string) > 0:
            # whitespace check
            if input_string.isspace():  # eliminate trailing whitespace
                for char in input_string:
                    if char == '\n':
                        self.line_number += 1
                input_string = ''
                break
            while len(input_string) > 0 and input_string[0].isspace():
                if input_string[0] == '\n':
                    self.line_number += 1
                input_string = input_string[1:]

            # lex
            token: Token = self.lex(input_string)
            if token.token_type == "UNDEFINED":
                self.tokens.append(token)
                break  # check this line for problems
            self.tokens.append(token)

            # remove lexed characters
            input_string = input_string[len(token.value):]

        # add EOF token if end of input is reached
        if len(input_string) == 0:
            self.tokens.append(Token("EOF", "", self.line_number))

        # return formatted answer
        return self.tokens

    def lex(self, input_string: str) -> Token:
        # print(input_string)  # DEBUG
        # runs the entire remaining input string through every FSA
        for fsa in self.fsa_dict.keys():
            fsa.reset()
            self.fsa_dict[fsa] = fsa.run(input_string)
        return self.__manager_fsm__(input_string)

    def __manager_fsm__(self, input_string: str) -> Token:
        # output_token: Token = Token('UNDEFINED', '', 0)   # modify with correct value and line number
        max_chars: int = 0
        max_fsa: FSA = self.undefined_fsa
        for fsa in self.fsa_dict.keys():
            if self.fsa_dict[fsa] > max_chars:
                max_chars = self.fsa_dict[fsa]
                max_fsa = fsa
        if max_fsa == self.undefined_fsa:
            output_token = Token(max_fsa.get_name(), input_string[0:1], self.line_number)
        else:
            output_token = Token(max_fsa.get_name(), input_string[0:max_chars], self.line_number)
        return output_token

    def reset(self) -> None:
        for fsa in self.fsa_dict.keys():
            fsa.reset()
