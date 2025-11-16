from parser import *
from chestnut_types import *
from error import *
from token_types import *
from lexer import lex
from math import floor
import copy
import os

def generate_struct_init(properties):
    def struct_instance_init(self, *args):
        ChestnutStruct.__init__(self, CHESTNUT_NULL)
        i = 0
        for i, prop in enumerate(properties):
            if i < len(args):
                setattr(self, prop.identifier.data, args[i])
            else:
                setattr(self, prop.identifier.data, CHESTNUT_NULL)
    return struct_instance_init

class FunctionRegister:
    def __init__(self):
        self.functions = {}

    def is_registered(self, name):
        return name in self.functions

    def register(self, func):
        fname = ""
        if isinstance(func, BridgeFunction):
            fname = func.identifier.data
        if isinstance(func, Function):
            fname = func.statement.name.data
        if not fname in self.functions:
            self.functions[fname] = {"candidates": []}
        registry = self.functions[fname]

        for candidate in registry["candidates"]:
            if candidate.statement.mangled_key == func.statement.mangled_key:
                # Function register is temporarily disabled until we get functions
                # Registering in lexical scope instead of with the global FunctionRegister
                # Any function that defines inner functions right now will error out
                # if the code below the return were enabled.
                return
                # raise RuntimeException("Cannot define a function overload with the same parameters", func.statement.name)
        
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
    """
        Provides mutable access to a variable from an outside scope by keeping
        a weak reference to the original scope it was defined in and acting as 
        a scope dictionary that can only interact with that specific variable.
    """

    def __init__(self, scope, var_name):
        # Set the reference to the scope and variable name
        self.scope = scope
        self.var_name = var_name

    def __getitem__(self, _):
        # The only item available here is var_name.
        return self.scope[self.var_name]

    def __setitem__(self, _, value):
        # The only item we're allowed to set is var_name.
        self.scope[self.var_name] = value

    def __contains__(self, key):
        # The only item we're allowed to confirm existence for is var_name.
        return self.var_name == key

    def __iadd__(self, value):
        # In-place addition for the scoped variable.
        self.scope[self.var_name] += value
        return self

    def __isub__(self, value):
        # In-place subtraction for the scoped variable.
        self.scope[self.var_name] -= value
        return self

    def __imul__(self, value):
        # In-place multiplication for the scoped variable.
        self.scope[self.var_name] *= value
        return self

    def __itruediv__(self, value):
        # In-place division for the scoped variable.
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
            params.append(FnParameter(param.identifier, param.value_type, CHESTNUT_NULL))
        self.function_register.register(BridgeFunction(Token("Identifier", "constructor", None, None), params))
        
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

class BridgeFunction:
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
        # Test
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

class Function(ChestnutAny):
    def __init__(self, statement, parent_scopes=None):
        self.statement = statement
        self.scopes = parent_scopes if parent_scopes is not None else []
        self.token = Token("Null", CHESTNUT_NULL, None, None)
        self.value = CHESTNUT_NULL

    def reconcile_parameters(self, evaluator, call_parameters):
        statement = self.statement
        name = None
        struct_identifier = None
        if isinstance(statement, FnStatementNode):
            name = statement.name.data
        elif isinstance(statement, AnonymousFnExpressionNode):
            name = self.name

        if len(call_parameters) > 0 and isinstance(call_parameters[-1], UnaryOperationNode) and call_parameters[-1].op.label == "Spread":
            op_node = call_parameters.pop(-1)
            evaluated_spread = evaluator.evaluate(op_node)
            for arg in evaluated_spread.args:
                call_parameters.append(arg)

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
        self.value = CHESTNUT_NULL
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

            func = BridgeFunction(func_name, params)

            self.scopes[0][k] = BridgeFunction(func_name, params)
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
    
    def visit_StructFnStatementNode(self, node):
        if not isinstance(node, StructFnStatementNode):
            raise InternalException(f"Cannot use {node.__class__.__name__} in visit_StructFnStatementNode", node)

        struct_name = node.target_struct.paramtype.data
        method_name = node.name.data
        scope_key = f"{struct_name} {method_name}"
        func_object = Function(node)
        if self.exists_in_any_scope(scope_key):
            raise RuntimeError(f"{method_name} for struct {struct_name} already exists", node)
        self.current_scope()[scope_key] = func_object

        return 1
    
    def visit_ChestnutNull(self, node):
        if not isinstance(node, ChestnutNull):
            raise InternalException(f"Cannot use {node.__class__.__name__} in visit_ChestnutNull", node)
        return node

    def visit_ChestnutInteger(self, node):
        if not isinstance(node, ChestnutInteger):
            raise InternalException(f"Cannot use {node.__class__.__name__} in visit_ChestnutInteger", node)
        return node.value

    def visit_ChestnutBoolean(self, node):
        if not isinstance(node, ChestnutBoolean):
            raise InternalException(f"Cannot use {node.__class__.__name__} in visit_ChestnutBoolean", node)
        return node.value

    def visit_ChestnutFloat(self, node):
        if not isinstance(node, ChestnutFloat):
            raise InternalException(f"Cannot use {node.__class__.__name__} in visit_ChestnutFloat", node)
        return node.value

    def visit_ChestnutString(self, node):
        if not isinstance(node, ChestnutString):
            raise InternalException(f"Cannot use {node.__class__.__name__} in visit_ChestnutString", node)
        return node.value

    def _handle_unary_Spread(self, node):
        return SpreadArgs(self.evaluate(node.right))

    def _handle_unary_Outer(self, node):
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
    
    def _handle_unary_Subtraction(self, node):
        right = self.evaluate(node.right)
        return ChestnutInteger(-(right.value))

    def _handle_unary_Not(self, node):
        right = self.evaluate(node.right)
        return ChestnutBoolean(not right)

    def _handle_unary_BitwiseNot(self, node):
        right = self.evaluate(node.right)
        return ~right

    def visit_UnaryOperationNode(self, node):
        if not isinstance(node, UnaryOperationNode):
            raise InternalException(f"Cannot use {node.__class__.__name__} in visit_UnaryOperationNode", node)
        op = node.op
        method = f"_handle_unary_{op.label}"
        if hasattr(self,method):
            return getattr(self, method)(node)
        raise RuntimeException(f"Unexpected {op.label} operation '{op.data}'", op)

    def visit_ChestnutString(self, node):
        if not isinstance(node, ChestnutString):
            raise InternalException(f"Cannot use {node.__class__.__name__} in visit_ChestnutString", node)
        return node.value

    def visit_ImportStatementNode(self, node):
        if not isinstance(node, ImportStatementNode):
            raise InternalException(f"Cannot use {node.__class__.__name__} in visit_ImportStatementNode", node)
        import_path = f"{os.getcwd()}{os.sep}{node.location.data}"
        with open(import_path) as new_import:
            tokens = lex("".join(new_import.readlines()))
            parser = Parser(tokens)
            ast = parser.parse_program()
            for n in ast:
                if len(node.imports) == 0 or n.get_name() in [ x.data for x in node.imports ]:
                    self.evaluate(n)

    def visit_StructDefinitionNode(self, node):
        if not isinstance(node, StructDefinitionNode):
            raise InternalException(f"Cannot use {node.__class__.__name__} in visit_StructDefinitionNode", node)
        label = node.identifier.data
        scope = self.find_first_scope_containing(label)
        if not scope is None:
            raise Exception(f"Cannot redefine struct {label} at line {node.target.line}, column {node.target.column}")
        struct_node = StructNode(node)
        self.current_scope()[label] = struct_node

    def _handle_prop_Assignment(self, target_object, property, value):
        setattr(target_object, property, value)

    def _handle_prop_Addassign(self, target_object, property, value):
        setattr(target_object, property, getattr(target_object, property) + value)

    def _handle_prop_Subassign(self, target_object, property, value):
        setattr(target_object, property, getattr(target_object, property) - value)

    def _handle_prop_Mulassign(self, target_object, property, value):
        setattr(target_object, property, getattr(target_object, property) * value)

    def _handle_prop_Divassign(self, target_object, property, value):
        setattr(target_object, property, getattr(target_object, property) / value)

    def visit_PropertyAssignmentNode(self, node):
        if not isinstance(node, PropertyAssignmentNode):
            raise InternalException(f"Cannot use {node.__class__.__name__} in visit_PropertyAssignmentNode", node)
        target_object = self.evaluate(node.identifier)
        if target_object is None:
            raise RuntimeException("Attempt to access property on null", node.identifier)

        property = node.property_identifier.data

        if not hasattr(target_object, property):
            raise RuntimeException("Target has no attribute {property}", node.property_identifier)

        op = node.op
        value = self.evaluate(node.value_expression)

        method = f"_handle_prop_{op.label}"
        if hasattr(self, method):
            getattr(self, method)(target_object, property, value)
        else:
            raise RuntimeException(f"Property assignment operation {op.data} is unsupported", op)

        return 1

    def visit_PropertyAccessNode(self, node):
        if not isinstance(node, PropertyAccessNode):
            raise InternalException(f"Cannot use {node.__class__.__name__} in visit_PropertyAccessNode", node)
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

    def visit_ListLiteralNode(self, node):
        if not isinstance(node, ListLiteralNode):
            raise InternalException(f"Cannot use {node.__class__.__name__} in visit_ListLiteralNode", node)
        return ChestnutList([ self.evaluate(x) for x in node.elements ])

    def visit_TupleLiteralNode(self, node):
        if not isinstance(node, TupleLiteralNode):
            raise InternalException(f"Cannot use {node.__class__.__name__} in visit_TupleLiteralNode", node)
        return ChestnutTuple(tuple([ self.evaluate(x) for x in node.elements ]))

    def _handle_index_Assignment(self, node, target, index):
        target[index] = self.evaluate(node.value)

    def _handle_index_Addassign(self, node, target, index):
        target[index] += self.evaluate(node.value)

    def _handle_index_Subassign(self, node, target, index):
        target[index] -= self.evaluate(node.value)

    def _handle_index_Mulassign(self, node, target, index):
        target[index] *= self.evaluate(node.value)

    def _handle_index_Divassign(self, node, target, index):
        target[index] /= self.evaluate(node.value)

    def visit_IndexAssignNode(self, node):
        if not isinstance(node, IndexAssignNode):
            raise InternalException(f"Cannot use {node.__class__.__name__} in visit_IndexAssignNode", node)

        target = self.evaluate(node.identifier)
        if isinstance(target, tuple):
            raise RuntimeException("Illegal assingment, tuples are immutable", node.identifier)

        if not isinstance(target, (list, ChestnutList, ChestnutTuple, tuple)):
            raise RuntimeException("Index access attempted on non-list", node.identifier)

        index = self.evaluate(node.index)
        if index == ChestnutInteger(-1):
            index = ChestnutInteger(len(target) - 1)
        if index < ChestnutInteger(-1):
            raise RuntimeException("List bounds exceeded in assignment", node.identifier)
        if index > ChestnutInteger(len(target) - 1):
            raise RuntimeException("List bounds exceeded in assignment", node.identifier)

        op = node.op
        method = f"_handle_index_{op.label}"
        if hasattr(self, method):
            getattr(self, method)(node, target, index)
        else:
            raise RuntimeException(f"Unsupported index assignment operation {op.data}")

        return 1

    def visit_IndexAccessNode(self, node):
        if not isinstance(node, IndexAccessNode):
            raise InternalException(f"Cannot use {node.__class__.__name__} in visit_IndexAccessNode", node)
        target_value = self.evaluate(node.target)
        index = self.evaluate(node.index)
        if not isinstance(target_value, (list, ChestnutList)) and not isinstance(target_value, (tuple, ChestnutTuple)) and not isinstance(target_value, str) and not isinstance(target_value, ChestnutString):
            raise Exception(f"Index access attempted on non-array type {target_value.__repr__()}")

        if index == index.__class__(-1):
            index = index.__class__(len(target_value) - 1)
        if index < index.__class__(0) or index >= index.__class__(len(target_value)):
            raise Exception(f"Index out of bounds")
        return target_value[index]

    def visit_ExpressionStatementNode(self, node):
        return self.evaluate(node.expression)

    def visit_ReturnStatementNode(self, node):
        return_value = None
        if node.expression:
            return_value = self.evaluate(node.expression)
        raise ReturnValue(return_value)

    def visit_ConstantStatementNode(self, node):
        labels = node.label
        if not isinstance(node.label, ChestnutTuple):
            labels = [node.label]

        for l in labels:
            if self.exists_in_any_scope(l.data):
                raise RuntimeException(f"`{l.data}` is already declared elsewhere", l)

        expression = self.evaluate(node.expression)
        if not isinstance(expression, ChestnutTuple):
            expression = [expression]

        i = 0
        while i < len(labels):
            setattr(expression[i], "constant", True)
            self.current_scope()[f"{labels[i].data}"] = expression[i]
            i = i + 1

        return 1

    def visit_LetStatementNode(self, node):
        labels = node.label
        if not hasattr(node.label, "__iter__"):
            labels = [node.label]

        for l in labels:
            if not self.calling_builtin:
                if self.exists_in_any_scope(l.data):
                    raise RuntimeException(f"Cannot redeclare {l.data}", l)

        expression = self.evaluate(node.expression)
        if not isinstance(expression, ChestnutTuple):
            expression = [expression]

        i = 0
        while i < len(labels):
            if isinstance(expression[0], tuple):
                self.current_scope()[labels[i].data] = expression[0][i]
            else:
                self.current_scope()[labels[i].data] = expression[i]
            i = i + 1

        return 1

    def visit_ShadowStatementNode(self, node):
        labels = node.label
        if not isinstance(node.label, list):
            labels = [node.label]
        for l in labels:
            var_scope = self.find_first_scope_containing(l.data)
            if var_scope is None:
                raise RuntimeException(f"Cannot shadow undeclared {l.data}", l)

            if hasattr(var_scope[l.data], "constant"):
                raise RuntimeException(f"Cannot shadow constant {l.data}", l)

            if l.data in self.current_scope():
                raise RuntimeException(f"Cannot shadow {l.data} because it was declared or redeclared  in the same scope.")

        expression = self.evaluate(node.expression)
        if not isinstance(expression, tuple):
            expression = [expression]

        i = 0
        while i < len(labels):
            if isinstance(expression[0], tuple):
                self.current_scope()[labels[i].data] = expression[0][i]
            else:
                self.current_scope()[labels[i].data] = expression[i]
            i = i + 1

        return 1

    def visit_FnStatementNode(self, node):
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
        self.function_register.register(func_object)
        scope = self.find_first_scope_containing(node.name.data)
        if scope is not None:
            if hasattr(scope[node.name.data], "constant"):
                raise Exception(f"Function definition for `{node.name.data}` conflicts with a constant at line {node.name.line}, column {node.name.column}")
        # if self.exists_in_any_scope(node.name.data):
        #     raise Exception(f"{node.name.data} is already defined in the current scope, line {node.name.line}, column {node.name.column}")
        self.current_scope()[node.name.data] = func_object

        return 1

    def visit_AnonymousFnExpressionNode(self, node):
        return AnonymousFunction(node)

    def visit_CallStatementNode(self, node):
        callable = self.evaluate(node.identifier)
        if not isinstance(callable, (Function, AnonymousFunction, BridgeFunction, StructNode, StructMethodCall)):
            raise RuntimeException(f"Attempt to call non-callable type {str(callable)}")
        self.calling_builtin = False
        identifier = None
        func = None
        instance = None
        # if isinstance(callable, StructNode):
        #     method = "constructor"
        #     func = callable.function_register.resolve(method, [ self.evaluate(x) for x in node.params ])
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
            # l = self.function_register.resolve(identifier, [ self.evaluate(x) for x in node.params ])
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

        if not isinstance(func, Function) and not isinstance(func, AnonymousFunction) and not isinstance(func, BridgeFunction):
            # Block function calls to other stored data.
            raise Exception(f"Call to non-function `{identifier}` at line {node.identifier.line}, column {node.identifier.column}")
        if isinstance(func, BridgeFunction):
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

            return result

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
            print(node.identifier.__class__.__name__)
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

    def visit_BreakStatementNode(self, node):
        raise BreakLoop(node)

    def visit_ContinueStatementNode(self, node):
        raise ContinueLoop(node)

    def visit_Token(self, node):
        if not isinstance(node, Token):
            raise InternalException(f"Cannot use visit_Token with { node.__class__.__name__}", node)
        if node.label != "Identifier":
            raise InternalException(f"Expected Identifier token, got {node.__class__.__name__}", node)

        label = node.data

        stored_scope = self.find_first_scope_containing(label)
        if stored_scope is None:
            raise Exception(f"Couldn't find symbol {label} at line {node.line}, column {node.column}")
        result = stored_scope[label]
        if isinstance(result, BringVariable):
            return result.__getitem__(None)

        return result

    def visit_IfStatementNode(self, node):
        if self.evaluate(node.condition_expression):
            self.push_scope()
            for statement in node.block_statements:
                self.evaluate(statement)
            self.pop_scope()
            return
        for elif_block in node.elif_blocks:
            if self.evaluate(elif_block.condition_expression):
                self.push_scope()
                for statement in elif_block.block_statements:
                    self.evaluate(statement)
                self.pop_scope()
                return
        if node.else_block:
            self.push_scope()
            for statement in node.else_block.block_statements:
                self.evaluate(statement)
            self.pop_scope()
        return

    def visit_CaseStatementNode(self, node):
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

    def visit_IterateStatementNode(self, node):
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

    def visit_WhileStatementNode(self, node):
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

    def visit_UntilStatementNode(self, node):
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

    def visit_LoopindexExpressionNode(self, node):
        scope = self.find_first_scope_containing("loop index")
        if scope is None:
            raise Exception(f"`loop_index` keyword must be used inside a loop")
        return scope["loop index"]

    def visit_UseExpressionNode(self, node):
        if not node.condition is None:
            if self.evaluate(node.condition):
                return self.evaluate(node.right)
            return self.evaluate(node.left)
        else:
            left = self.evaluate(node.left)
            if isinstance(left, ChestnutNull):
                return self.evaluate(node.right)
            return left

    def _handle_assign_Assignment(self, scope, label, expression):
        if isinstance(scope[label], BringVariable):
            scope[label].__setitem__(None, expression)
        else:
            scope[label] = expression

    def _handle_assign_Addassign(self, scope, label, expression):
        scope[label] += expression

    def _handle_assign_Subassign(self, scope, label, expression):
        scope[label] -= expression

    def _handle_assign_Mulassign(self, scope, label, expression):
        scope[label] *= expression

    def _handle_assign_Divassign(self, scope, label, expression):
        scope[label] /= expression

    def visit_AssignStatementNode(self, node):
        label = node.identifier.data


        if not self.exists_in_any_scope(node.identifier.data):
            raise Exception(f"Undeclared identifier {label} at line {node.identifier.line}, column {node.identifier.column}")

        scope = self.find_first_scope_containing(label)
        if hasattr(scope[label], "constant"):
            raise Exception(f"Cannot assign to constant `{label}` at line {node.identifier.line}, column {node.identifier.column}")

        if isinstance(node, AnonymousFunction):
            node.name = label
        expression = self.evaluate(node.expression)

        op = node.op
        method = f"_handle_assign_{op.label}"

        if hasattr(self, method):
            getattr(self, method)(scope, label, expression)
        else:
            return 0
        return 1

    def _handle_binary_Eq(self, left, right):
        return left == right

    def _handle_binary_Neq(self, left, right):
        return left != right

    def _handle_binary_Lte(self, left, right):
        return left <= right

    def _handle_binary_Lt(self, left, right):
        return left < right

    def _handle_binary_Gt(self, left, right):
        return left > right

    def _handle_binary_Gte(self, left, right):
        return left >= right

    def _handle_binary_And(self, left, right):
        return left and right

    def _handle_binary_Or(self, left, right):
        return left or right

    def _handle_binary_BitwiseAnd(self, left, right):
        return left & right

    def _handle_binary_BitwiseOr(self, left, right):
        return left | right

    def _handle_binary_BitwiseNand(self, left, right):
        return ~(left & right)

    def _handle_binary_BitwiseXor(self, left, right):
        return left ^ right

    def _handle_binary_BitwiseNor(self, left, right):
        return ~(left | right)

    def _handle_binary_BitwiseXnor(self, left, right):
        return ~(left ^ right)

    def _handle_binary_BitwiseShiftLeft(self, left, right):
        return left << right

    def _handle_binary_BitwiseShiftRight(self, left, right):
        return left >> right

    def _handle_binary_BitwiseRotateLeft(self, left, right):
        return left.lrotate(right)

    def _handle_binary_BitwiseRotateRight(self, left, right):
        return left.rrotate(right)

    def _handle_binary_Addition(self, left, right):
        return left + right

    def _handle_binary_Subtraction(self, left, right):
        return left - right

    def _handle_binary_Multiplication(self, left, right):
        return left * right

    def _handle_binary_Division(self, left, right):
        return left / right

    def _handle_binary_Modulo(self, left, right):
        return left % right

    def _handle_binary_Exponent(self, left, right):
        return left ** right

    def visit_BinaryOperationNode(self, node):
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)
        op = node.op
        method = f"_handle_binary_{op.label}"

        if hasattr(self, method):
            return getattr(self, method)(left, right)
        else:
            raise RuntimeException(f"Cannot use visit_BinaryOperationNode with operation {op.label}", op)

    def evaluate(self, node):
        visitor_method = f"visit_{node.__class__.__name__}"
        if hasattr(self, visitor_method):
            return getattr(self, visitor_method)(node) 
        else:
            raise RuntimeException(f"Can't evaluate unknown node type {type(node)}")
