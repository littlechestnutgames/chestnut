from parser import (
    AnonymousFnExpressionNode,
    AssignStatementNode,
    BinaryOperationNode,
    CallStatementNode,
    CaseStatementNode,
    ConstantStatementNode,
    ExpressionStatementNode,
    FnStatementNode,
    IndexAccessNode,
    IndexAssignNode,
    LetStatementNode,
    ListLiteralNode,
    IfStatementNode,
    IterateStatementNode,
    UnaryOperationNode,
    UntilStatementNode,
    UseExpressionNode,
    PrintStatementNode,
    ReturnStatementNode,
    ShadowStatementNode
)
from lexer import Token
from math import floor

class Function:
    def __init__(self, statement, scopes):
        self.statement = statement
        self.scopes = scopes[:]

    def reconcile_parameters(self, evaluator, call_parameters):
        statement = self.statement
        name = None
        if isinstance(statement, FnStatementNode):
            name = statement.name.data
        elif isinstance(statement, AnonymousFnExpressionNode):
            name = self.name

        required_count = 0
        has_variadic = False
        for param in statement.parameters:
            if param.default_value is None and not param.variadic:
                required_count += 1
            if param.variadic:
                has_variadic = True

        if (len(call_parameters) < required_count) or (not has_variadic and len(call_parameters) > len(statement.parameters)):
            raise Exception(f"Required number of parameters for `{name}` is {required_count}, got {len(call_parameters)}")

        evaluated_args = [evaluator.evaluate(param) for param in call_parameters]

        values = {}
        arg_index = 0
        for param in statement.parameters:
            param_name = param.name.data
            if param.variadic:
                # Variadic takes the remaining arguments.
                values[param_name] = evaluated_args[arg_index:]
                break
            elif arg_index < len(evaluated_args):
                values[param_name] = evaluated_args[arg_index]
                arg_index += 1
            elif param.default_value is not None:
                values[param_name] = evaluator.evaluate(param.default_value)

        return values
    def __repr__(self):
        return f"Function(<{self.statement}>, <{self.scopes}>)"

class AnonymousFunction(Function):
    def __init__(self, statement, scopes, name=None):
        super().__init__(statement, scopes)
        self.name = name

class ReturnValue(BaseException):
    def __init__(self, value):
        self.value = value

class Evaluator:
    def __init__(self):
        self.scopes = [{}]

    def push_scope(self, scope={}):
        self.scopes.append({})

    def pop_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()
        else:
            raise Exception("Cannot pop the global scope")

    def find_first_scope_containing(self, var_name):
        for scope in reversed(self.scopes):
            if var_name in scope:
                return scope
        return None

    def exists_in_any_scope(self, var_name):
        return self.exists_in_current_scope(var_name) or self.exists_in_parent_scope(var_name)

    def exists_in_current_scope(self, var_name):
        return var_name in self.scopes[-1]

    def exists_in_parent_scope(self, var_name):
        for scope in reversed(self.scopes[:-1]):
            if var_name in scope:
                return True
        return False

    def current_scope(self):
        return self.scopes[-1]
    
    def constant_exists(self, label):
        return self.exists_in_any_scope(f"constant {label}")

    def evaluate(self, node):
        if isinstance(node, PrintStatementNode):
            node_data = self.evaluate(node.expression)
            print(node_data)
        elif isinstance(node, Token) and node.label == "Null":
            return None
        elif isinstance(node, Token) and node.label == "Hex":
            return hex(node.data)
        elif isinstance(node, Token) and node.label == "Binary":
            return bin(node.data)
        elif isinstance(node, Token) and node.label == "Octal":
            return oct(node.data)
        elif isinstance(node, Token) and node.label in ["Integer", "Boolean", "Float", "String"]:
            return node.data
        elif isinstance(node, ListLiteralNode):
            elems = []
            for elem in node.elements:
                elems.append(self.evaluate(elem))
            return elems
        elif isinstance(node, IndexAccessNode):
            index = self.evaluate(node.index)
            label = node.target.data
            scope = self.find_first_scope_containing(label)
            if scope is None:
                raise Exception(f"Illegal index access in undefined identifier `{label}` at line {node.target.line}, column {node.target.column}")
            value = scope[label]
            if index == -1:
                index = len(value)-1
            if index > len(value)-1 or index < -1:
                raise Exception(f"Index out of bounds")
            return value[index]

        elif isinstance(node, ExpressionStatementNode):
            return self.evaluate(node.expression)
        elif isinstance(node, ReturnStatementNode):
            return_value = None
            if node.expression:
                return_value = self.evaluate(node.expression)
            raise ReturnValue(return_value)
        elif isinstance(node, ConstantStatementNode):
            label = node.label.data

            if self.constant_exists(label):
                raise Exception(f"Cannot redeclare constant `{label}` at line {node.label.line}, column {node.label.column}")

            if self.exists_in_any_scope(label):
                raise Exception(f"`{label}` is already declared in this scope at line {node.label.line}, column {node.label.column}")

            expression = self.evaluate(node.expression)

            self.current_scope()[f"constant {label}"] = expression

            return 1

        elif isinstance(node, LetStatementNode):
            label = node.label.data

            if self.constant_exists(label):
                raise Exception(f"Cannot redeclare constant `{label}` at line {node.label.line}, column {node.label.column}")

            if self.exists_in_any_scope(label):
                raise Exception(f"Cannot redeclare {label} in this scope at line {node.label.line}, column {node.label.column}")

            expression = self.evaluate(node.expression)

            self.current_scope()[label] = expression

            return 1

        elif isinstance(node, ShadowStatementNode):
            label = node.label.data

            if self.constant_exists(label):
                raise Exception(f"Cannot shadow constant `{label}` at line {node.label.line}, column {node.label.column}")

            if not self.exists_in_any_scope(label):
                raise Exception(f"{label} is not declared in any scope at line {node.label.line}, column {node.label.column}")

            expression = self.evaluate(node.expression)

            self.current_scope()[label] = expression

            return 1

        elif isinstance(node, FnStatementNode):
            func_object = Function(node, self.scopes)
            if self.constant_exists(node.name.data):
                raise Exception(f"Function definition for `{node.name.data}` conflicts with a constant at line {node.name.line}, column {node.name.column}")
            if self.exists_in_any_scope(node.name.data):
                raise Exception(f"{node.name.data} is already defined in the current scope, line {node.name.line}, column {node.name.column}")
            self.current_scope()[node.name.data] = func_object

            return 1

        elif isinstance(node, AnonymousFnExpressionNode):
            return AnonymousFunction(node, self.scopes)

        elif isinstance(node, CallStatementNode):
            identifier = node.identifier.data

            if not self.exists_in_any_scope(identifier) and not self.exists_in_any_scope(f"constant {identifier}"):
                # The function was found neither in non-constant or constant storage.
                raise Exception(f"Call to undefined function `{identifier}`")

            func_scope = self.find_first_scope_containing(identifier)
            func = None
            # Check if the scope was found and assign from the function inside.
            if func_scope:
                func = func_scope[identifier]

            if func_scope is None:
                # Non-constant lookup failed. Look for it as a constant.
                func_scope = self.find_first_scope_containing(f"constant {identifier}")

                if func_scope is None:
                    # Scope changed and now there is no identifier present.
                    raise Exception(f"Call to undefined function {identifier}")

                # We found a constant function, save the function reference.
                func = func_scope["constant " + identifier]

            if not isinstance(func, Function) and not isinstance(func, AnonymousFunction):
                # Block function calls to other stored data.
                raise Exception(f"Call to non-function `{identifier}` at line {node.identifier.line}, column {node.identifier.column}")

            fn = func.statement

            original_scopes_length = len(self.scopes)

            # Push scope clones into the scope stack.
            for scope in func.scopes:
                self.push_scope(scope)

                # Push our function's local scope onto the scope stack.
                self.push_scope()

                # Process parameters
                params = func.reconcile_parameters(self, node.params)
                for p in func.statement.parameters:
                    self.current_scope()[p.name.data] = params[p.name.data]
                for s in func.statement.statements:
                    try:
                        self.evaluate(s)
                    except ReturnValue as val:
                        return val
                # Return to our origin scopes count.
                while len(self.scopes) > original_scopes_length:
                    self.pop_scope()
            return False

        elif isinstance(node, Token) and node .label == "Identifier":
            label = node.data

            if self.constant_exists(label):
                label = f"constant {label}"
            stored_scope = self.find_first_scope_containing(label)
            if stored_scope is None:
                raise Exception(f"Couldn't find symbol {label} at line {node.line}, column {node.column}")

            return stored_scope[label]

        elif isinstance(node, IfStatementNode):
            if self.evaluate(node.condition_expression):
                self.push_scope()
                for statement in node.block_statements:
                    self.evaluate(statement)
                self.pop_scope()
                return
            for elif_block in node.elif_blocks:
                if self.evaluate(elif_block.condition_expression):
                    self.push_scope()
                    for statement in elif_block.statements:
                        self.evaluate(statement)
                    self.pop_scope()
                    return
            if node.else_block:
                self.push_scope()
                for statement in node.else_block:
                    self.evaluate(statement)
                self.pop_scope()
            return

        elif isinstance(node, CaseStatementNode):
            subject = self.evaluate(node.subject)
            for when_block in node.when_blocks:
                valid = False
                for condition in when_block.conditions:
                    valid = valid or subject == self.evaluate(condition)
                    if valid:
                        break
                if valid:
                    self.push_scope()
                    for statement in when_block.statements:
                        self.evaluate(statement)
                    self.pop_scope()
                    return
            if node.otherwise:
                self.push_scope()
                for statement in node.otherwise.statements:
                    self.evaluate(statement)
                self.pop_scope()
            return
            

        elif isinstance(node, AssignStatementNode):
            label = node.identifier.data

            if self.constant_exists(label):
                raise Exception(f"Cannot assign to constant `{label}` at line {node.identifier.line}, column {node.identifier.column}")

            if not self.exists_in_any_scope(node.identifier.data):
                raise Exception(f"Undeclared identifier {label} at line {node.identifier.line}, column {node.identifier.column}")

            scope = self.find_first_scope_containing(label)
            if isinstance(node, AnonymousFunction):
                node.name = label
            expression = self.evaluate(node.expression)

            op = node.op

            if op.label == "Assignment":
                scope[label] = expression
            elif op.label == "Addassign":
                scope[label] = scope[label] + expression
            elif op.label == "Subassign":
                scope[label] = scope[label] - expression
            elif op.label == "Mulassign":
                scope[label] = scope[label] * expression
            elif op.label == "Divassign":
                scope[label] = scope[label] / expression
            else:
                return 0
            return 1

        elif isinstance(node, IterateStatementNode):
            subject = self.evaluate(node.subject)
            identifier = node.identifier
            statements = node.statements
            parent_scope = self.current_scope();
            for elem in subject:
                self.push_scope()
                self.current_scope()[identifier.data] = elem
                for statement in statements:
                    self.evaluate(statement)
                self.pop_scope()

        elif isinstance(node, UntilStatementNode):
            while not self.evaluate(node.condition):
                self.push_scope()
                for statement in node.statements:
                    self.evaluate(statement)
                self.pop_scope()

        elif isinstance(node, UseExpressionNode):
            if not node.condition is None:
                if self.evaluate(node.condition):
                    return self.evaluate(node.right)
                return self.evaluate(node.left)
            else:
                left = self.evaluate(node.left)
                if left is None:
                    return self.evaluate(node.right)
                return left

        elif isinstance(node, BinaryOperationNode):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            op = node.op

            value = None
            match op.label:
                case "Eq":
                    value = left == right
                case "Neq":
                    value = left != right
                case "Lte":
                    value = left <= right
                case "Lt":
                    value = left < right
                case "Gt":
                    value = left > right
                case "Gte":
                    value = left >= right
                case "And":
                    value = left and right
                case "Or":
                    value = left or right
                case "Nand":
                    value = not (left and right)
                case "Xor":
                    value = (left and not right) or (not left and right)
                case "Xnor":
                    value = (left and right) or (not left and not right)
                case "Nor":
                    value = not left and not right
                case "Addition":
                    if isinstance(left, str) or isinstance(right, str):
                        value = str(left) + str(right)
                    else:
                        value = left + right
                case "Subtraction":
                    value = left - right
                case "Division":
                    if right == 0:
                        raise SyntaxError(f"Division by 0.")
                    value = left / right
                case "Multiplication":
                    value = left * right
                case "Modulo":
                    value = left % right
                case "Exponent":
                    value = left ** right

            return value
        elif isinstance(node, UnaryOperationNode):
            op = node.op
            right = self.evaluate(node.right)

            if op.label == "Subtraction":
                return -right
            elif op.label == "Not":
                return not right
            raise SyntaxError(f"Unexpected {op.label} operation '{op.data}' at line {op.line}, column {op.column}")
        else:
            raise TypeError(f"Can't evaluate unknown node type {type(node)}")

