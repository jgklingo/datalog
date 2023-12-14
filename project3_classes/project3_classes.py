from project2_classes.project2_classes import DatalogProgram
from project5_classes.graph import Graph
from copy import copy


class RTuple:
    def __init__(self, values: list):
        self.values: list = values

    def __hash__(self):
        return hash(tuple(self.values))

    def __eq__(self, other):
        if type(other) == RTuple:
            if self.values == other.values:
                return True
        return False

    def __str__(self):
        return f"({','.join(self.values)})"


class Header:
    def __init__(self, attributes: list):
        self.attributes: list = attributes


class Relation:
    def __init__(self, name: str, header: Header):
        self.name = name
        self.header = header
        self.tuples: set[RTuple] = set()

    def add_tuple(self, t: RTuple):
        self.tuples.add(t)
        pass

    def select_1(self, index: int, constant) -> 'Relation':
        new_relation = Relation(self.name, self.header)
        for t in self.tuples:
            if t.values[index] == constant:
                new_relation.add_tuple(t)
        return new_relation

    def select_2(self, index1: int, index2: int) -> 'Relation':
        new_relation = Relation(self.name, self.header)
        for t in self.tuples:
            if str(t.values[index1]) == str(t.values[index2]):
                new_relation.add_tuple(t)
        return new_relation

    def project(self, columns: list[int]) -> 'Relation':
        new_header_attributes: list = []

        for i in columns:
            new_header_attributes.append(self.header.attributes[i])

        new_header: Header = Header(new_header_attributes)

        new_relation = Relation(self.name, new_header)

        for t in self.tuples:
            new_tuple_elements: list = []
            for c in columns:
                new_tuple_elements.append(t.values[c])
            new_relation.add_tuple(RTuple(new_tuple_elements))

        return new_relation

    def rename(self, names: list[str], indexes: list[int]) -> 'Relation':
        # may need to implement deepcopy, let's see
        header_copy = [item for item in self.header.attributes]
        for i in range(len(header_copy)):
            if i in indexes:
                header_copy[i] = names[i]
        new_header = Header(header_copy)
        new_relation = Relation(self.name, new_header)
        new_relation.tuples = set([RTuple([t.values[i] for i in indexes]) for t in self.tuples])
        return new_relation

    def join(self, other: 'Relation') -> 'Relation':
        # spacing matches pseudocode
        new_header, matching = self.__combine_headers(other.header)

        new_relation = Relation(f'{self.name} \u2A1D {other.name}', new_header)

        for tuple1 in self.tuples:
            for tuple2 in other.tuples:

                if self.__is_joinable(tuple1, tuple2, matching):
                    new_tuple: RTuple = self.__combine_tuples(tuple1, tuple2, matching)
                    new_relation.add_tuple(new_tuple)

        return new_relation

    def union(self, other: 'Relation') -> bool:
        # returns whether tuples were added
        start_size = len(self.tuples)
        if self.header.attributes != other.header.attributes:
            raise ValueError("Header attributes must match")
        self.tuples = self.tuples.union(other.tuples)
        end_size = len(self.tuples)
        return end_size > start_size

    def to_string(self):
        string = ''
        for t in sorted(self.tuples, key=lambda ele: ele.values):
            i = 0
            attribute_list = []
            for attribute in self.header.attributes:
                attribute_list.append(f"{attribute}={t.values[i]}")
                i += 1
            if len(attribute_list) > 0:
                string += '  ' + ', '.join(attribute_list) + '\n'
        return string

    def __combine_headers(self, other: Header) -> (Header, dict[int:int]):
        # join helper:
        # Add all the names from one header, then add all the names that aren't already included from the other
        new_header = Header(copy(self.header.attributes))
        for attribute in other.attributes:
            if attribute not in new_header.attributes:
                new_header.attributes.append(attribute)

        matching: dict[int:int] = {}
        for self_attribute_index in range(len(self.header.attributes)):
            for other_attribute_index in range(len(other.attributes)):
                if self.header.attributes[self_attribute_index] == other.attributes[other_attribute_index]:
                    matching[other_attribute_index] = self_attribute_index

        return new_header, matching

    @staticmethod
    def __is_joinable(tuple0: RTuple, tuple1: RTuple, matching: dict[int:int]) -> bool:
        # join helper:
        # Receives two tuples and information about where they should match
        # You can store the information about where they match in a dict[int, int] of indexes (i.e. {index1 : index2}
        # Make that dict when combining the headers (you will need a doubly nested for loop)
        for index in matching:
            if tuple1.values[index] != tuple0.values[matching[index]]:
                return False
        return True

    @staticmethod
    def __combine_tuples(tuple0: RTuple, tuple1: RTuple, matching: dict[int:int]) -> RTuple:
        # join helper:
        # Receives two tuples and information about where they should match
        new_tuple = []
        for i in range(len(tuple0.values)):
            new_tuple.append(tuple0.values[i])
        for i in range(len(tuple1.values)):
            if i not in matching:
                new_tuple.append(tuple1.values[i])
        return RTuple(new_tuple)


class Database:
    def __init__(self):
        self.dictionary: dict[str:Relation] = {}

    def append(self, relation: Relation) -> None:
        self.dictionary[relation.name] = relation

    def lookup(self, name: str) -> Relation:
        return self.dictionary[name]


class Interpreter:
    def __init__(self, datalog_program: DatalogProgram):
        self.datalog_program: DatalogProgram = datalog_program
        self.database: Database = Database()
        self.create_database()

        self.rule_eval_string: str = 'Rule Evaluation\n'
        self.eval_cycles: int = 0
        self.tuples_added: bool = True

        self.dependency_graph = Graph(len(self.datalog_program.rules))
        reverse_graph = Graph(len(self.datalog_program.rules))
        outer_rule_number: int = 0
        for rule in self.datalog_program.rules:
            for body_predicate in rule.body_predicates:
                inner_rule_number = 0
                for r in self.datalog_program.rules:
                    if r.head_predicate.name == body_predicate.name:
                        self.dependency_graph.add_edge(outer_rule_number, inner_rule_number)
                        reverse_graph.add_edge(inner_rule_number, outer_rule_number)
                    inner_rule_number += 1
            outer_rule_number += 1
        reverse_postorder = reverse_graph.dfs_forest_po()
        scc_list = self.dependency_graph.dfs_forest_scc(list(reversed(reverse_postorder)))

        for scc in scc_list:
            self.tuples_added = True
            self.rule_eval_string += f"SCC: {','.join(['R' + str(num) for num in scc])}\n"
            cycles = 0

            trivial = False
            if len(scc) == 1:
                trivial = True
                for b_predicate in self.datalog_program.rules[next(iter(scc))].body_predicates:
                    if b_predicate.name == self.datalog_program.rules[next(iter(scc))].head_predicate.name:
                        trivial = False

            if trivial:
                self.evaluate_rules(self.datalog_program.rules[next(iter(scc))])
                cycles = 1
            else:
                while self.tuples_added:
                    self.tuples_added = False
                    for rule_number in sorted(scc):  # sorted?
                        if self.evaluate_rules(self.datalog_program.rules[rule_number]):
                            self.tuples_added = True
                    cycles += 1
            self.rule_eval_string += f"{str(cycles)} passes: {','.join(['R' + str(num) for num in scc])}\n"

        self.evaluated_queries: list[Relation] = []
        for query in self.datalog_program.queries:
            self.evaluated_queries.append(self.evaluate_query(query))
        pass

    def __str__(self):
        string = ''
        string += "Dependency Graph\n" + self.dependency_graph.to_string()
        string += self.rule_eval_string + '\n'
        string += 'Query Evaluation\n'
        for query, original_query in zip(self.evaluated_queries, self.datalog_program.queries):
            query_arguments: list[str] = [q.value for q in original_query.parameters]
            string += f"{query.name}({','.join(query_arguments)})? "
            if len(query.tuples) > 0:
                string += f"Yes({len(query.tuples)})\n"
            else:
                string += "No\n"
            string += query.to_string()
        return string

    def create_database(self):
        for scheme in self.datalog_program.schemes:
            new_header: Header = Header([p.value for p in scheme.parameters])
            new_relation: Relation = Relation(scheme.name, new_header)
            self.database.append(new_relation)
        for fact in self.datalog_program.facts:
            relation = self.database.lookup(fact.name)
            relation.add_tuple(RTuple([i.value for i in fact.parameters]))

    def evaluate_query(self, query):
        relation: Relation = self.database.lookup(query.name)

        # select
        seen_ids: dict = {}
        for i in range(len(query.parameters)):
            if not query.parameters[i].is_id:
                if query.parameters[i].value not in seen_ids:
                    seen_ids[query.parameters[i].value] = i
                else:
                    relation = relation.select_2(seen_ids[query.parameters[i].value], i)
            else:
                relation = relation.select_1(i, query.parameters[i].value)

        # project
        variable_indexes: list[int] = []
        seen_variables: list[str] = []
        for i in range(len(query.parameters)):
            if not query.parameters[i].is_id:
                if query.parameters[i].value not in seen_variables:
                    variable_indexes.append(i)
                    seen_variables.append(query.parameters[i].value)
        relation = relation.project(variable_indexes)

        # rename
        relation = relation.rename([query.parameters[i].value for i in variable_indexes],
                                   list(range(len(relation.header.attributes))))

        return relation

    def evaluate_rules(self, rule) -> bool:
        if rule.head_predicate.name == "Roll":
            pass
        # evaluate the predicates on the right-hand side of the rule
        evaluated_queries: list[Relation] = []
        for bp in rule.body_predicates:
            evaluated_queries.append(self.evaluate_query(bp))
        # join the relations that result
        while len(evaluated_queries) > 1:
            evaluated_queries[0] = evaluated_queries[0].join(evaluated_queries[1])
            evaluated_queries.remove(evaluated_queries[1])
        evaluated_rule = evaluated_queries[0]
        # project the columns that appear in the head predicate
        project_indexes = []
        for p in rule.head_predicate.parameters:
            for a in evaluated_rule.header.attributes:
                if p.value == a:
                    project_indexes.append(evaluated_rule.header.attributes.index(a))
        evaluated_rule = evaluated_rule.project(project_indexes)
        # rename the relation to make it union compatible
        database_relation = self.database.lookup(rule.head_predicate.name)
        evaluated_rule = evaluated_rule.rename(database_relation.header.attributes, [i for i in range(len(rule.head_predicate.parameters))])
        # part of printing code (see below)
        remove_for_printout = []
        for t in evaluated_rule.tuples:
            if t in database_relation.tuples:
                remove_for_printout.append(t)
        # union with the relation in the database
        tuples_added = database_relation.union(evaluated_rule)
        # print for grader
        for t in remove_for_printout:
            evaluated_rule.tuples.remove(t)
        self.rule_eval_string += str(rule) + '\n' + evaluated_rule.to_string()
        return tuples_added


# R1 = Relation('R', Header(['char', 'int']), )
# R1.add_tuple(RTuple(['a', 1]))
# R1.add_tuple(RTuple(['b', 2]))
# R1.add_tuple(RTuple(['c', 3]))
# R1.add_tuple(RTuple(['d', 4]))
# R2 = Relation('Q', Header(['char', 'int']))
# R2.add_tuple(RTuple(['f', 3]))
# P = R1.union(R2)
# pass
