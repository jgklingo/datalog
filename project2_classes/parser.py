from project2_classes.my_token import Token
from .project2_classes import *
from copy import deepcopy


class Parser:
    def __init__(self):
        self.tokens: list = []
        self.index: int = 0

        self.datalog_program = DatalogProgram()
        self.current_pred: Predicate = Predicate()
        self.current_rule: Rule = Rule()

    def throw_error(self):
        raise ValueError(self.get_curr_token().to_string())

    def get_curr_token(self) -> Token:
        if self.index >= len(self.tokens):
            self.index = len(self.tokens)
            self.throw_error()
        return self.tokens[self.index]

    def advance(self):
        self.index += 1

    def match(self, expected_type: str):
        # matches terminals
        if self.get_curr_token().token_type == expected_type:
            self.advance()
        else:
            self.throw_error()

    def run(self, tokens: list[Token]) -> DatalogProgram:
        self.index: int = 0
        self.tokens: list[Token] = tokens

        # remove comment tokens
        filtered_tokens: list[Token] = []
        for token in self.tokens:
            if token.token_type != "COMMENT":
                filtered_tokens.append(token)
        self.tokens = filtered_tokens

        self.parse_datalog_program()
        return self.datalog_program

    # datalogProgram	->	SCHEMES COLON scheme schemeList FACTS COLON factList RULES COLON ruleList QUERIES COLON query queryList EOF
    def parse_datalog_program(self):
        self.match("SCHEMES")
        self.match("COLON")
        self.parse_scheme()
        self.parse_scheme_list()
        self.match("FACTS")
        self.match("COLON")
        self.parse_fact_list()
        self.match("RULES")
        self.match("COLON")
        self.parse_rule_list()
        self.match("QUERIES")
        self.match("COLON")
        self.parse_query()
        self.parse_query_list()
        # self.match("EOF")
        pass

    # schemeList	->	scheme schemeList | lambda
    def parse_scheme_list(self):
        if self.get_curr_token().token_type != "FACTS":
            self.parse_scheme()
            self.parse_scheme_list()
        else:
            return

    # factList	->	fact factList | lambda
    def parse_fact_list(self):
        if self.get_curr_token().token_type != "RULES":
            self.parse_fact()
            self.parse_fact_list()
        else:
            return

    # ruleList	->	rule ruleList | lambda
    def parse_rule_list(self):
        if self.get_curr_token().token_type != "QUERIES":
            self.parse_rule()
            self.parse_rule_list()
        else:
            return

    # queryList	->	query queryList | lambda
    def parse_query_list(self):
        if self.get_curr_token().token_type != "EOF":
            self.parse_query()
            self.parse_query_list()
        else:
            return

    # scheme   	-> 	ID LEFT_PAREN ID idList RIGHT_PAREN
    def parse_scheme(self):
        self.current_pred.clear()  # part 3
        self.current_pred.name = self.get_curr_token().value  # part 3
        # use match for terminals and call functions for nonterminals
        self.match("ID")
        self.match("LEFT_PAREN")
        new_parameter = Parameter(self.get_curr_token().value)  # part 3
        self.current_pred.parameters.append(deepcopy(new_parameter))  # part 3
        self.match("ID")
        self.parse_id_list()
        self.match("RIGHT_PAREN")
        self.datalog_program.schemes.append(deepcopy(self.current_pred))  # part 3

    # fact    	->	ID LEFT_PAREN STRING stringList RIGHT_PAREN PERIOD
    def parse_fact(self):
        self.current_pred.clear()  # part 3
        self.current_pred.name = self.get_curr_token().value  # part 3
        self.match("ID")
        self.match("LEFT_PAREN")
        new_parameter = Parameter(self.get_curr_token().value)  # part 3
        self.current_pred.parameters.append(deepcopy(new_parameter))  # part 3
        self.match("STRING")
        self.parse_string_list()
        self.match("RIGHT_PAREN")
        self.match("PERIOD")
        self.datalog_program.facts.append(deepcopy(self.current_pred))  # part 3

    # rule    	->	headPredicate COLON_DASH predicate predicateList PERIOD
    def parse_rule(self):
        self.current_rule.clear()  # part 3
        self.parse_head_predicate()
        self.match("COLON_DASH")
        self.parse_predicate()
        self.parse_predicate_list()
        self.match("PERIOD")
        self.datalog_program.rules.append(deepcopy(self.current_rule))  # part 3

    # query	        ->      predicate Q_MARK
    def parse_query(self):
        self.current_pred.clear()  # part 3
        self.current_pred.name = self.get_curr_token().value  # part 3
        self.parse_predicate()
        self.match("Q_MARK")
        self.datalog_program.queries.append(deepcopy(self.current_pred))  # part 3

    # headPredicate	->	ID LEFT_PAREN ID idList RIGHT_PAREN
    def parse_head_predicate(self):
        head_predicate = Predicate()  # part 3
        head_predicate.name = self.get_curr_token().value  # part 3
        self.current_rule.head_predicate = head_predicate  # part 3
        self.current_pred = self.current_rule.head_predicate
        self.match("ID")
        self.match("LEFT_PAREN")
        new_parameter: Parameter = Parameter(self.get_curr_token().value)
        self.current_rule.head_predicate.parameters.append(deepcopy(new_parameter))
        self.match("ID")
        self.parse_id_list()
        self.match("RIGHT_PAREN")

    # predicate	->	ID LEFT_PAREN parameter parameterList RIGHT_PAREN
    def parse_predicate(self):
        body_predicate = Predicate()  # part 3
        body_predicate.name = self.get_curr_token().value  # part 3
        self.current_pred = body_predicate  # part 3
        self.match("ID")
        self.match("LEFT_PAREN")
        self.parse_parameter()
        self.parse_parameter_list()
        self.match("RIGHT_PAREN")

    # predicateList	->	COMMA predicate predicateList | lambda
    def parse_predicate_list(self):
        self.current_rule.body_predicates.append(deepcopy(self.current_pred))
        if self.get_curr_token().token_type == "COMMA":
            self.match("COMMA")
            self.parse_predicate()
            self.parse_predicate_list()
        else:
            return

    # parameterList	-> 	COMMA parameter parameterList | lambda
    def parse_parameter_list(self):
        if self.get_curr_token().token_type == "COMMA":
            self.match("COMMA")
            self.parse_parameter()
            self.parse_parameter_list()
        else:
            return

    # stringList	-> 	COMMA STRING stringList | lambda
    def parse_string_list(self):
        if self.get_curr_token().token_type == "COMMA":
            self.match("COMMA")
            new_parameter = Parameter(self.get_curr_token().value)  # part 3
            self.current_pred.parameters.append(deepcopy(new_parameter))  # part 3
            self.match("STRING")
            self.parse_string_list()
        else:
            return

    # idList  	-> 	COMMA ID idList | lambda
    def parse_id_list(self):
        # COMMA ID idList
        if self.get_curr_token().token_type == "COMMA":
            self.match("COMMA")
            new_parameter = Parameter(self.get_curr_token().value)  # part 3
            self.current_pred.parameters.append(deepcopy(new_parameter))  # part 3
            self.match("ID")
            self.parse_id_list()
        # lambda
        else:
            return

    # parameter	->	STRING | ID
    def parse_parameter(self):
        if self.get_curr_token().token_type == "STRING":
            new_parameter = Parameter(self.get_curr_token().value)  # part 3
            self.current_pred.parameters.append(deepcopy(new_parameter))  # part 3
            self.match("STRING")
        elif self.get_curr_token().token_type == "ID":
            new_parameter = Parameter(self.get_curr_token().value)  # part 3
            self.current_pred.parameters.append(deepcopy(new_parameter))  # part 3
            self.match("ID")
        else:
            self.throw_error()

    