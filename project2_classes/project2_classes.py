class DatalogProgram:
    def __init__(self):
        self.schemes: list[Predicate] = []
        self.facts: list[Predicate] = []
        self.queries: list[Predicate] = []
        self.rules: list[Rule] = []

        self.domain: set[str] = set()  # strings in the facts section

    def generate_domain(self):
        for predicate in self.facts:
            for parameter in predicate.parameters:
                self.domain.add(parameter.value)
        self.domain = sorted(self.domain)

    def __str__(self):
        string = f"Schemes({len(self.schemes)}):\n"
        for p in self.schemes:
            string += '  ' + str(p) + '\n'
        string += f"Facts({len(self.facts)}):\n"
        for p in self.facts:
            string += '  ' + str(p) + '.\n'
        string += f"Rules({len(self.rules)}):\n"
        for r in self.rules:
            string += '  ' + str(r) + '\n'
        string += f"Queries({len(self.queries)}):\n"
        for p in self.queries:
            string += '  ' + str(p) + '?\n'
        self.generate_domain()
        string += f"Domain({len(self.domain)}):\n"
        for d in self.domain:
            string += '  ' + d + '\n'
        return string


class Predicate:
    def __init__(self):
        self.parameters: list[Parameter] = []
        self.name: str = ''

    def clear(self):
        self.parameters = []
        self.name = ''

    def __str__(self):
        string = f"{self.name}({','.join([str(p) for p in self.parameters])})"
        return string


class Parameter:
    def __init__(self, value: str):
        self.value: str = value
        self.is_id: bool = self.check_id()

    def check_id(self) -> bool:
        return self.value[0] == "'" and self.value[-1] == "'"

    def __str__(self):
        return self.value


class Rule:
    def __init__(self):
        self.head_predicate: Predicate = Predicate()
        self.body_predicates: list[Predicate] = []

    def clear(self):
        self.head_predicate: Predicate = Predicate()
        self.body_predicates = []

    def __str__(self):
        string = f"{self.head_predicate} :- "
        string += ','.join([str(p) for p in self.body_predicates])
        string += '.'
        return string
