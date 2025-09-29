from collections import namedtuple

Token = namedtuple("Token", ["label", "data", "line", "column"])

class LexerState:
    def __init__(self):
        self.pos = 0
        self.line = 1
        self.column = 1
    
    def advance_line(self):
        self.column = 0
        self.advance_column()
        self.line += 1
    
    def reset_line(self):
        self.line = 1

    def reset_column(self):
        self.column = 1
    
    def advance_column(self, amount=1):
        self.column += amount
        self.pos += amount

# The ordering of these lex items is by logical grouping.
# If you're adding new tokens, ensure that they won't get picked
# up by earlier tokens in a different lexing group.
def lex(input):
    state = LexerState()
    state.pos = 0
    while state.pos < len(input):
        start_line = state.line
        start_column = state.column

        # Whitespace.
        if input[state.pos].isspace():
            if input[state.pos] == '\n':
                state.advance_line()
            else:
                state.advance_column()
            continue
        elif input[state.pos:state.pos+4] == "null":
            yield Token("Null", "null", start_line, start_column)
            state.advance_column(4)

        # Comparison operators.
        elif input[state.pos:state.pos+2] == "==":
            yield Token("Eq", "==", start_line, start_column)
            state.advance_column(2)
        elif input[state.pos:state.pos+2] == "!=":
            yield Token("Neq", "!=", start_line, start_column)
            state.advance_column(2)
        elif input[state.pos:state.pos+2] == "<=":
            yield Token("Lte", "<=", start_line, start_column)
            state.advance_column(2)
        elif input[state.pos] == "<":
            yield Token("Lt", "<", start_line, start_column)
            state.advance_column()
        elif input[state.pos:state.pos+2] == ">=":
            yield Token("Gte", ">=", start_line, start_column)
            state.advance_column(2)
        elif input[state.pos] == ">":
            yield Token("Gt", ">", start_line, start_column)
            state.advance_column()

        # Ands and Ors and other bits and bobs.
        elif is_token_match(input, state.pos, "nand"):
            yield Token("Nand", "nand", start_line, start_column)
            state.advance_column(4)
        elif is_token_match(input, state.pos, "and"):
            yield Token("And", "and", start_line, start_column)
            state.advance_column(3)
        elif is_token_match(input, state.pos, "xnor"):
            yield Token("Xnor", "xnor", start_line, start_column)
            state.advance_column(4)
        elif is_token_match(input, state.pos, "xor"):
            yield Token("Xor", "xor", start_line, start_column)
            state.advance_column(3)
        elif is_token_match(input, state.pos, "nor"):
            yield Token("Nor", "nor", start_line, start_column)
            state.advance_column(3)
        elif is_token_match(input, state.pos, "not"):
            yield Token("Not", "not", start_line, start_column)
            state.advance_column(3)
        elif input[state.pos] == "!":
            yield Token("Not", "!", start_line, start_column)
            state.advance_column()
        elif is_token_match(input, state.pos, "or"):
            yield Token("Or", "or", start_line, start_column)
            state.advance_column(2)

        # Assignment
        elif input[state.pos:state.pos+2] == "+=":
            yield Token("Addassign", "+=", start_line, start_column)
            state.advance_column(2)
        elif input[state.pos:state.pos+2] == "-=":
            yield Token("Subassign", "-=", start_line, start_column)
            state.advance_column(2)
        elif input[state.pos:state.pos+2] == "*=":
            yield Token("Mulassign", "*=", start_line, start_column)
            state.advance_column(2)
        elif input[state.pos:state.pos+2] == "/=":
            yield Token("Divassign", "/=", start_line, start_column)
            state.advance_column(2)
        elif input[state.pos] == "=":
            yield Token("Assignment", "=", start_line, start_column)
            state.advance_column()

        # Mathematics
        elif input[state.pos] == "-" or input[state.pos] == "−":
            yield Token("Subtraction", "-", start_line, start_column)
            state.advance_column()
        elif input[state.pos] == "+":
            yield Token("Addition", "+", start_line, start_column)
            state.advance_column()
        elif input[state.pos] == "/" or input[state.pos] == "÷":
            yield Token("Division", "/", start_line, start_column)
            state.advance_column()
        elif input[state.pos:state.pos+2] == "**":
            yield Token("Exponent", "**", start_line, start_column)
            state.advance_column(2)
        elif input[state.pos] == "*" or input[state.pos] == "∗":
            yield Token("Multiplication", "*", start_line, start_column)
            state.advance_column()
        elif input[state.pos] == "%":
            yield Token("Modulo", "%", start_line, start_column)
            state.advance_column()

        # Keywords
        elif is_token_match(input, state.pos, "let"):
            yield Token("Let", "let", start_line, start_column)
            state.advance_column(3)
        elif is_token_match(input, state.pos, "shadow"):
            yield Token("Shadow", "shadow", start_line, start_column)
            state.advance_column(6)
        elif is_token_match(input, state.pos, "constant"):
            yield Token("Constant", "constant", start_line, start_column)
            state.advance_column(8)
        elif is_token_match(input, state.pos, "print"):
            yield Token("Print", "print", start_line, start_column)
            state.advance_column(5)
        elif is_token_match(input, state.pos, "spread"):
            yield Token("Spread", "spread", start_line, start_column)
            state.advance_column(6)

        ## Conditionals
        elif is_token_match(input, state.pos, "use"):
            yield Token("Use", "use", start_line, start_column)
            state.advance_column(3)
        elif is_token_match(input, state.pos, "over"):
            yield Token("Over", "over", start_line, start_column)
            state.advance_column(4)
        elif is_token_match(input, state.pos, "unless"):
            yield Token("Unless", "unless", start_line, start_column)
            state.advance_column(6)
        elif is_token_match(input, state.pos, "endif"):
            yield Token("Endif", "endif", start_line, start_column)
            state.advance_column(5)
        elif is_token_match(input, state.pos, "elif"):
            yield Token("Elif", "elif", start_line, start_column)
            state.advance_column(4)
        elif is_token_match(input, state.pos, "if"):
            yield Token("If", "if", start_line, start_column)
            state.advance_column(2)
        elif is_token_match(input, state.pos, "then"):
            yield Token("Then", "then", start_line, start_column)
            state.advance_column(4)
        elif is_token_match(input, state.pos, "else"):
            yield Token("Else", "else", start_line, start_column)
            state.advance_column(4)
        elif is_token_match(input, state.pos, "endcase"):
            yield Token("Endcase", "endcase", start_line, start_column)
            state.advance_column(7)
        elif is_token_match(input, state.pos, "case"):
            yield Token("Case", "case", start_line, start_column)
            state.advance_column(4)
        elif is_token_match(input, state.pos, "when"):
            yield Token("When", "when", start_line, start_column)
            state.advance_column(4)
        elif is_token_match(input, state.pos, "otherwise"):
            yield Token("Otherwise", "otherwise", start_line, start_column)
            state.advance_column(9)

        ## Iterators
        elif is_token_match(input, state.pos, "enduntil"):
            yield Token("Enduntil", "enduntil", start_line, start_column)
            state.advance_column(8)
        elif is_token_match(input, state.pos, "until"):
            yield Token("Until", "until", start_line, start_column)
            state.advance_column(5)
        elif is_token_match(input, state.pos, "repeat"):
            yield Token("Repeat", "repeat", start_line, start_column)
            state.advance_column(6)
        elif is_token_match(input, state.pos, "enditerate"):
            yield Token("Enditerate", "enditerate", start_line, start_column)
            state.advance_column(10)
        elif is_token_match(input, state.pos, "iterate"):
            yield Token("Iterate", "iterate", start_line, start_column)
            state.advance_column(7)
        elif is_token_match(input, state.pos, "with"):
            yield Token("With", "with", start_line, start_column)
            state.advance_column(4)

        ## Functions
        elif is_token_match(input, state.pos, "endfn"):
            yield Token("Endfn", "endfn", start_line, start_column)
            state.advance_column(5)
        elif is_token_match(input, state.pos, "fn"):
            yield Token("Fn", "fn", start_line, start_column)
            state.advance_column(2)
        elif is_token_match(input, state.pos, "returns"):
            yield Token("Returns", "returns", start_line, start_column)
            state.advance_column(7)
        elif is_token_match(input, state.pos, "return"):
            yield Token("Return", "return", start_line, start_column)
            state.advance_column(6)
        elif is_token_match(input, state.pos, "variadic"):
            yield Token("Variadic", "variadic", start_line, start_column)
            state.advance_column(8)
        elif is_token_match(input, state.pos, "false"):
            yield Token("Boolean", False, start_line, start_column)
            state.advance_column(5)
        elif is_token_match(input, state.pos, "true"):
            yield Token("Boolean", True, start_line, start_column)
            state.advance_column(4)

        ## Delimiters
        elif input[state.pos] == "(":
            yield Token("LParen", "(", start_line, start_column)
            state.advance_column()
        elif input[state.pos] == ")":
            yield Token("RParen", ")", start_line, start_column)
            state.advance_column()
        elif input[state.pos] == "[":
            yield Token("LBrace", "[", start_line, start_column)
            state.advance_column()
        elif input[state.pos] == "]":
            yield Token("RBrace", "]", start_line, start_column)
            state.advance_column()
        elif input[state.pos] == ":":
            yield Token("Colon", ":", start_line, start_column)
            state.advance_column()
        elif input[state.pos] == ",":
            yield Token("Comma", ",", start_line, start_column)
            state.advance_column()

        # Comments
        elif input[state.pos:state.pos+3] == "###":
            state.advance_column(3)
            while state.pos + 2 < len(input) and input[state.pos:state.pos+3] != "###":
                if input[state.pos] == '\n':
                    state.advance_line()
                else:
                    state.advance_column()
            if state.pos + 2 >= len(input):
                raise ValueError(f"Unterminated multiline comment at line {start_line}, column {start_column}")
            state.advance_column(3)
            continue

        elif input[state.pos] == "#":
            while state.pos < len(input) and input[state.pos] != '\n':
                state.advance_column()

        # Strings
        elif input[state.pos] == '"':
            t = ""
            state.advance_column()
            while state.pos < len(input) and input[state.pos] != '"' or (input[state.pos-1] == '\\' and input[state.pos] == '"'):
                t += input[state.pos]
                if input[state.pos] == '\n':
                    state.advance_line()
                else:
                    state.advance_column()
            if state.pos >= len(input) or input[state.pos] != '"':
                raise ValueError(f"Unterminated string at line {start_line}, column {start_column}")
            else:
                yield Token("String", t, start_line, start_column)
            state.advance_column()

        elif input[state.pos:state.pos+2] == "0x":
            num = input[state.pos:state.pos+2]
            state.advance_column(2)
            hex_chars = ['0','1','2','3','4','5','6','7',
                         '8','9','a','b','c','d','e','f']
            while state.pos < len(input) and input[state.pos].lower() in hex_chars:
                num += input[state.pos]
                state.advance_column()
            if num == "0x":
                raise ValueError(f"Unterminated hex digit at line {start_line}, column {start_column}")
            yield Token("Hex", int(num, 16), start_line, start_column)
        elif input[state.pos:state.pos+2] == "0o":
            num = input[state.pos:state.pos+2]
            state.advance_column(2)
            octal_chars = ['0','1','2','3','4','5','6','7']
            while state.pos < len(input) and input[state.pos].lower() in octal_chars:
                num += input[state.pos]
                state.advance_column()
            if num == "0o":
                raise ValueError(f"Unterminated octal digit at line {start_line}, column {start_column}")
            yield Token("Octal", int(num, 8), start_line, start_column)
        elif input[state.pos:state.pos+2] == "0b":
            num = input[state.pos:state.pos+2]
            state.advance_column(2)
            hex_chars = ['0','1']
            while state.pos < len(input) and input[state.pos].lower() in hex_chars:
                num += input[state.pos]
                state.advance_column()
            if num == "0b":
                raise ValueError(f"Unterminated binary digit at line {start_line}, column {start_column}")
            yield Token("Binary", int(num, 2), start_line, start_column)
        # Numbers
        elif input[state.pos].isnumeric() or input[state.pos] == '.':
            num = input[state.pos]
            state.advance_column()
            while state.pos < len(input) and (input[state.pos].isnumeric() or input[state.pos] == '.'):
                num += input[state.pos]
                state.advance_column()
            if num.count('.') > 1:
                raise ValueError(f"Invalid floating point number detected at line {start_line}, column {start_column}")
            elif num.count('.') == 1:
                yield Token("Float", float(num), start_line, start_column)
            else:
                yield Token("Integer", int(num), start_line, start_column)

        # Identifiers
        else:
            t = input[state.pos]
            state.advance_column()
            while state.pos < len(input) and is_identifier(input[state.pos]):
                t += input[state.pos]
                state.advance_column()
            yield Token("Identifier", t, start_line, start_column)


def is_token_match(input, pos, expect):
    # Can't be a valid token if the state.position and expected string exceed the length.
    if pos + len(expect) > len(input):
        return False

    # Can't be a valid token if the substring is not present.
    if input[pos:pos+len(expect)] != expect:
        return False

    # If the substring is at the end of the input, it's valid because there are no characters after.
    if pos + len(expect) == len(input):
        return True

    # The next character can't be an identifier character.
    return not is_identifier(input[pos+len(expect)])


def is_identifier(c):
    symbol_blacklist = ["=", "+", "-", "/", "*", "%", "^", "(", ")", "[", "]", ",", ":", "!", "<", ">", "#", '"']
    return not c.isspace() and c not in symbol_blacklist

