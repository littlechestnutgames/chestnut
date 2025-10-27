from parser import *
from chestnut_type import *
from error import *
from supporting import *
from lexer import lex
from math import floor
import copy
import os

def generate_struct_init(properties):
    def struct_instance_init(self, *args):
        ChestnutStruct.__init__(self, ChestnutNull(None))
        i = 0
        for i, prop in enumerate(properties):
            if i < len(args):
                setattr(self, prop.identifier.data, args[i])
            else:
                setattr(self, prop.identifier.data, ChestnutNull(None))
    return struct_instance_init

class FunctionRegister:
    def __init__(self):
        self.functions = {}

    def register(self, func):
        fname = func.name.data if hasattr(func, "name") else func.identifier.data
        if not fname in self.functions:
            self.functions[fname] = {"candidates": []}
        registry = self.functions[fname]

        for candidate in registry["candidates"]:
            if candidate.mangled_key == func.mangled_key:
                raise RuntimeException("Cannot define a function overload with the same parameters", func.name)
        
        registry["candidates"].insert(0, func)

    def resolve(self, name, call_parameters=[]):
        if name not in self.functions:
            raise RuntimeException(f"Call to undefined function {name}")

        call_params = call_parameters
        num_call_params = len(call_params)
        
        best_match_candidate = None
        best_score = -1 

        registry = self.functions[name]
        
        for candidate in registry["candidates"]:
            candidate_params = candidate.parameters 
            num_candidate_params = len(candidate_params)
            current_score = 0
            is_feasible = True

            is_variadic_func = num_candidate_params > 0 and candidate_params[-1].variadic
            
            required_count = 0
            for param in candidate_params:
                if param.default_value is None and not param.variadic:
                    required_count += 1
                else:
                    break

            num_fixed_params = num_candidate_params
            if is_variadic_func:
                num_fixed_params -= 1
            
            if is_variadic_func:
                if num_call_params < required_count:
                    continue
            else:
                if not (required_count <= num_call_params <= num_fixed_params):
                    continue
            
            for i in range(min(num_call_params, num_fixed_params)):
                param = candidate_params[i]
                expected_type = eval("Chestnut" + param.paramtype.data)
                runtime_arg = call_params[i]
                runtime_type_name = runtime_arg.__class__.__name__.replace("Chestnut", "")
                
                if isinstance(runtime_arg, expected_type):
                    current_score += 3
                elif expected_type == ChestnutAny:
                    current_score += 1
                else:
                    is_feasible = False
                    break
            
            if not is_feasible:
                continue

            if is_variadic_func and num_call_params > num_fixed_params:
                variadic_param = candidate_params[-1]
                variadic_type = eval("Chestnut" + variadic_param.paramtype.data)
                
                for i in range(num_fixed_params, num_call_params):
                    runtime_arg = call_params[i]

                    if isinstance(runtime_arg, variadic_type):
                        current_score += 3
                    elif variadic_type == ChestnutAny:
                        current_score += 1 
                    else:
                        is_feasible = False
                        break
            
            if is_feasible and current_score > best_score:
                best_score = current_score
                best_match_candidate = candidate

        if best_match_candidate is None:
            raise RuntimeException(f"No call signature for {name} is compatible with given parameters" + str(call_parameters))

        return best_match_candidate

class BringVariable:
    def __init__(self, scope, var_name):
        self.scope = scope
        self.var_name = var_name

    def __getitem__(self, _):
        return self.scope[self.var_name]

    def __setitem__(self, _, value):
        self.scope[self.var_name] = value

    def __contains__(self, key):
        return self.var_name == key

    def __iadd__(self, value):
        self.scope[self.var_name] += value
        return self

    def __isub__(self, value):
        self.scope[self.var_name] -= value
        return self

    def __imul__(self, value):
        self.scope[self.var_name] *= value
        return self

    def __itruediv__(self, value):
        self.scope[self.var_name] /= value
        return self

    def __repr__(self):
        return f"BringVariable({self.var_name})"

    def __str__(self):
        value = self.scope[self.var_name]
        if isinstance(value, BringVariable):
            return f"<{value.var_name}> (BringVariable)"

        return str(self.scope[self.var_name])

class StructNode:
    def __init__(self, definition):
        self.definition = definition
        self.function_register = FunctionRegister()

        params = []
        for param in  self.definition.properties:
            params.append(FnParameter(param.identifier, param.value_type, ChestnutNull(None)))
        print(f"Registering {definition.identifier.data}'s constructor with its function register")
        self.function_register.register(NativeFunction(Token("Identifier", "constructor", None, None), params))
        
    def constructor(self):
        name = self.definition.identifier.data
        properties = self.definition.properties
        struct_class = type(name, (ChestnutStruct,), {
            "__repr__": lambda self: name + "(" + str(properties) + ")",
            "__init__": generate_struct_init(properties),
            "gettype": lambda self: name
        })
        struct_instance = struct_class()
        return struct_instance

class StructMethodCall:
    def __init__(self, instance, func_object):
        self.instance = instance
        self.func_object = func_object

class NativeFunction:
    def __init__(self, identifier, params):
        self.identifier = identifier
        self.params = params
        self.name = identifier
        self.parameters = params

    def reconcile_parameters(self, evaluator, call_parameters):
        name = self.identifier
        required_count = 0
        has_variadic = False
        for param in self.params:
            if param.default_value is None and not param.variadic:
                required_count += 1
            if param.variadic:
                has_variadic = True

        if (len(call_parameters) < required_count) or (not has_variadic and len(call_parameters) > len(self.params)):
            raise RuntimeException(f"Required number of parameters for `{name}` is {required_count}, got {len(call_parameters)}")

        evaluated_args = [evaluator.evaluate(param) for param in call_parameters]

        values = {}
        arg_index = 0
        for param in self.params:
            param_name = param.name.data
            if arg_index < len(evaluated_args):
                values[param_name] = evaluated_args[arg_index]
            elif param.default_value is not None:
                values[param_name] = evaluator.evaluate(param.default_value)
            arg_index += 1
        return values

class Function:
    def __init__(self, statement, parent_scopes=None):
        self.statement = statement
        self.scopes = parent_scopes if parent_scopes is not None else []

    def reconcile_parameters(self, evaluator, call_parameters):
        statement = self.statement
        name = None
        struct_identifier = None
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
            raise RuntimeException(f"Required number of parameters for `{name}` is {required_count}, got {len(call_parameters)}")

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
        return f"{self.statement}"

class AnonymousFunction(Function):
    def __init__(self, statement, name=None, parent_scopes=None):
        super().__init__(statement, parent_scopes)
        self.name = name

class SpreadArgs(ChestnutAny):
    def __init__(self, args):
        self.token = Token("Null", ChestnutNull, None, None)
        self.value = ChestnutNull(None)
        self.args = args
    def __repr__(self):
        return f"SpreadArgs(<{self.args}>)"

class ReturnValue(BaseException):
    def __init__(self, value):
        self.value = value

class BasicControlFlow(BaseException):
    def __init__(self, ast_node):
        self.ast_node = ast_node

    def gettype(self):
        return "BasicControlFlow"

    def __repr__(self):
        return f"BasicControlFlow(<{self.ast_node}>)"

class BreakLoop(BasicControlFlow):
    def gettype(self):
        return "BreakLoop"

class ContinueLoop(BasicControlFlow):
    def gettype(self):
        return "Continue"

class Evaluator:
    def get_core_spec(self):
        from bridge import py_bridge as core
        mods = [ x for x in dir(core) if x.startswith("__internal_") ]
        import inspect
        core_spec = {}
        for mod in mods:
            core_spec[mod] = {}
            args = inspect.getfullargspec(core.__dict__[mod]).args
            varargs = inspect.getfullargspec(core.__dict__[mod]).varargs
            if args:
                core_spec[mod]["args"] = args
            if varargs:
                core_spec[mod]["varargs"] = varargs
        return core_spec
    def get_local_script(self, script_name):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return f"{dir_path}{os.sep}{script_name}"

    def eval_library(self, path):
        with open(self.get_local_script(path)) as new_import:
            tokens = lex("".join(new_import.readlines()))
            parser = Parser(tokens)
            ast = parser.parse_program()
            for node in ast:
                setattr(node, "Chestnut-bridge", True)
                self.evaluate(node)

    def __init__(self):
        self.function_register = FunctionRegister()
        self.calling_builtin = False
        core_spec = self.get_core_spec()
        native_funcs = {}
        self.scopes = [{}]
        for k, v in core_spec.items():
            func_name = Token("Identifier", k, None, None)
            params = []
            if "args" in v:
                for arg in v["args"]:
                    params.append(FnParameter(Token("Identifier", arg, None, None), Token("Identifier", "Any", None, None), None, False))
            if "varargs" in v:
                params.append(FnParameter(Token("Identifier", v["varargs"], None, None), Token("Identifier", "Any", None, None), None, True))

            func = NativeFunction(func_name, params)

            self.scopes[0][k] = NativeFunction(func_name, params)
            self.function_register.register(func)
        self.eval_library("lib/core.nuts")

    def push_scope(self, scope={}):
        self.scopes.append({})

    def pop_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()
        else:
            raise Exception("Cannot pop the global scope")

    def find_first_scope_containing(self, var_name):
        found_scope = None
        for i in range(len(self.scopes) - 1, -1, -1):
            scope = self.scopes[i]
            if var_name in scope:
                return scope
        return None

    def exists_in_any_scope(self, var_name):
        return self.exists_in_current_scope(var_name) or self.exists_in_parent_scope(var_name)

    def exists_in_current_scope(self, var_name):
        return var_name in self.scopes[-1] and not "call boundary" in self.scopes[-1]

    def exists_in_parent_scope(self, var_name):
        for scope in reversed(self.scopes[:-1]):
            if "call boundary" in scope:
                break
            if var_name in scope:
                return True
        if var_name in self.scopes[0]:
            return True
        return False

    def current_scope(self):
        return self.scopes[-1]
    
    def constant_exists(self, label):
        return self.exists_in_any_scope(f"constant {label}")

    def evaluate(self, node):
        if isinstance(node, StructFnStatementNode):
            struct_name = node.target_struct.paramtype.data
            method_name = node.name.data
            scope_key = f"{struct_name} {method_name}"
            func_object = Function(node)
            if self.exists_in_any_scope(scope_key):
                raise RuntimeError(f"{method_name} for struct {struct_name} already exists", node)
            self.current_scope()[scope_key] = func_object

            return 1
        elif isinstance(node, ChestnutNull):
            return node
        elif isinstance(node, ChestnutInteger):
            return node.value
        elif isinstance(node, ChestnutBoolean):
            return node.value
        elif isinstance(node, ChestnutFloat):
            return node.value
        elif isinstance(node, ChestnutString):
            return node.value
        elif isinstance(node, ChestnutAny) and node.token.label in ["ChestnutInteger", "ChestnutBoolean", "ChestnutFloat", "ChestnutString", "UnaryOperationNode"]:
            return node.value
        elif isinstance(node, ImportStatementNode):
            import_path = f"{os.getcwd()}{os.sep}{node.location.data}"
            with open(import_path) as new_import:
                tokens = lex("".join(new_import.readlines()))
                parser = Parser(tokens)
                ast = parser.parse_program()
                for node in ast:
                    self.evaluate(node)
        elif isinstance(node, StructDefinitionNode):
            label = node.identifier.data
            scope = self.find_first_scope_containing(label)
            if not scope is None:
                raise Exception(f"Cannot redefine struct {label} at line {node.target.line}, column {node.target.column}")
            struct_node = StructNode(node)
            self.current_scope()[label] = struct_node
        elif isinstance(node, PropertyAssignmentNode):
            target_object = self.evaluate(node.identifier)
            if target_object is None:
                raise RuntimeException("Attempt to access property on null", node.identifier)
            property = node.property_identifier.data

            if not hasattr(target_object, property):
                raise RuntimeException("Target has no attribute {property}", node.property_identifier)

            op = node.op 
            if op.label == "Assignment":
                setattr(target_object, property, self.evaluate(node.value_expression))
            elif op.label == "Addassign":
                setattr(target_object, property, getattr(target_object, property) + self.evaluate(node.value_expression))
            elif op.label == "Subassign":
                setattr(target_object, property, getattr(target_object, property) - self.evaluate(node.value_expression))
            elif op.label == "Divassign":
                setattr(target_object, property, getattr(target_object, property) / self.evaluate(node.value_expression))
            elif op.label == "Mulassign":
                setattr(target_object, property, getattr(target_object, property) * self.evaluate(node.value_expression))
            return 1
        elif isinstance(node, PropertyAccessNode):
            target_object = self.evaluate(node.identifier)
            if target_object is None:
                raise RuntimeException(f"Attempt to access property on null object at line...", node)
            property_name = node.property_identifier.data
            if hasattr(target_object, "gettype"):
                scope_key = f"{target_object.gettype()} {node.property_identifier.data}"
                scope = self.find_first_scope_containing(scope_key)
                if scope is not None:
                    func_object = scope[scope_key]
                    return StructMethodCall(target_object, func_object)
            return getattr(target_object, property_name)
        elif isinstance(node, ListLiteralNode):
            return ChestnutList([ self.evaluate(x) for x in node.elements ])
        elif isinstance(node, TupleLiteralNode):
            return ChestnutTuple(tuple([ self.evaluate(x) for x in node.elements ]))
        elif isinstance(node, IndexAssignNode):
            target = self.evaluate(node.identifier)
            if isinstance(target, tuple):
                raise RuntimeException("Illegal assingment, tuples are immutable", node.identifier)
            if not isinstance(target, list):
                raise RuntimeException("Index access attempted on non-list", node.identifier)
            index = self.evaluate(node.index)
            if index == ChestnutInteger(-1):
                index = ChestnutInteger(len(target) - 1)
            if index < ChestnutInteger(-1):
                raise RuntimeException("List bounds exceeded in assignment", node.identifier)
            if index > ChestnutInteger(len(target) - 1):
                raise RuntimeException("List bounds exceeded in assignment", node.identifier)
            op = node.op

            if node.op.label == "Assignment":
                target[index] = self.evaluate(node.value)
            elif node.op.label == "Addassign":
                target[index] += self.evaluate(node.value)
            elif node.op.label == "Subassign":
                target[index] -= self.evaluate(node.value)
            elif node.op.label == "Divassign":
                target[index] /= self.evaluate(node.value)
            elif node.op.label == "Mulassign":
                target[index] *= self.evaluate(node.value)
            return 1

        elif isinstance(node, IndexAccessNode):
            target_value = self.evaluate(node.target)
            index = self.evaluate(node.index)
            if not isinstance(target_value, list) and not isinstance(target_value, tuple) and not isinstance(target_value, str) and not isinstance(target_value, ChestnutString):
                raise Exception(f"Index access attempted on non-array type {target_value.__repr__()}")
            if index == ChestnutInteger(-1):
                index = ChestnutInteger(len(target_value) - 1)
            if index < ChestnutInteger(0) or index >= ChestnutInteger(len(target_value)):
                raise Exception(f"Index out of bounds")
            return target_value[index]

        elif isinstance(node, ExpressionStatementNode):
            return self.evaluate(node.expression)
        elif isinstance(node, ReturnStatementNode):
            return_value = None
            if node.expression:
                return_value = self.evaluate(node.expression)
            raise ReturnValue(return_value)
        elif isinstance(node, ConstantStatementNode):
            labels = node.label
            if not isinstance(node.label, ChestnutTuple):
                labels = [node.label]
            for l in labels:
                if self.constant_exists(l.data):
                    raise RuntimeException(f"Cannot redeclare constant `{l.data}`", l)
                if self.exists_in_any_scope(l.data):
                    raise RuntimeException(f"`{l.data}` is already declared in this scope", l)

            expression = self.evaluate(node.expression)
            if not isinstance(expression, ChestnutTuple):
                expression = [expression]

            i = 0
            while i < len(labels):
                self.current_scope()[f"constant {labels[i].data}"] = expression[i]
                i = i + 1

            return 1

        elif isinstance(node, LetStatementNode):
            labels = node.label
            if not hasattr(node.label, "__iter__"):
                labels = [node.label]

            for l in labels:
                if not self.calling_builtin:
                    if self.constant_exists(l.data):
                        raise RuntimeException(f"Cannot redeclare constant `{l.data}`", l)

                    if self.exists_in_any_scope(l.data):
                        raise RuntimeException(f"Cannot redeclare {l.data} in this scope", l)

            expression = self.evaluate(node.expression)
            if not isinstance(expression, ChestnutTuple):
                expression = [expression]

            i = 0
            while i < len(labels):
                self.current_scope()[labels[i].data] = expression[i]
                i = i + 1

            return 1

        elif isinstance(node, ShadowStatementNode):
            labels = node.label
            if not isinstance(node.label, list):
                labels = [node.label]
            for l in labels:
                if self.constant_exists(l.data):
                    raise RuntimeException(f"Cannot shadow constant `{l.data}`", l)

                if self.exists_in_current_scope(l.data):
                    raise RuntimeException(f"Cannot shadow {l.data} because is already declared in the same scope", l)

                if not self.exists_in_any_scope(l.data):
                    raise RuntimeException(f"{l.data} is not declared in any scope", l)

            expression = self.evaluate(node.expression)
            if not isinstance(expression, tuple):
                expression = [expression]

            i = 0
            while i < len(labels):
                self.current_scope()[labels[i].data] = expression[i]
                i = i + 1

            return 1

        elif isinstance(node, FnStatementNode):
            captured_scopes = []

            definition_scope = self.current_scope()
            captured_scopes.append(definition_scope)

            for bring in node.brings:
                scope = self.find_first_scope_containing(bring.data)
                if scope is None:
                    raise RuntimeException(f"Variable {bring.data} in brings clause not found in any scope", node)

                if scope not in captured_scopes:
                    captured_scopes.append(scope)

            func_object = Function(node, captured_scopes)
            self.function_register.register(node)
            if self.constant_exists(node.name.data):
                raise Exception(f"Function definition for `{node.name.data}` conflicts with a constant at line {node.name.line}, column {node.name.column}")
            # if self.exists_in_any_scope(node.name.data):
            #     raise Exception(f"{node.name.data} is already defined in the current scope, line {node.name.line}, column {node.name.column}")
            self.current_scope()[node.name.data] = func_object

            return 1

        elif isinstance(node, AnonymousFnExpressionNode):
            return AnonymousFunction(node)

        elif isinstance(node, CallStatementNode):
            callable = self.evaluate(node.identifier)
            print(callable)
            self.calling_builtin = False
            identifier = None
            func = None
            instance = None
            if isinstance(callable, StructNode):
                method = "constructor"
                func = callable.function_register.resolve(method, [ self.evaluate(x) for x in node.params ])
            if isinstance(callable, StructMethodCall):
                instance = callable.instance
                func = callable.func_object
                identifier = func.statement.target_struct.name.data
                scope_key = f"{func.statement.target_struct.paramtype.data} {func.statement.name.data}"
                first_scope = self.find_first_scope_containing(scope_key)
                first_scope[identifier] = instance

            if isinstance(node.identifier, AnonymousFnExpressionNode):
                func = AnonymousFunction(node.identifier)

            if func is None:
                if not self.exists_in_any_scope(node.identifier.data) and not self.exists_in_any_scope(f"constant {node.identifier.data}"):
                    # The function was found neither in non-constant or constant storage.
                    raise Exception(f"Call to undefined function `{node.identifier.data}`")

                identifier = node.identifier.data
                func_scope = self.find_first_scope_containing(identifier)
                l = self.function_register.resolve(identifier, [ self.evaluate(x) for x in node.params ])
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

            if isinstance(func, StructNode):
                return func.constructor()

            if not isinstance(func, Function) and not isinstance(func, AnonymousFunction) and not isinstance(func, NativeFunction):
                # Block function calls to other stored data.
                raise Exception(f"Call to non-function `{identifier}` at line {node.identifier.line}, column {node.identifier.column}")
            if isinstance(func, NativeFunction):
                params = []
                try:
                    reconciled_values = func.reconcile_parameters(self, node.params)
                except RuntimeException as e:
                    raise RuntimeException(e.message, node.identifier)

                final_args = []
                for k in reconciled_values:
                    value = reconciled_values[k]
                    if isinstance(value, SpreadArgs):
                        for arg in value.args:
                            final_args.append(arg)
                    else:
                       final_args.append(value)
                from bridge import py_bridge as core
                
                if not hasattr(core,func.identifier.data):
                    raise InternalException(f"{func.identifier.data} does not exist in the core built-ins", node)

                result = core.__dict__[func.identifier.data](
                    *final_args
                )

                raise ReturnValue(result)

            fn = func.statement

            base_stack_length = len(self.scopes)

            # Push a call boundary before restoring the captured scopes.
            # This call boundary will prevent scope from leaking from lower levels.
            if hasattr(fn, "Chestnut-bridge"):
                # Bridge functions like print don't get their own boundaries.
                self.scopes.append({"Chestnut-bridge": True})
                self.calling_builtin = True
            else:
                self.scopes.append({"call boundary": True})

            for scope_to_load in func.scopes:
                self.scopes.append(scope_to_load)

            self.push_scope() 

            params = []
            try:
                params = func.reconcile_parameters(self, node.params)
            except RuntimeException as e:
                raise RuntimeException(e.message, node.identifier)
            for p in func.statement.parameters:
                self.current_scope()[p.name.data] = params[p.name.data]
                
            for s in func.statement.statements:
                try:
                    self.evaluate(s)
                except ReturnValue as val:
                    if isinstance(val.value, (Function, AnonymousFunction)):
                        live_closure_scope = self.scopes.pop()
                        val.value.scopes.append(live_closure_scope)

                    while len(self.scopes) > base_stack_length:
                        self.pop_scope()
                    return val.value

            while len(self.scopes) > base_stack_length:
                self.pop_scope()
            return False

        elif isinstance(node, BreakStatementNode):
            raise BreakLoop(node)

        elif isinstance(node, ContinueStatementNode):
            raise ContinueLoop(node)

        elif isinstance(node, Token) and node.label == "Identifier":
            label = node.data

            if self.constant_exists(label):
                label = f"constant {label}"
            stored_scope = self.find_first_scope_containing(label)
            if stored_scope is None:
                raise Exception(f"Couldn't find symbol {label} at line {node.line}, column {node.column}")
            result = stored_scope[label]
            if isinstance(result, BringVariable):
                return result.__getitem__(None)

            return result

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
                for statement in node.else_block.block_statements:
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
                if isinstance(scope[label], BringVariable):
                    scope[label].__setitem__(None, expression)
                else:
                    scope[label] = expression
            elif op.label == "Addassign":
                scope[label] += expression
            elif op.label == "Subassign":
                scope[label] -= expression
            elif op.label == "Mulassign":
                scope[label] *= expression
            elif op.label == "Divassign":
                scope[label] /= expression
            else:
                return 0
            return 1

        elif isinstance(node, IterateStatementNode):
            self.push_scope()
            subject = self.evaluate(node.subject)
            identifier = node.identifier
            statements = node.statements
            root_loop_scope = self.current_scope()
            root_loop_scope["loop index"] = ChestnutInteger(0)
            for elem in subject:
                self.push_scope()
                self.current_scope()[identifier.data] = elem
                try:
                    for statement in statements:
                        self.evaluate(statement)
                except BreakLoop:
                    self.pop_scope()
                    break
                except ContinueLoop:
                    root_loop_scope["loop index"] = root_loop_scope["loop index"] + ChestnutInteger(1)
                    self.pop_scope()
                    continue
                self.pop_scope()
                root_loop_scope["loop index"] = root_loop_scope["loop index"] + ChestnutInteger(1)
            self.pop_scope()
            del root_loop_scope["loop index"]


        elif isinstance(node, WhileStatementNode):
            self.push_scope()
            root_loop_scope = self.current_scope()
            self.current_scope()["loop index"] = ChestnutInteger(0)
            while self.evaluate(node.condition):
                self.push_scope()
                try:
                    for statement in node.statements:
                        self.evaluate(statement)
                except BreakLoop:
                    self.pop_scope()
                    break
                except ContinueLoop:
                    root_loop_scope["loop index"] = root_loop_scope["loop index"] + ChestnutInteger(1)
                    self.pop_scope()
                    continue
                self.pop_scope()
                root_loop_scope["loop index"] = root_loop_scope["loop index"] + ChestnutInteger(1)
            self.pop_scope()
            del root_loop_scope["loop index"]

        elif isinstance(node, UntilStatementNode):
            self.push_scope()
            root_loop_scope = self.current_scope()
            self.current_scope()["loop index"] = ChestnutInteger(0)
            while not self.evaluate(node.condition):
                self.push_scope()
                try:
                    for statement in node.statements:
                        self.evaluate(statement)
                except BreakLoop:
                    self.pop_scope()
                    break
                except ContinueLoop:
                    root_loop_scope["loop index"] = root_loop_scope["loop index"] + ChestnutInteger(1)
                    self.pop_scope()
                    continue
                self.pop_scope()
                root_loop_scope["loop index"] = root_loop_scope["loop index"] + ChestnutInteger(1)
            self.pop_scope()
            del root_loop_scope["loop index"]

        elif isinstance(node, LoopindexExpressionNode):
            scope = self.find_first_scope_containing("loop index")
            if scope is None:
                raise Exception(f"`loop_index` keyword must be used inside a loop")
            return scope["loop index"]

        elif isinstance(node, UseExpressionNode):
            if not node.condition is None:
                if self.evaluate(node.condition):
                    return self.evaluate(node.right)
                return self.evaluate(node.left)
            else:
                left = self.evaluate(node.left)
                if isinstance(left, ChestnutNull):
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
                case "BitwiseAnd":
                    value = left & right
                case "BitwiseOr":
                    value = left | right
                case "BitwiseNand":
                    value = ~(left & right)
                case "BitwiseXor":
                    value = left ^ right
                case "BitwiseNor":
                    value = ~(left | right)
                case "BitwiseXnor":
                    value = ~(left ^ right)
                case "BitwiseShiftLeft":
                    value = left << right
                case "BitwiseShiftRight":
                    value = left >> right
                case "BitwiseRotateRight":
                    raise InternalException("Bitwise right rotate is not implemented yet")
                case "BitwiseRotateLeft":
                    raise InternalException("Bitwise left rotate is not implemented yet")
                case "Addition":
                        value = left + right
                case "Subtraction":
                    value = left - right
                case "Division":
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
            if op.label == "Spread":
                return SpreadArgs(self.evaluate(node.right))
            # Outer code here
            if op.label == "Outer":
                levels = 1
                ref = node.right
                while isinstance(ref, UnaryOperationNode) and ref.op.label == "Outer":
                    levels = levels + 1
                    ref = ref.right
                if not isinstance(ref, Token) and hasattr(ref, "label") and not ref.label == "Identifier":
                    raise RuntimeException("Expected identifer after outer", ref)

                identifier = None
                if isinstance(ref, LoopindexExpressionNode):
                    identifier = "loop index"
                else:
                    identifier = ref.data
                for scope in reversed(self.scopes[:]):
                    if identifier in scope and levels > 0:
                        levels = levels - 1
                    elif identifier in scope:
                        return scope[identifier]
                return ChestnutNull(Token("Null", "null", 0, 0))

            right = self.evaluate(node.right)

            if op.label == "Subtraction":
                return -right
            elif op.label == "Not":
                value = ChestnutBoolean(not right)
                return value
            elif op.label == "BitwiseNot":
                return ~right
            raise RuntimeException(f"Unexpected {op.label} operation '{op.data}'", op)
        else:
            raise RuntimeException(f"Can't evaluate unknown node type {type(node)}")
