from error import *
from collections import namedtuple
from token_types import *
from chestnut_types import *

class TokenData:
    def __init__(self, token_type, default_value=None):
        self.token_type = token_type
        self.default_value = default_value

class TrieNode:
    def __init__(self):
        self.children = {}
        self.value = None

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.max_token_length = 0

    def insert(self, key, value, default_value=None):
        current = self.root
        if len(key) > self.max_token_length:
            self.max_token_length = len(key)

        for c in key:
            if c not in current.children:
                current.children[c] = TrieNode()
            current = current.children[c]
        current.value = TokenData(value, default_value)

    def search(self, key):
        current = self.root
        for c in key:
            if c not in current.children:
                return None
            current = current.children[c]
        return current.value

token_trie = Trie()

# 10 character sequences
token_trie.insert("loop_index", "Loopindex")

# 9 character sequences
token_trie.insert("endstruct", "Endstruct")
token_trie.insert("otherwise", "Otherwise")

# 8 character sequences
token_trie.insert("constant", "Constant")
token_trie.insert("continue", "Continue")
token_trie.insert("endwhile", "Endwhile")
token_trie.insert("variadic", "Variadic")

# 7 character sequences
token_trie.insert("endcase", "Endcase")
token_trie.insert("endloop", "Endloop")
token_trie.insert("returns", "Returns")

# 6 character sequences
token_trie.insert("brings", "Brings")
token_trie.insert("endfor", "Endfor")
token_trie.insert("import", "Import")
token_trie.insert("return", "Return")
token_trie.insert("shadow", "Shadow")
token_trie.insert("spread", "Spread")
token_trie.insert("struct", "Struct")
token_trie.insert("unless", "Unless")

# 5 character sequences
token_trie.insert("break", "Break")
token_trie.insert("endfn", "Endfn")
token_trie.insert("endif", "Endif")
token_trie.insert("false", "Boolean", ChestnutBoolean(False))
token_trie.insert("outer", "Outer")
token_trie.insert("until", "Until")
token_trie.insert("while", "While")

# 4 character sequences
token_trie.insert("case", "Case")
token_trie.insert("elif", "Elif")
token_trie.insert("else", "Else")
token_trie.insert("loop", "Loop")
token_trie.insert("over", "Over")
token_trie.insert("then", "Then")
token_trie.insert("true", "Boolean", ChestnutBoolean(True))
token_trie.insert("when", "When")

# 3 character sequences
token_trie.insert("<<<", "BitwiseRotateLeft")
token_trie.insert(">>>", "BitwiseRotateRight")
token_trie.insert("and", "And")
token_trie.insert("for", "For")
token_trie.insert("let", "Let")
token_trie.insert("not", "Not")
token_trie.insert("null", "Null", CHESTNUT_NULL)
token_trie.insert("use", "Use")
    
# 2 character sequences
token_trie.insert("+=", "Addassign")
token_trie.insert("&&", "And")
token_trie.insert("as", "As")
token_trie.insert("~&", "BitwiseNand")
token_trie.insert("~|", "BitwiseNor")
token_trie.insert("<<", "BitwiseShiftLeft")
token_trie.insert(">>", "BitwiseShiftRight")
token_trie.insert("~^", "BitwiseXnor")
token_trie.insert("/=", "Divassign")
token_trie.insert("do", "Do")
token_trie.insert("==", "Eq")
token_trie.insert("**", "Exponent")
token_trie.insert("fn", "Fn")
token_trie.insert(">=", "Gte")
token_trie.insert("if", "If")
token_trie.insert("<=", "Lte")
token_trie.insert("%", "Modulo")
token_trie.insert("*=", "Mulassign")
token_trie.insert("!=", "Neq")
token_trie.insert("or", "Or")
token_trie.insert("||", "Or")
token_trie.insert("-=", "Subassign")

# 1 character sequences
token_trie.insert("&", "BitwiseAnd")
token_trie.insert("=", "Assignment")
token_trie.insert("+", "Addition")
token_trie.insert("~", "BitwiseNot")
token_trie.insert("|", "BitwiseOr")
token_trie.insert("^", "BitwiseXor")
token_trie.insert(":", "Colon")
token_trie.insert(",", "Comma")
token_trie.insert("/", "Division")
token_trie.insert("[", "LBrace")
token_trie.insert("(", "LParen")
token_trie.insert("<", "Lt")
token_trie.insert(">", "Gt")
token_trie.insert("*", "Multiplication")
token_trie.insert("!", "Not")
token_trie.insert(".", "Period")
token_trie.insert("]", "RBrace")
token_trie.insert(")", "RParen")
token_trie.insert("-", "Subtraction")
token_trie.insert(";", "Semicolon")

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

        for length in range(token_trie.max_token_length, 0, -1):
            if state.pos + length > len(input):
                continue

            potential_token_value = input[state.pos:state.pos + length]
            token_data: TokenData = token_trie.search(potential_token_value)
            
            if token_data is not None:
                if is_identifier(potential_token_value[0].lower()):
                    if is_token_match(input, state.pos, potential_token_value):
                        val = potential_token_value
                        if token_data.default_value is not None:
                            val = token_data.default_value
                        found_token = Token(token_data.token_type, val, start_line, start_column)
                        state.advance_column(length)
                        break
                else:
                    val = potential_token_value
                    if token_data.default_value is not None:
                        val = token_data.default_value
                    found_token = Token(token_data.token_type, val, start_line, start_column)
                    state.advance_column(length)
                    break
        if found_token:
            yield found_token
            continue

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
        elif input[state.pos] == '"' or input[state.pos] == "'" or input[state.pos] == '`':
            end_chr = input[state.pos]
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
                if char == end_chr and not is_escaped and interpolation_depth == 0:
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

