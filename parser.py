from error import *
from supporting import *
from chestnut_type import *
from abc import ABC

class UnaryOperationNode:
    def __init__(self, op, right):
        self.op = op
        self.right = right
    def __repr__(self):
        return f"UnaryOperationNode(<{self.op}>, <{self.right}>)"

    def get_name(self):
        return op.data

class BinaryOperationNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinaryOperationNode(<{self.left}>, <{self.op}>, <{self.right}>)"

    def get_name(self):
        return self.op.data

class ConstantStatementNode:
    def __init__(self, label, expression, explicit_type=None):
        self.label = label
        self.expression = expression
        self.explicit_type = None
    
    def __repr__(self):
        return f"ConstantStatementNode(<{self.label}>, <{self.expression}>)"

    def get_name(self):
        return self.label.data

class SimpleTokenStatement:
    def __init__(self, token):
        self.token = token

    def gettype(self):
        return "SimpleTokenStatement"

    def __repr__(self):
        return f"{self.gettype()}(<{self.token}>)"

    def get_name(self):
        return self.token.data

class BreakStatementNode(SimpleTokenStatement):
    def gettype(self):
        return "BreakStatementNode"

    def get_name(self):
        return "break"

class ContinueStatementNode(SimpleTokenStatement):
    def gettype(self):
        return "ContinueStatementNode"

    def get_name(self):
        return "continue"

class LetStatementNode:
    def __init__(self, label, expression, explicit_type=None):
        self.label = label
        self.expression = expression
        self.explicit_type = explicit_type
    
    def __repr__(self):
        return f"LetStatementNode(<{self.label}>, <{self.expression}>)"

    def get_name(self):
        return self.label.data

class ShadowStatementNode:
    def __init__(self, label, expression, explicit_type=None):
        self.label = label
        self.expression = expression
        self.explicit_type = explicit_type

    def get_name(self):
        return self.label.data

class LoopindexExpressionNode():
    def __repr__(self):
        return "LoopindexExpressionNode"

    def get_name(self):
        return "loop_index"

class ImportStatementNode:
    def __init__(self, token, location, imports=None):
        self.token = token
        self.location = location
        self.imports = imports

    def get_name(self):
        return self.token.data

class IfStatementNode:
    def __init__(self, condition_expression, block_statements, elif_blocks, else_block):
        self.condition_expression = condition_expression
        self.block_statements = block_statements
        self.elif_blocks = elif_blocks
        self.else_block = else_block

    def __repr__(self):
        return f"IfStatementNode(<{self.condition_expression}>, <{self.block_statements}>, <{self.elif_blocks}>, <{self.else_block}>)"

    def get_name(self):
        return "if"

class ElifStatementNode:
    def __init__(self, condition_expression, block_statements):
        self.condition_expression = condition_expression
        self.block_statements = block_statements

    def __repr__(self):
        return f"ElifStatementNode(<{self.condition_expression}>, <{self.block_statements}>)"

    def get_name(self):
        return "elif"

class ElseStatementNode:
    def __init__(self, block_statements):
        self.block_statements = block_statements

    def __repr__(self):
        return f"ElseStatementNode(<{self.block_statements}>)"

    def get_name(self):
        return "else"

class BaseFn:
    def __init__(self, parameters, statements, return_types=None, brings=[]):
        self.parameters = parameters
        self.statements = statements
        self.return_types = return_types
        self.brings = brings

    def mangle(self, identifier=""):
        return f"{"_".join(list(map(lambda x: x.paramtype.data, self.parameters)))} {identifier}".strip()

    def __repr__(self):
        if hasattr(self, "name"):
            return f"{self.__name__}({self.parameters}, {self.statements}, {self.return_types}, {self.brings})"
        else:
            return f"({self.parameters}, {self.statements}, {self.return_types}, {self.brings})"

class FnStatementNode(BaseFn):
    def __init__(self, name, parameters, statements, return_types=None, brings=[]):
        super().__init__(parameters, statements, return_types, brings)
        self.name = name
        self.mangled_key = self.mangle(self.name.data)

    def __repr__(self):
        return f"FnStatementNode:\n\tName: <{self.name}>\n\tParam count<{len(self.parameters)}>\n\tStatement count: {len(self.statements)}\n\tReturn types: {self.return_types}\n\tBrings{self.brings})"

    def get_name(self):
        return self.name.data

class StructFnStatementNode(BaseFn):
    def __init__(self, target_struct, name, parameters, statements, return_types=None, brings=[]):
        super().__init__(parameters, statements, return_types, brings)
        self.target_struct = target_struct
        self.name = name
        self.mangled_key = self.mangle(self.target_struct.name.data + " " + self.name.data)

    def __repr__(self):
        return f"StructFnStatementNode(<{self.target_struct}>, <{self.name}>, <{self.parameters}>, <{self.statements}>, <{self.return_types}>, <{self.no_mangle}>)"

    def get_name(self):
        return self.name.data

class AnonymousFnExpressionNode(BaseFn):
    def __init__(self, parameters, statements, return_types=None, brings=[]):
        super().__init__(parameters, statements, return_types, brings)

    def get_name(self):
        return "fn"

class FnParameter:
    def __init__(self, name, paramtype, default_value=None, variadic=False):
        self.name = name
        self.paramtype = paramtype
        self.default_value = default_value
        self.variadic = variadic

    def __repr__(self):
        return f"FnParameter(<{self.name}>, <{self.paramtype}>, <{self.default_value}>, <{self.variadic}>)"

    def get_name(self):
        return self.name.data

class CaseStatementNode:
    def __init__(self, subject, when_blocks, otherwise):
        self.subject = subject
        self.when_blocks = when_blocks
        self.otherwise = otherwise
    
    def __repr__(self):
        return f"CaseStatementNode(<{self.subject}>, <{self.when_blocks}>, <{self.otherwise}>)"

    def get_name(self):
        return "case"

class WhenStatementNode:
    def __init__(self, conditions, statements):
        self.conditions = conditions
        self.statements = statements

    def __repr__(self):
        return f"WhenStatementNode(<{self.conditions}>, <{self.statements}>)"

    def get_name(self):
        return "when"

class OtherwiseStatementNode:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"OtherwiseStatementNode(<{self.statements}>)"

    def get_name(self):
        return "otherwise"

class UntilStatementNode:
    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements

    def __repr__(self):
        return f"UntilStatementNode(<{self.condition}>, <{self.statements}>)"

    def get_name(self):
        return "until"

class WhileStatementNode:
    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements

    def __repr__(self):
        return f"WhileStatementNode(<{self.condition}>, <{self.statements}>)"

    def get_name(self):
        return "while"

class IterateStatementNode:
    def __init__(self, subject, identifier, statements):
        self.subject = subject
        self.identifier = identifier
        self.statements = statements

    def __repr__(self):
        return f"IterateStatementNode(<{self.subject}>, <{self.identifier}>, <{self.statements}>)"

    def get_name(self):
        return "iterate"

class ListLiteralNode:
    def __init__(self, elements):
        self.elements = elements
    def __repr__(self):
        return f"ListLiteralNode({self.elements})"

    def get_name(self):
        return "List"

class TupleLiteralNode:
    def __init__(self, elements):
        self.elements = elements
    def __repr__(self):
        return f"TupleLiteralNode({self.elements})"

    def get_name(self):
        return "Tuple"

class IndexAccessNode:
    def __init__(self, target, index):
        self.target = target
        self.index = index

    def __repr__(self):
        return f"IndexAccessNode(<{self.target}>, <{self.index}>)"

class IndexAssignNode:
    def __init__(self, identifier, index, op, value):
        self.identifier = identifier
        self.index = index
        self.op = op
        self.value = value

    def __repr__(self):
        return f"IndexAssignNode(<{self.identifier}>, {self.index}, {self.op}, {self.value})"

class ReturnStatementNode:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"Return(<{self.expression}>)"

class AssignStatementNode:
    def __init__(self, identifier, op, expression):
        self.identifier = identifier
        self.op = op
        self.expression = expression

    def __repr__(self):
        return f"AssignStatementNode(<{self.identifier}>, <{self.op}>, <{self.expression}>)"

class UseExpressionNode():
    def __init__(self, left, right, condition):
        self.left = left
        self.right = right
        self.condition = condition
    def __repr__(self):
        return f"UseExpressionNode(<{self.left}>, <{self.right}>, <{self.condition}>)"

class CallStatementNode:
    def __init__(self, identifier, params):
        self.identifier = identifier
        self.params = params

    def __repr__(self):
        return f"CallStatementNode(<{self.identifier}>, <{self.params}>)"
        
class ExpressionStatementNode():
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"ExpressionStatementNode(<{self.expression}>)"

class StructDefinitionNode():
    def __init__(self, identifier, properties):
        self.identifier = identifier
        self.properties = properties

    def __repr__(self):
        return f"StructDefinitionNode(<{self.identifier}>, <{self.properties}>)"

    def get_name(self):
        return self.identifier.data

class StructPropertyNode():
    def __init__(self, identifier, value_type):
        self.identifier = identifier
        self.value_type = value_type

    def __repr__(self):
        return f"StructPropertyNode(<{self.identifier}>, <{self.value_type}>)"

class PropertyAccessNode():
    def __init__(self, identifier, property_identifier):
        self.identifier = identifier
        self.property_identifier = property_identifier

    def __repr__(self):
        return f"PropertyAccessNode(<{self.identifier}>, <{self.property_identifier}>)"

class PropertyAssignmentNode():
    def __init__(self, identifier, property_identifier, op, value_expression):
        self.identifier = identifier
        self.property_identifier = property_identifier
        self.op = op
        self.value_expression = value_expression

    def __repr__(self):
        return f"PropertyAssignmentNode(<{self.identifier}>, <{self.property_identifier}>, <{self.op}>, <{self.value_expression}>)"

class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.current = None
        self.next = None
        self.consume()

    def consume(self):
        token = self.current
        if self.next is None:
            self.current = next(self.tokens, None)
        else:
            self.current = self.next
        self.next = next(self.tokens, None)
        return token

    def peek(self):
        return self.current

    def peek_next(self):
        return self.next

    def parse_program(self):
        statements = []
        while self.peek():
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        token = self.peek()
        statement = None
        if token and token.label in ["Let", "Shadow", "Constant"]:
            statement = self.parse_let_statement()
        elif token and token.label == "Struct":
            statement = self.parse_struct_definition()
        elif token and token.label == "Import":
            statement = self.parse_import_statement()
        elif token and token.label == "If":
            statement = self.parse_if_statement()
        elif token and token.label == "Fn":
            statement = self.parse_fn_statement()
        elif token and token.label == "Case":
            statement = self.parse_case_statement()
        elif token and token.label == "While":
            statement = self.parse_while_statement()
        elif token and token.label == "Until":
            statement = self.parse_until_statement()
        elif token and token.label == "Iterate":
            statement = self.parse_iterate_statement()
        elif token and token.label == "Return":
            statement = self.parse_return_statement()
        elif token and token.label == "Break":
            statement = BreakStatementNode(self.consume())
        elif token and token.label == "Continue":
            statement = ContinueStatementNode(self.consume())
        elif self.check_label("Identifier") and self.peek_next().label in [
                "Assignment", "Addassign", "Subassign", 
                "Mulassign", "Divassign"
            ]:
            statement = self.parse_assignment_statement()
        else:
            statement = ExpressionStatementNode(self.parse_expression())
        if self.check_label("Semicolon"):
            self.consume()
        return statement

    def parse_let_statement(self):
        let_token = self.consume()
        name_token = None
        explicit_type = None
        if self.check_next_label("Comma"):
            if not self.check_label("Identifier"):
                raise SyntaxException("Missing identifier after start of tuple in let", self.peek())
            name_token = [self.consume()]
            while self.check_label("Comma"):
                self.consume() # Consume ,
                if not self.check_label("Identifier"):
                    raise SyntaxException("Missing identifier in tuple assignment via let", self.peek())
                name_token.append(self.consume())
        else:
            if not self.check_label("Identifier"):
                raise SyntaxException("Expected identifier in let statement", self.peek())
            name_token = self.consume()
            if self.check_label("Colon"):
                # Explicitly typed variable
                colon = self.consume()

                if not self.check_label("Identifier"):
                    raise SyntaxException(f"Expected type identifier after colon in let statement", self.peek())
                type_identifier = self.consume()

        assignment_token = self.consume()
        if not assignment_token or assignment_token.label != "Assignment":
            raise SyntaxException(f"Expected '=' after identifier {name_token.data} in let statement", self.peek())

        expression = self.parse_expression()

        if let_token.label == "Shadow":
            return ShadowStatementNode(name_token, expression, explicit_type)
        elif let_token.label == "Constant":
            return ConstantStatementNode(name_token, expression, explicit_type)
        return LetStatementNode(name_token, expression, explicit_type)

    def parse_struct_definition(self):
        self.consume()
        if not self.check_label("Identifier"):
            raise SyntaxException(f"Expected identifier after struct", self.peek())
        identifier = self.consume()

        properties = []
        while not self.check_label("Endstruct"):
            if not self.check_label("Identifier"):
                raise SyntaxException(f"Expected identifier for property, got {self.peek().label}", self.peek())
            property_identifier = self.consume()

            if not self.check_label("Colon"):
                raise SyntaxException(f"Expected colon and identifer after property name, got {self.peek().label}", self.peek())
            self.consume()

            if not self.check_label("Identifier"):
                raise SyntaxException(f"Expected identifier for property, got {self.peek().label}", self.peek())

            type_identifier = self.consume()

            properties.append(StructPropertyNode(property_identifier, type_identifier))
        if not self.check_label("Endstruct"):
            raise SyntaxException(f"Expected endstruct after struct definition", self.peek())

        self.consume()

        return StructDefinitionNode(identifier, properties)

    def parse_import_statement(self):
        keyword = self.consume()
        if not self.check_label("String"):
            raise SyntaxException("Expected string after import", self.peek())
        location = self.consume()
        imports = []
        if self.check_label("LParen"):
            self.consume()
            if not self.check_label("Identifier"):
                raise SyntaxException(f"Expected identifier, got {self.peek().label}", self.peek())
            imports.append(self.consume())
            while self.check_label("Comma"):
                self.consume()
                if not self.check_label("Identifier"):
                    raise SyntaxException(f"Expected identifier, got {self.peek().label}", self.peek())
                imports.append(self.consume())
            if not self.check_label("RParen"):
                raise SyntaxException(f"Expected right parenthesis to end imports list, got {self.peek().label}", self.peek())
            self.consume()

        return ImportStatementNode(keyword, location, imports)

    def parse_if_statement(self):
        # Consume the if
        self.consume()

        condition_expression = self.parse_expression()

        if not self.check_label("Then"):
            raise SyntaxException("`then` missing after condition in if statement", self.peek())

        # Consume then.
        self.consume()

        if_statements = []
        while not self.check_labels(['Elif', 'Else', 'Endif']):
            if_statements.append(self.parse_statement())

        if not self.check_labels(['Elif', 'Else', 'Endif']):
            raise SyntaxException("Expected elif, else, or endif after if statement", self.peek())

        elif_blocks = []
        while self.check_label('Elif'):
            # Consume elif
            self.consume()
            
            condition_expression = self.parse_expression()

            if not self.check_label("Then"):
                raise SyntaxException("`then` missing after condition in elif statement", self.peek())

            # Consume then
            self.consume()

            elif_statements = []
            while self.check_labels(['Elif', 'Else', 'Endif']):
                elif_statements.append(self.parse_statement())

            elif_blocks.append(ElifStatementNode(condition_expression, elif_statements))

        if not self.check_labels(['Else', 'Endif']):
            raise SyntaxException("Expected else or endifin if statement", self.peek())

        else_block = None
        if self.check_label("Else"):
            # Consume else
            self.consume()
            
            else_statements = []
            while not self.check_label("Endif"):
                else_statements.append(self.parse_statement())

            else_block = ElseStatementNode(else_statements)

        if not self.check_label("Endif"):
            raise SyntaxException("Expected endif in if statement", self.peek())

        # Consume endif
        self.consume()

        return IfStatementNode(condition_expression, if_statements, elif_blocks, else_block)

    def pull_params(self):
        self.consume() # Consume the (
        params = []

        if self.check_label("RParen"): # Empty params list.
            self.consume()
            return params

        variadic_encountered = False
        optional_encountered = False
        variadic = False
        default_value = None

        if self.check_label("Variadic"):
            self.consume()
            variadic = True
            variadic_encountered = True

        # Parse parameter identifier
        if not self.check_label("Identifier"):
            raise SyntaxException("Expected identifier in function parameters", self.peek())
        identifier = self.consume() # Consume identifier

        # Parse type delimiter
        if not self.check_label("Colon"):
            raise SyntaxException("Expected colon after parameter identifier", self.peek())
        self.consume()

        # Parse type identifier
        if not self.check_label("Identifier"):
            raise SyntaxException("Expected type identifier in function parameters", self.peek())
        param_type = self.consume()

        # Check if we need to parse default value assignment
        if self.check_label("Assignment"):
            self.consume() # Consume =
            optional_encountered = True
            default_value = self.parse_expression()
        params.append(FnParameter(identifier, param_type, default_value, variadic))

        while self.check_label("Comma"):
            # Reset
            variadic = False
            default_value = None
            identifier = None
            param_type = None

            self.consume() # Consume ,

            if self.check_label("Variadic"):
                self.consume()
                variadic = True
                variadic_encountered = True

            # Variadic parameter received prior to this.
            if variadic_encountered and not variadic:
                raise SyntaxException("Variadic parameters must appear as the last parameter", self.peek())

            # Parse parameter identifier
            if not self.check_label("Identifier"):
                raise SyntaxException("Expected identifier in function parameters", self.peek())
            identifier = self.consume() # Consume identifier

            # Parse type delimiter
            if not self.check_label("Colon"):
                raise SyntaxException("Expected colon after parameter identifier", self.peek())
            self.consume()

            # Parse type identifier
            if not self.check_label("Identifier"):
                raise SyntaxException("Expected type identifier in function parameters", self.peek())
            param_type = self.consume()

            # Check if we need to parse default value assignment
            if self.check_label("Assignment"):
                if variadic:
                    raise SyntaxException("Variadic parameters may not have default values", self.peek())
                self.consume() # Consume =
                optional_encountered = True
                default_value = self.parse_expression()
            else:
                # Did we see an optional argument before this required argument?
                if optional_encountered and not variadic:
                    raise SyntaxException("Optional parameters must appear after required parameters", self.peek())
            params.append(FnParameter(identifier, param_type, default_value, variadic))
        if not self.check_label("RParen"):
            raise SyntaxException("Expected ')' after parameter list", self.peek())
        self.consume() # Consume )
        return params

    def parse_brings(self):
        brings = []
        if self.check_label("Brings"):
            self.consume() # Consume Brings
            if not self.check_label("LParen"):
                raise SyntaxException("Expected '(' after brings token", self.peek())
            self.consume() # Consume (
            if not self.check_label("Identifier"):
                raise SyntaxException("Expected identifier in brings", self.peek())
            brings.append(self.consume())
            while self.check_label("Comma"):
                self.consume() # Consume ,
                if not self.check_label("Identifier"):
                    raise SyntaxException("Expected identifier in brings", self.peek())
                brings.append(self.consume())
            if not self.check_label("RParen"):
                raise SyntaxException("Expected ')' after brings identifiers", self.peek())
            self.consume() # Consume )
        return brings

    def parse_returns(self):
        return_types = []
        if self.check_label("Returns"):
            self.consume() # Consume Returns

            if not self.check_labels(["LParen", "Identifier"]):
                raise SyntaxException(f"Expected type identifier(s), got {self.peek().label}", self.peek())

            if self.check_label("LParen"):
                self.consume() # Consume LParen
                # Multiple return types.
                while not self.check_label("RParen"):
                    if self.check_label("Comma"):
                        self.consume()

                    if not self.check_label("Identifier"):
                        raise SyntaxException(f"Expected type identifier, got {self.peek().label}", self.peek())
                    return_types.append(self.consume())

                self.consume() # Consume RParen
            else:
                return_types.append(self.consume())
        return return_types

    def parse_fn_statement(self):
        # Consume fn token
        self.consume()
        struct_params = None
        if self.check_label("LParen"):
            struct_params = self.pull_params()

        name = None
        if self.check_label("Identifier"):
            name = self.consume()

        fn_params = struct_params
        if self.check_label("LParen"):
            fn_params = self.pull_params()

        if struct_params is not None and struct_params != fn_params:
            if len(struct_params) > 1:
                raise SyntaxException("Struct methods should only contain one identifier with type", struct_params[1])
            if struct_params[0].variadic:
                raise SyntaxException("A struct method parameter cannot be variadic", struct_params[0])
            if struct_params[0].default_value is not None:
                raise SyntaxException("A struct method parameter may not have a default value", struct_params[0])

        brings = self.parse_brings()

        return_types = self.parse_returns()

        statements = []

        while not self.check_label("Endfn"):
            statements.append(self.parse_statement())

        if not self.peek():
            raise SyntaxException(f"Unexpected end of input, expected endfn for fn {name.data}", self.peek())
        self.consume() # Consume Endfn

        if struct_params is not None and struct_params != fn_params:
            if name is None:
                raise SyntaxException("Expected function identifier for struct method", struct_params)
            return StructFnStatementNode(struct_params[0], name, fn_params, statements, return_types, brings)

        if name is None:
            raise SyntaxException("Validly defined anonymous function not associated to label will be unrefencable", self.peek())

        return FnStatementNode(name, fn_params, statements, return_types, brings)
    
    def parse_case_statement(self):
        self.consume()

        subject = self.parse_expression()

        when_blocks = []
        stacking_conditions = []
        while self.check_label("When"):
            self.consume()
            condition = self.parse_expression()
            stacking_conditions.append(condition)

            if self.check_label("When"):
                continue

            statements = []
            while not self.check_labels(["When", "Otherwise", "Endcase"]):
                statements.append(self.parse_statement())
            when_blocks.append(WhenStatementNode(stacking_conditions, statements))
            stacking_conditions = []
        
        otherwise = None
        if self.check_label("Otherwise"):
            self.consume()
            statements = []
            while not self.check_label("Endcase"):
                statements.append(self.parse_statement())
            otherwise = OtherwiseStatementNode(statements)
        if not self.check_label("Endcase"):
            raise SyntaxException(f"Unexpected {self.peek().label}, expected endcase", self.peek())
        
        self.consume()

        return CaseStatementNode(subject, when_blocks, otherwise)
    
    def parse_while_statement(self):
        self.consume()

        condition = self.parse_expression()

        if not self.check_label("Repeat"):
            raise SyntaxException("Expected repeat after condition in until statement", self.peek())

        self.consume()

        statements = []
        while not self.check_label("Endwhile"):
            statements.append(self.parse_statement())
        
        if not self.check_label("Endwhile"):
            raise SyntaxException("Unexpected end of input, unterminated while block", self.peek())
        
        self.consume()

        return WhileStatementNode(condition, statements)

    def parse_until_statement(self):
        self.consume()

        condition = self.parse_expression()

        if self.peek() and self.peek().label != "Repeat":
            raise SyntaxException("Expected repeat after condition in until statement", self.peek())

        self.consume()

        statements = []
        while self.peek() and self.peek().label != "Enduntil":
            statements.append(self.parse_statement())
        
        if self.peek() and self.peek().label != "Enduntil":
            raise SyntaxException("Unexpected end of input, unterminated until block", self.peek())
        
        self.consume()

        return UntilStatementNode(condition, statements)
    
    def check_label(self, label):
        return self.peek() and self.peek().label == label
   
    def check_labels(self, labels):
        return self.peek() and self.peek().label in labels

    def check_next_label(self, label):
        return self.peek_next() and self.peek_next().label == label

    def parse_iterate_statement(self):
        self.consume() # consume iterate

        subject = self.parse_expression()

        if not self.check_label("With"):
            raise SyntaxException("Expected keyword with in iterate block", self.peek())
        self.consume() # consume with.

        if not self.check_label("Identifier"):
            raise SyntaxException(f"Expected identifier after with, got {self.peek().label}", self.peek())
        
        identifier = self.consume()
        statements = []
        while not self.check_label("Enditerate"):
            statements.append(self.parse_statement())

        if not self.check_label("Enditerate"):
            raise SyntaxException("Unexpected end of input, iterate block missing enditerate", self.peek())
        self.consume()
        return IterateStatementNode(subject, identifier, statements)
    
    def parse_return_statement(self):
        self.consume() # Consume return
        return ReturnStatementNode(self.parse_expression())

    def parse_assignment_statement(self):
        identifier = self.consume()
        op = self.consume() # Consume the Assign operator.
        expression = self.parse_expression()
        return AssignStatementNode(identifier, op, expression)
    
    def parse_expression(self):
        return self.parse_ternary()
 
    def parse_ternary(self):
        if self.check_label("Use"):
            return self.parse_use_expression()
        return self.parse_logical_ors()

    def parse_use_expression(self):
        self.consume() # Consume Use

        val1 = None
        if self.peek().label == "Use":
            val1 = self.parse_use_expression()
        else:
            val1 = self.parse_logical_ors()

        if not self.check_label("Over"):
            raise SyntaxException(f"Expected 'over' in use expression", self.peek())
        
        self.consume() # Consume Over

        val2 = None
        if self.peek().label == "Use":
            val2 = self.parse_use_expression()
        else:
            val2 = self.parse_logical_ors()

        condition = None
        # This portion is optional because we can do `use x over y` as a syntax for defaulting falsey values
        if self.check_label("Unless"):
            self.consume() # Consume Unless
            condition = self.parse_logical_ors()
        
        return UseExpressionNode(val1, val2, condition)
    
    def parse_binary_operation(self, next_fn, labels=[]):
        left = next_fn()
        while self.peek() and self.peek().label in labels:
            op = self.consume()
            right = next_fn()
            left = BinaryOperationNode(left, op, right)
        return left
    
    def parse_unary_operation(self, next_fn, label):
        if self.peek() and self.peek().label == label:
            op = self.consume()
            right = self.parse_unary_operation(next_fn, label)
            return UnaryOperationNode(op, right)
        return next_fn()

    def parse_logical_ors(self):
        return self.parse_binary_operation(self.parse_logical_ands, ['Or', 'BitwiseOr', 'BitwiseNor', 'BitwiseXor', 'BitwiseXnor', 'BitwiseShiftLeft', 'BitwiseShiftRight', 'BitwiseRotateLeft', 'BitwiseRotateRight'])

    def parse_logical_ands(self):
        return self.parse_binary_operation(self.parse_relational, ['And', "BitwiseAnd", "BitwiseNand"])

    def parse_relational(self):
        return self.parse_binary_operation(self.parse_additive, ["Gte", "Gt", "Eq", "Neq", "Lte", "Lt"])

    def parse_additive(self):
        return self.parse_binary_operation(self.parse_multiplicative, ['Addition', 'Subtraction'])

    def parse_multiplicative(self):
        return self.parse_binary_operation(self.parse_exponentiation, ['Multiplication', 'Division', 'Modulo'])

    def parse_exponentiation(self):
        left = self.parse_unary_outer()
        if self.peek() and self.peek().label == "Exponent":
            op = self.consume()
            right = self.parse_exponentiation()
            return BinaryOperationNode(left, op, right)
        return left

    def parse_unary_outer(self):
        return self.parse_unary_operation(self.parse_unary_spread, "Outer")

    def parse_unary_spread(self):
        return self.parse_unary_operation(self.parse_unary_not, "Spread")

    def parse_unary_not(self):
        return self.parse_unary_operation(self.parse_unary_bitwisenot, "Not")
    
    def parse_unary_bitwisenot(self):
        return self.parse_unary_operation(self.parse_unary_negative, "BitwiseNot")

    def parse_unary_negative(self):
        return self.parse_unary_operation(self.parse_postfix_expression, "Subtraction")

    def parse_fn_expression(self):
        # Consume fn token
        self.consume()

        if self.peek() and self.peek().label != "LParen":
            raise SyntaxException(f"Expected '(' after fn, got {self.peek().label}", self.peek())

        parameters = self.pull_params()

        brings = self.parse_brings()

        return_types = self.parse_returns()

        statements = []
        while self.peek() and self.peek().label != "Endfn":
            statements.append(self.parse_statement())
        if not self.peek():
            raise SyntaxException(f"Unexpected end of input, expected endfn", self.peek())
        self.consume()

        return AnonymousFnExpressionNode(parameters, statements, return_types, brings)

    def parse_tuple_literal(self):
        elements = []
        if self.check_label("RParen"):
            return TupleLiteralNode(tuple(elements))
        elements.append(self.parse_expression())
        while self.check_label("Comma"):
            self.consume()
            if self.check_label("RParen"):
                raise SyntaxException(f"Unexpected trailing comma in tuple", self.peek())
            elements.append(self.parse_expression())
        if not self.check_label("RParen"):
            raise SyntaxException(f"Expected ')' at the end of a tuple, got {self.peek().label}", self.peek())
        self.consume()
        return TupleLiteralNode(tuple(elements))

    def parse_list_literal(self):
        self.consume() # Consume the left brace.

        elements = []
        if self.check_label("RBrace"):
            self.consume()
            return ListLiteralNode(elements)

        elements.append(self.parse_expression())
        while self.check_label("Comma"):
            self.consume()
            if self.check_label("RBrace"):
                raise SyntaxException(f"Unexpected trailing comma in list", self.peek())
            elements.append(self.parse_expression())

        if not self.check_label("RBrace"):
            raise SyntaxException(f"Expect ']' at the end of a list literal, got {self.peek().label}", self.peek())

        self.consume() # Consume the right brace.
        return ListLiteralNode(elements)

    def parse_index_access(self, target):
        self.consume() # Consume [

        index = self.parse_expression()

        if not self.check_label("RBrace"):
            raise SyntaxException(f"Expected ']' at the end of index access expression, got {self.peek().label}", self.peek())

        self.consume() # Consume ]

        if self.check_labels(["Assignment", "Addassign", "Subassign", "Mulassign", "Divassign"]):
            op = self.consume() # Consume assignment symbol
            expression = self.parse_expression()
            return IndexAssignNode(target, index, op, expression)

        return IndexAccessNode(target, index)

    def parse_property_access(self, identifier):
        self.consume() # Consume period

        if not self.check_label("Identifier"):
            raise SyntaxException(f"Expected identifier after period for property access", self.peek())

        property_identifier = self.consume() # Consume property label.

        if not self.check_labels(["Assignment", "Addassign", "Subassign", "Divassign", "Mulassign"]):
            return PropertyAccessNode(identifier, property_identifier)

        op = self.consume() # Consume operator

        value_expression = self.parse_expression()

        return PropertyAssignmentNode(identifier, property_identifier, op, value_expression)

    def parse_loopindex(self):
        self.consume() # `Consume the Loopindex
        return LoopindexExpressionNode()

    def parse_readline(self):
        self.consume()
        if not self.check_label("LParen"):
            raise SyntaxException(f"Expected '(' in readline call, get {self.peek().label}", self.peek())
        self.consume()
        if not self.check_label("RParen"):
            raise SyntaxException(f"Expected '(' in readline call, get {self.peek().label}", self.peek())
        self.consume()
        return ReadlineExpressionNode()

    def parse_postfix_expression(self):
        left = self.parse_primary()
     
        while self.check_labels(["LBrace", "Period", "LParen"]) and not self.check_label("Semicolon"):
            if self.check_label("LBrace"):
                left = self.parse_index_access(left)
            elif self.check_label("Period"):
                left = self.parse_property_access(left)
            elif self.check_label("LParen"):
                self.consume() # Consume (
                params = []
                if self.check_label("RParen"):
                    self.consume() # Consume )
                    left = CallStatementNode(left, params)
                    continue
                params.append(self.parse_expression()) # Consume first
                while self.check_label("Comma"):
                    self.consume() # Consume ,
                    if self.check_label("RParen"):
                        raise SyntaxExpression("Expected identifier after comma in call", self.peek())
                    params.append(self.parse_expression())
                if not self.check_label("RParen"):
                    raise SyntaxExpression("Expected ')' in inline function call", self.peek())
                self.consume() # Consume ')'
                left = CallStatementNode(left, params)
                continue
        if self.check_label("Semicolon"):
            self.consume()
        return left

    def parse_paren_expression(self):
        self.consume() # Consume (
        if self.check_label("RParen"):
            self.consume()
            return TupleLiteralNode(tuple([]))
        first_expression = self.parse_expression()
        if self.check_label("Comma"):
            expressions = [first_expression]
            while self.check_label("Comma"):
                self.consume()
                if self.check_label("RParen"):
                    raise SyntaxException("Expected identifer in tuple after comma, got ')'", self.peek())
                expressions.append(self.parse_expression())
            if not self.check_label("RParen"):
                raise SyntaxException("Expected ')' at the end of a tuple", self.peek())
            self.consume() # Consume )
            return TupleLiteralNode(tuple(expressions))
        else:
            if self.check_label('RParen'):
                self.consume() # Consume )
                return first_expression
            else:
                raise SyntaxException(f"Expected right parenthesis, got {self.peek().label}", self.peek())

    def parse_primary(self):
        token = self.peek()

        if self.check_label("Boolean"):
            return ChestnutBoolean(self.consume())
        elif self.check_labels(["Integer", "Binary", "Hex", "Octal"]):
            return ChestnutInteger(self.consume())
        elif self.check_label("Float"):
            return ChestnutFloat(self.consume())
        elif self.check_label("String"):
            return ChestnutString(self.consume())
        elif self.check_label("Null"):
            return ChestnutNull(self.consume())

        elif token and token.label == "Fn":
            return self.parse_fn_expression()
        elif token and token.label == "Loopindex":
            return self.parse_loopindex()
        elif self.check_label("Identifier"):
            identifier = self.consume()

            if self.check_label("LParen"):
                self.consume()
                params = []
                while not self.check_label("RParen"):
                    if self.check_label("Comma"):
                        self.consume()
                        if not self.peek() or self.check_label("RParen"):
                            raise SyntaxException(f"Expected identifier after comma in function call to {identifier.data}", self.peek())
                    params.append(self.parse_expression())
                if not self.check_label("RParen"):
                    raise SyntaxException(f"Unexpected end of input parsing arguments in {identifier.data}", self.peek())
                self.consume()

                return CallStatementNode(identifier, params)
            else:
                return identifier
        elif self.check_label("LBrace"):
            return self.parse_list_literal()
        elif self.check_label('LParen'):
            return self.parse_paren_expression()
        else:
            raise SyntaxException(f"Unexpected token {token.label}", self.peek())
