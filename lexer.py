from error import *
from collections import namedtuple
from supporting import *
from chestnut_type import *
token_types = [
    # 10 character sequences
    TokenType("Enditerate", "enditerate"),
    TokenType("Loopindex", "loop_index"),

    # 9
    TokenType("Endstruct", "endstruct"),
    TokenType("Otherwise", "otherwise"),

    # 8 character sequences
    TokenType("Constant", "constant"),
    TokenType("Continue", "continue"),
    TokenType("Enduntil", "enduntil"),
    TokenType("Endwhile", "endwhile"),
    TokenType("Variadic", "variadic"),

    # 7 character sequences
    TokenType("Endcase", "endcase"),
    TokenType("Iterate", "iterate"),
    TokenType("Returns", "returns"),

    # 6 character sequences
    TokenType("Brings", "brings"),
    TokenType("Import", "import"),
    TokenType("Repeat", "repeat"),
    TokenType("Return", "return"),
    TokenType("Shadow", "shadow"),
    TokenType("Spread", "spread"),
    TokenType("Struct", "struct"),
    TokenType("Unless", "unless"),

    # 5 character sequences
    TokenType("Boolean", "false", ChestnutBoolean(False)),
    TokenType("Break", "break"),
    TokenType("Endfn", "endfn"),
    TokenType("Endif", "endif"),
    TokenType("Outer", "outer"),
    TokenType("Until", "until"),
    TokenType("While", "while"),

    # 4 character sequences
    TokenType("Boolean", "true", ChestnutBoolean(True)),
    TokenType("Case", "case"),
    TokenType("Elif", "elif"),
    TokenType("Else", "else"),
    TokenType("Over", "over"),
    TokenType("Then", "then"),
    TokenType("When", "when"),
    TokenType("With", "with"),

    # 3 character sequences
    TokenType("BitwiseRotateLeft", "<<<"),
    TokenType("BitwiseRotateRight", ">>>"),
    TokenType("And", "and"),
    TokenType("Let", "let"),
    TokenType("Not", "not"),
    TokenType("Null", "null", None),
    TokenType("Use", "use"),
    
    # 2 character sequences
    TokenType("Addassign", "+="),
    TokenType("And", "&&"),
    TokenType("BitwiseNand", "~&"),
    TokenType("BitwiseNor", "~|"),
    TokenType("BitwiseShiftLeft", "<<"),
    TokenType("BitwiseShiftRight", ">>"),
    TokenType("BitwiseXnor", "~^"),
    TokenType("Divassign", "/="),
    TokenType("Eq", "=="),
    TokenType("Exponent", "**"),
    TokenType("Fn", "fn"),
    TokenType("Gte", ">="),
    TokenType("If", "if"),
    TokenType("Lte", "<="),
    TokenType("Modulo", "%"),
    TokenType("Mulassign", "*="),
    TokenType("Neq", "!="),
    TokenType("Or", "or"),
    TokenType("Or", "||"),
    TokenType("Subassign", "-="),

    # 1 character sequences
    TokenType("BitwiseAnd", "&"),
    TokenType("Assignment", "="),
    TokenType("Addition", "+"),
    TokenType("BitwiseNot", "~"),
    TokenType("BitwiseOr", "|"),
    TokenType("BitwiseXor", "^"),
    TokenType("Colon", ":"),
    TokenType("Comma", ","),
    TokenType("Division", "/"),
    TokenType("LBrace", "["),
    TokenType("LParen", "("),
    TokenType("Lt", "<"),
    TokenType("Gt", ">"),
    TokenType("Multiplication", "*"),
    TokenType("Not", "!"),
    TokenType("Period", "."),
    TokenType("RBrace", "]"),
    TokenType("RParen", ")"),
    TokenType("Subtraction", "-")
]

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
        found_token = None

        # Simple token types
        for token_type in token_types:
            if len(token_type.sequence) == 1:
                if input[state.pos] == token_type.sequence:
                    value = token_type.sequence
                    if token_type.default_value is not None:
                        if token_type.default_value == True or token_type.default_value == False:
                            value = ChestnutBoolean(token_type.default_value)
                        else:
                            value = token_type.default_value
                    found_token = Token(token_type.name, value, start_line, start_column)
                    state.advance_column()
                    break
            else:
                if is_token_match(input, state.pos, token_type.sequence):
                    value = token_type.sequence
                    if token_type.default_value is not None:
                        value = token_type.default_value
                    found_token = Token(token_type.name, value, start_line, start_column)
                    state.advance_column(len(token_type.sequence))
                    break
        if found_token:
            yield found_token

        # Comments
        elif input[state.pos:state.pos+3] == "###":
            state.advance_column(3)
            while state.pos + 2 < len(input) and input[state.pos:state.pos+3] != "###":
                if input[state.pos] == '\n':
                    state.advance_line()
                else:
                    state.advance_column()
            if state.pos + 2 >= len(input):
                raise SyntaxException(f"Unterminated multiline comment", line=start_line, column=start_column)
            state.advance_column(3)
            continue

        elif input[state.pos] == "#":
            while state.pos < len(input) and input[state.pos] != '\n':
                state.advance_column()

        # Strings
        elif input[state.pos] == '"':
            state.advance_column() # move past the start quote
            end_quote_pos = None
            line_ends = 0

            interpolation_depth = 0
            is_escaped = False

            # Find the end quote mark
            for quo_ind, char in enumerate(input[state.pos:]):
                if char == "{" and input[state.pos + quo_ind + 1] == "{":
                    if not is_escaped:
                        interpolation_depth = interpolation_depth + 1
                if char == "}" and input[state.pos + quo_ind + 1] == "}":
                    if not is_escaped and interpolation_depth > 0:
                        interpolation_depth = interpolation_depth - 1
                if char == '"' and not is_escaped and interpolation_depth == 0:
                    end_quote_pos = quo_ind
                    break
                if char == "\n":
                    line_ends = line_ends + 1
                is_escaped = (char == '\\' and not is_escaped)

            # no end quote.
            if end_quote_pos is None:
                raise SyntaxException("Unterminated string", line=start_line, column=start_column)

            capstr = input[state.pos:state.pos+end_quote_pos]
            if not "{{" in capstr:
                # Normal string
                yield Token("String", ChestnutString(capstr.encode().decode("unicode-escape")), line=start_line, column=start_column)
                for i in range(line_ends):
                    state.advance_line()
                state.advance_column(len(capstr) - line_ends + 1)
            else:
                # String interpolation.
                strpos = 0
                t = ""
                while strpos < len(capstr):
                    if capstr[strpos:strpos + 2] == "{{":
                        strtoken = Token("String", ChestnutString(t.encode().decode("unicode-escape")), start_line, start_column)
                        yield strtoken
                        t = ""

                        token = Token("Addition", "{{", start_line, start_column)
                        yield token

                        yield Token("LParen", "(", start_line, start_column)

                        strpos = strpos + 2 # Move past {{
                        while strpos < len(capstr) and capstr[strpos:strpos + 2] != "}}":
                            t = t + capstr[strpos]
                            strpos = strpos + 1

                        if strpos == len(capstr) or capstr[strpos:strpos + 2] != "}}":
                            raise SyntaxException("Unterminated string interpolation", line=start_line, column=start_column)

                        expression = lex(t)
                        t = ""
                        for ex in expression:
                            yield ex

                        yield Token("RParen", ")", start_line, start_column)

                        token = Token("Addition", "}}", start_line, start_column)
                        yield token

                        strpos = strpos + 2 # Move past }}
                    else:
                        t = t + capstr[strpos]
                        strpos = strpos + 1
                token = Token("String", ChestnutString(t.encode().decode("unicode-escape")), start_line, start_column)
                yield token

                for i in range(line_ends):
                    state.advance_line()
                state.advance_column(len(capstr) - line_ends + 1)

        elif input[state.pos:state.pos+2] == "0x":
            num = input[state.pos:state.pos+2]
            state.advance_column(2)
            hex_chars = ['0','1','2','3','4','5','6','7',
                         '8','9','a','b','c','d','e','f']
            while state.pos < len(input) and input[state.pos].lower() in hex_chars:
                num += input[state.pos]
                state.advance_column()
            if num == "0x":
                raise SyntaxException(f"Unterminated hex digit", line=start_line, column=start_column)
            yield Token("Integer", ChestnutInteger(int(num, 16)), start_line, start_column)
        elif input[state.pos:state.pos+2] == "0o":
            num = input[state.pos:state.pos+2]
            state.advance_column(2)
            octal_chars = ['0','1','2','3','4','5','6','7']
            while state.pos < len(input) and input[state.pos].lower() in octal_chars:
                num += input[state.pos]
                state.advance_column()
            if num == "0o":
                raise SyntaxException(f"Unterminated octal digit", line=start_line, column=start_column)
            yield Token("Integer", ChestnutInteger(int(num, 8)), start_line, start_column)
        elif input[state.pos:state.pos+2] == "0b":
            num = input[state.pos:state.pos+2]
            state.advance_column(2)
            hex_chars = ['0','1']
            while state.pos < len(input) and input[state.pos].lower() in hex_chars:
                num += input[state.pos]
                state.advance_column()
            if num == "0b":
                raise SyntaxException(f"Unterminated binary digit", line=start_line, column=start_column)
            yield Token("Integer", ChestnutInteger(int(num, 2)), start_line, start_column)
        # Numbers
        elif input[state.pos].isnumeric():
            num = input[state.pos]
            state.advance_column()
            while state.pos < len(input) and (input[state.pos].isnumeric() or input[state.pos] == '.'):
                num += input[state.pos]
                state.advance_column()
            if num.count('.') > 1:
                raise SyntaxException(f"Invalid floating point number detected", line=start_line, column=start_column)
            elif num.count('.') == 1:
                yield Token("Float", ChestnutFloat(float(num)), start_line, start_column)
            else:
                yield Token("Integer", ChestnutInteger(int(num)), start_line, start_column)

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
    symbol_blacklist = [
        ".", "=", "+", "-", "/",
        "*", "%", "^", "(", ")",
        "[", "]", ",", ":", "!",
        "<", ">", "#", '"', "~",
        "|" ]
    return not c.isspace() and c not in symbol_blacklist

