class UnaryOperationNode:
    def __init__(self, op, right):
        self.op = op
        self.right = right
    def __repr__(self):
        return f"UnaryOperationNode(<{self.op}>, <{self.right}>)"

class BinaryOperationNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return f"BinaryOperationNode(<{self.left}>, <{self.op}>, <{self.right}>)"

class ConstantStatementNode:
    def __init__(self, label, expression):
        self.label = label
        self.expression = expression
    
    def __repr__(self):
        return f"ConstantStatementNode(<{self.label}>, <{self.expression}>)"

class LetStatementNode:
    def __init__(self, label, expression):
        self.label = label
        self.expression = expression
    
    def __repr__(self):
        return f"LetStatementNode(<{self.label}>, <{self.expression}>)"

class ShadowStatementNode:
    def __init__(self, label, expression):
        self.label = label
        self.expression = expression

class PrintStatementNode:
    def __init__(self, expression):
        self.expression = expression
        
    def __repr__(self):
        return f"PrintStatementNode<{self.expression}>"

class IfStatementNode:
    def __init__(self, condition_expression, block_statements, elif_blocks, else_block):
        self.condition_expression = condition_expression
        self.block_statements = block_statements
        self.elif_blocks = elif_blocks
        self.else_block = else_block

    def __repr__(self):
        return f"IfStatementNode(<{self.condition_expression}>, <{self.block_statements}>, <{self.elif_blocks}>, <{self.else_block}>)"

class ElifStatementNode:
    def __init__(self, condition_expression, block_statements):
        self.condition_expression = condition_expression
        self.block_statements = block_statements

    def __repr__(self):
        return f"ElifStatementNode(<{self.condition_expression}>, <{self.block_statements}>)"

class ElseStatementNode:
    def __init__(self, block_statements):
        self.block_statements = block_statements

    def __repr__(self):
        return f"ElseStatementNode(<{self.block_statements}>)"

class FnStatementNode:
    def __init__(self, name, parameters, statements):
        self.name = name
        self.parameters = parameters
        self.statements = statements

    def __repr__(self):
        return f"FnStatementNode(<{self.name}>, <{self.parameters}>, <{self.statements}>)"

class AnonymousFnExpressionNode:
    def __init__(self, parameters, statements):
        self.parameters = parameters
        self.statements = statements

    def __repr__(self):
        return f"AnonymousFnExpressionNode(<{self.parameters}>, <{self.statements}>)"

class FnParameter:
    def __init__(self, name, paramtype, default_value=None, variadic=False):
        self.name = name
        self.paramtype = paramtype
        self.default_value = default_value
        self.variadic = variadic

    def __repr__(self):
        return f"FnParameter(<{self.name}>, <{self.paramtype}>, <{self.default_value}>, <{self.variadic}>)"

class CaseStatementNode:
    def __init__(self, subject, when_blocks, otherwise):
        self.subject = subject
        self.when_blocks = when_blocks
        self.otherwise = otherwise
    
    def __repr__(self):
        return f"CaseStatementNode(<{self.subject}>, <{self.when_blocks}>, <{self.otherwise}>)"

class WhenStatementNode:
    def __init__(self, conditions, statements):
        self.conditions = conditions
        self.statements = statements

    def __repr__(self):
        return f"WhenStatementNode(<{self.conditions}>, <{self.statements}>)"

class OtherwiseStatementNode:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"OtherwiseStatementNode(<{self.statements}>)"

class UntilStatementNode:
    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements

    def __repr__(self):
        return f"UntilStatementNode(<{self.condition}>, <{self.statements}>)"

class IterateStatementNode:
    def __init__(self, subject, identifier, statements):
        self.subject = subject
        self.identifier = identifier
        self.statements = statements

    def __repr__(self):
        return f"IterateStatementNode(<{self.subject}>, <{self.identifier}>, <{self.statements}>)"

class ListLiteralNode:
    def __init__(self, elements):
        self.elements = elements
    def __repr__(self):
        return f"ListLiteralNode({self.elements})"

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
        if token and token.label in ["Let", "Shadow", "Constant"]:
            return self.parse_let_statement()
        elif token and token.label == "Print":
            return self.parse_print_statement()
        elif token and token.label == "If":
            return self.parse_if_statement()
        elif token and token.label == "Fn":
            return self.parse_fn_statement()
        elif token and token.label == "Case":
            return self.parse_case_statement()
        elif token and token.label == "Until":
            return self.parse_until_statement()
        elif token and token.label == "Iterate":
            return self.parse_iterate_statement()
        elif token and token.label == "Return":
            return self.parse_return_statement()
        elif self.check_label("Identifier") and self.peek_next().label in [
                "Assignment", "Addassign", "Subassign", 
                "Mulassign", "Divassign"
            ]:
            return self.parse_assignment_statement()
        else:
            return ExpressionStatementNode(self.parse_expression())

    def parse_let_statement(self):
        let_token = self.consume()

        name_token = self.consume()
        if not name_token or name_token.label != "Identifier":
            raise SyntaxError(f"Expected identifier after 'let', got {name_token.label}")

        assignment_token = self.consume()
        if not assignment_token or assignment_token.label != "Assignment":
            raise SyntaxError(f"Expected '=' after identifier {name_token.data} in let statement")

        expression = self.parse_expression()

        if let_token.label == "Shadow":
            return ShadowStatementNode(name_token, expression)
        elif let_token.label == "Constant":
            return ConstantStatementNode(name_token, expression)
        return LetStatementNode(name_token, expression)

    def parse_print_statement(self):
        self.consume()

        if not self.check_label("LParen"):
            raise SyntaxError(f"Expected '(' in print statement at {self.get_line_and_column()}")
        
        self.consume()

        expression = self.parse_expression()

        if not self.check_label("RParen"):
            raise SyntaxError(f"Expected ')' in print statement at {self.get_line_and_column()}")
        
        self.consume()

        return PrintStatementNode(expression)

    def parse_if_statement(self):
        # Consume the if
        self.consume()

        condition_expression = self.parse_expression()

        if self.peek() and self.peek().label != "Then":
            raise SyntaxError("`then` missing after condition in if statement")

        # Consume then.
        self.consume()

        if_statements = []
        while self.peek() and not self.peek().label in ['Elif', 'Else', 'Endif']:
            if_statements.append(self.parse_statement())

        if self.peek() and not self.peek().label in ['Elif', 'Else', 'Endif']:
            raise SyntaxError("Expected elif, else, or endif after if statement")

        elif_blocks = []
        while self.peek() and self.peek().label == 'Elif':
            # Consume elif
            self.consume()
            
            condition_expression = self.parse_expression()

            if self.peek() and self.peek().label != "Then":
                raise SyntaxError("`then` missing after condition in elif statement")

            # Consume then
            self.consume()

            elif_statements = []
            while self.peek() and not self.peek().label in ['Elif', 'Else', 'Endif']:
                elif_statements.append(self.parse_statement())

            elif_blocks.append(ElifStatementNode(condition_expression, elif_statements))

        if self.peek() and not self.peek().label in ['Else', 'Endif']:
            raise SyntaxError("Expected else or endifin if statement")

        else_block = None
        if self.peek() and self.peek().label == "Else":
            # Consume else
            self.consume()
            
            else_statements = []
            while self.peek() and not self.peek().label == "Endif":
                else_statements.append(self.parse_statement())

            else_block = ElseStatementNode(else_statements)

        if self.peek() and self.peek().label != "Endif":
            raise SyntaxError("Expected endif in if statement")

        # Consume endif
        self.consume()

        return IfStatementNode(condition_expression, if_statements, elif_blocks, else_block)

    def parse_fn_statement(self):
        # Consume fn token
        self.consume()

        if self.peek() and self.peek().label != "Identifier":
            raise SyntaxError(f"Identifier expected after fn, got {self.peek().label}")

        name = self.consume()

        if self.peek() and self.peek().label != "LParen":
            raise SyntaxError(f"Expected '(' after fn, got {self.peek().label}")

        self.consume()

        parameters = []
        variadic_encountered = False
        optional_encountered = False
        while self.peek() and self.peek().label != "RParen":
            if self.peek() and self.peek().label == "Comma":
                self.consume()
                if self.peek().label == "RParen":
                    raise SyntaxError("Expected parameter in fn, got ')'")

            # Have we seen variadic before this parameter? Reject it.
            if variadic_encountered:
                raise SyntaxError("A variadic parameter must be the last parameter.")

            variadic = False
            if self.peek() and self.peek().label == "Variadic":
                variadic_encountered = True
                variadic = True
                self.consume() # Consume variadic

            if self.peek() and self.peek().label != "Identifier":
                raise SyntaxError(f"Expected identifier in fn, got {self.peek().label}")

            param = self.consume() # Consume parameter label.

            if self.peek() and self.peek().label != "Colon":
                raise SyntaxError(f"Expected ':' after identifier in fn, got {self.peek().label}")

            self.consume() # Consume colon.

            if self.peek() and self.peek().label != "Identifier":
                raise SyntaxError(f"Expected type identifier in param {param.data}, got {self.peek().label}")

            paramtype = self.consume()

            default_value = None
            # Default value parsing.
            if not self.check_label("Assignment") and optional_encountered and not variadic:
                raise SyntaxError(f"Required parameter received after optional parameter at line {param.line}, column {param.column}")

            if variadic and self.peek() and self.peek().label == "Assignment":
                raise SyntaxError(f"Variadic parameters cannot have default values, at line {param.line}, column {param.column}")

            if self.peek() and self.peek().label == "Assignment":
                self.consume() # Consume the =
                default_value = self.parse_expression()
                optional_encountered = True
            parameters.append(FnParameter(param, paramtype, default_value, variadic))

        if self.peek() and self.peek().label != "RParen":
            raise SyntaxError(f"Expected ')' after fn parameters, got {self.peek().label}")

        # Consume )
        self.consume()

        return_types = []
        if self.peek() and self.peek().label == "Returns":
            self.consume()

            if self.peek() and self.peek().label != "LParen" and self.peek().label != "Identifier":
                raise SyntaxError(f"Expected type identifier(s), got {self.peek().label}")

            if self.peek() and self.peek().label == "LParen":
                # Multiple return types.
                while self.peek() and self.peek().label != "RParen":
                    if self.peek() and self.peek().label == "Comma":
                        self.consume()

                    if self.peek() and self.peek().label != "Identifier":
                        raise SyntaxError(f"Expected type identifier, got {self.peek().label}")
                    return_types.append(self.consume())

                self.consume() # Consume RParen
            else:
                return_types.append(self.consume())

        statements = []
        while self.peek() and self.peek().label != "Endfn":
            statements.append(self.parse_statement())
        if not self.peek():
            raise SyntaxError(f"Unexpected end of input, expected endfn for fn {name.data}")
        self.consume()

        return FnStatementNode(name, parameters, statements)
    
    def get_line_and_column(self):
        return f"line {self.peek().line}, column {self.peek().column}"
    

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
            raise SyntaxError(f"Unexpected {self.peek().label}, expected endcase at {self.get_line_and_column()}")
        
        self.consume()

        return CaseStatementNode(subject, when_blocks, otherwise)
    
    def parse_until_statement(self):
        self.consume()

        condition = self.parse_expression()

        if self.peek() and self.peek().label != "Repeat":
            raise SyntaxError("Expected repeat after condition in until statement")

        self.consume()

        statements = []
        while self.peek() and self.peek().label != "Enduntil":
            statements.append(self.parse_statement())
        
        if self.peek() and self.peek().label != "Enduntil":
            raise SyntaxError("Unexpected end of input, unterminated until block")
        
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
            raise SyntaxError("Expected keyword with in iterate block")
        self.consume() # consume with.

        if not self.check_label("Identifier"):
            raise SyntaxError(f"Expected identifier after with, got {self.peek().label}")
        
        identifier = self.consume()
        statements = []
        while not self.check_label("Enditerate"):
            statements.append(self.parse_statement())

        if not self.check_label("Enditerate"):
            raise SyntaxError("Unexpected end of input, iterate block missing enditerate")
        self.consume()
        return IterateStatementNode(subject, identifier, statements)
    
    def parse_return_statement(self):
        self.consume()
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
            raise SyntaxError(f"Expected 'over' in use expression at {self.get_line_and_column()}")
        
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
        return self.parse_binary_operation(self.parse_logical_ands, ['Or', 'Nor', 'Xor', 'Xnor'])

    def parse_logical_ands(self):
        return self.parse_binary_operation(self.parse_relational, ['And', 'Nand'])

    def parse_relational(self):
        return self.parse_binary_operation(self.parse_additive, ["Gte", "Gt", "Eq", "Neq", "Lte", "Lt"])

    def parse_additive(self):
        return self.parse_binary_operation(self.parse_multiplicative, ['Addition', 'Subtraction'])

    def parse_multiplicative(self):
        return self.parse_binary_operation(self.parse_exponentiation, ['Multiplication', 'Division', 'Modulo'])

    def parse_exponentiation(self):
        left = self.parse_unary_spread()
        if self.peek() and self.peek().label == "Exponent":
            op = self.consume()
            right = self.parse_exponentiation()
            return BinaryOperationNode(left, op, right)
        return left

    def parse_unary_spread(self):
        return self.parse_unary_operation(self.parse_unary_not, "Spread")

    def parse_unary_not(self):
        return self.parse_unary_operation(self.parse_unary_negative, "Not")

    def parse_unary_negative(self):
        return self.parse_unary_operation(self.parse_primary, "Subtraction")

    def parse_fn_expression(self):
        # Consume fn token
        self.consume()

        if self.peek() and self.peek().label != "LParen":
            raise SyntaxError(f"Expected '(' after fn, got {self.peek().label}")

        self.consume()

        parameters = []
        variadic_encountered = False
        while self.peek() and self.peek().label != "RParen":
            if self.peek() and self.peek().label == "Comma":
                self.consume()
                if self.peek().label == "RParen":
                    raise SyntaxError("Expected parameter in fn, got ')'")

            # Have we seen variadic before this parameter? Reject it.
            if variadic_encountered:
                raise SyntaxError("A variadic parameter must be the last parameter.")

            variadic = False
            if self.peek() and self.peek().label == "Variadic":
                variadic_encountered = True
                variadic = True
                self.consume() # Consume variadic

            if self.peek() and self.peek().label != "Identifier":
                raise SyntaxError(f"Expected identifier in fn, got {self.peek().label}")

            param = self.consume()

            if self.peek() and self.peek().label != "Colon":
                raise SyntaxError(f"Expected ':' after identifier in fn, got {self.peek().label}")

            self.consume() # Consume colon.

            if self.peek() and self.peek().label != "Identifier":
                raise SyntaxError(f"Expected type identifier in param {param.data}, got {self.peek().label}")

            paramtype = self.consume()

            default_value = None
            # Default value parsing.
            if self.peek() and self.peek().label == "Assign":
                self.consume()

                default_value = self.parse_expression()
            parameters.append(FnParameter(param, paramtype, default_value, variadic))

        if self.peek() and self.peek().label != "RParen":
            raise SyntaxError(f"Expected ')' after fn parameters, got {self.peek().label}")

        # Consume )
        self.consume()

        return_types = []
        if self.peek() and self.peek().label == "Returns":
            self.consume()

            if self.peek() and self.peek().label != "LParen" and self.peek().label != "Identifier":
                raise SyntaxError(f"Expected type identifier(s), got {self.peek().label}")

            if self.peek() and self.peek().label == "LParen":
                # Multiple return types.
                while self.peek() and self.peek().label != "RParen":
                    if self.peek() and self.peek().label == "Comma":
                        self.consume()

                    if self.peek() and self.peek().label != "Identifier":
                        raise SyntaxError(f"Expected type identifier, got {self.peek().label}")
                    return_types.append(self.consume())

                self.consume() # Consume RParen
            else:
                return_types.append(self.consume())

        statements = []
        while self.peek() and self.peek().label != "Endfn":
            statements.append(self.parse_statement())
        if not self.peek():
            raise SyntaxError(f"Unexpected end of input, expected endfn at {self.get_line_and_column()}")
        self.consume()

        return AnonymousFnExpressionNode(parameters, statements)

    def parse_list_literal(self):
        self.consume() # Consume the left brace.

        elements = []
        
        if self.check_label("RBrace"):
            return ListLiteralNode(elements)

        elements.append(self.parse_expression())
        while self.check_label("Comma"):
            self.consume()
            if self.check_label("RBrace"):
                raise SyntaxError(f"Unexpected trailing comma in list at {self.get_line_and_column()}")
            elements.append(self.parse_expression())

        if not self.check_label("RBrace"):
            raise SyntaxError(f"Expect ']' at the end of a list literal, got {self.peek().label} at {self.get_line_and_column()}")

        self.consume() # Consume the right brace.
        return ListLiteralNode(elements)

    def parse_index_access(self, target):
        self.consume() # Consume [

        index = self.parse_expression()

        if not self.check_label("RBrace"):
            raise SyntaxError(f"Expected ']' at the end of index access expression, got {self.peek().label} at {self.get_line_and_column()}")

        self.consume() # Consume ]

        if self.check_labels(["Assignment", "Addassign", "Subassign", "Mulassign", "Divassign"]):
            op = self.consume() # Consume assignment symbol
            expression = self.parse_expression()
            return IndexAssignNode(target, index, op, expression)

        return IndexAccessNode(target, index)

    def parse_primary(self):
        token = self.peek()

        if token and token.label in ["Boolean", "Integer", "Float", "String", "Binary", "Hex", "Octal", "Null"]:
            return self.consume()
        
        elif token and token.label == "Fn":
            return self.parse_fn_expression()

        if token and token.label == "Identifier":
            identifier = self.consume()
            if self.check_label("LBrace"):
                return self.parse_index_access(identifier)

            if self.check_label("LParen"):
                self.consume()
                params = []
                while not self.check_label("RParen"):
                    if self.check_label("Comma"):
                        self.consume()
                        if not self.peek() or self.check_label("RParen"):
                            raise SyntaxError(f"Expected identifier after comma in function call to {identifier.data}")
                    params.append(self.parse_expression())
                if not self.check_label("RParen"):
                    raise SyntaxError(f"Unexpected end of input parsing arguments in {identifier.data}")
                self.consume()

                return CallStatementNode(identifier, params)
            else:
                return identifier
        elif self.check_label("LBrace"):
            return self.parse_list_literal()
        elif token and token.label == 'LParen':
            self.consume()
            expression_node = self.parse_expression()

            if self.peek() and self.peek().label == 'RParen':
                self.consume()
                return expression_node
            else:
                raise SyntaxError(f"Expected right parenthesis, got {self.peek().label}")
        else:
            raise SyntaxError(f"Unexpected token {token.label} at {self.get_line_and_column()}")
