from project3_classes.project3_classes import *
from project2_classes.parser import Parser
from project1_classes.lexer_fsm import LexerFSM as Lexer


# Return your program output here for grading (can treat this function as your "main")
def project5(input: str) -> str:
    lexer = Lexer()
    lexer.run(input)
    tokens = lexer.tokens
    parser = Parser()
    interpreter = Interpreter(parser.run(tokens))

    return str(interpreter)


def read_file_contents(filepath):
    with open(filepath, "r") as f:
        return f.read()

    # Use this to run and debug code within VS


if __name__ == "__main__":
    input_contents = read_file_contents("project5-passoff/80/input6.txt")
    print(project5(input_contents))
