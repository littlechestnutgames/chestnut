I am working on programming a new programming language called Chestnut.

Chestnut:
* Is written in python.
* Enforces lexical scoping strictly. Even if statements don't leak scope.
* Want to make lumpy a general purpose programming language.
* Want Chestnut to have an interpreter.
* Want Chestnut to have a REPL.
* Want Chestnut to have a compiler.

Roadmap:
1. [x] Write lexer
2. [x] Write parser
3. [ ] Write evaluator # Underway
4. [ ] Write interpreter interface
5. [ ] Write REPL
6. [ ] Write codegen using LLVM lib
7. [ ] Write compile functions.
8. [ ] Produce bootstrapping compiler.
9. [ ] Self-host by starting the list over from 1 in Chestnut.

The lexer outputs tokens like {label: "LParen", data: "("} and {label: "Float", data: 3.14}

For the below tokens, see the syntax section for usage for the tokens.

Tokens supposed are:
* Null - The null
* Eq - This is ==
* Neq - This is !=
* Lte - This is <=
* Lt - This is <
* Gte - This is >=
* Gt - This is >
* Nand - This is nand
* And - This is and
* Xnor - This is xnor
* Xor - This is xor
* Nor - This is nor
* Not - This is both both not and !
* Or - This is or
* Addassign - This is +=
* Subassign - This is -=
* Mulassign - This is *=
* Divassign - This is /=
* Assignment - This is =
* Negation - This is -
* Addition - This is +
* Division - This is /
* Multiplication - This is *
* Modulo - This is % and mod
* Exponent - This is ^
* Let - This is let
* Print - This is print
* Spread - This is spread
* Use - This is use
* Over - This is over
* Unless - This is unless
* Endif - This is endif
* Elif - This is elif
* If - This is if
* Then - This is then
* Else - This is else
* Endcase - This is endcase
* Case - This is case
* When - This is when
* Otherwise - This is otherwise
* Enduntil - This is enduntil
* Until - This is until
* Repeat - This is repeat
* Enditerate - This is enditerate
* Iterate - This is iterate
* With - This is with
* Endfn - This is endfn
* Fn - This is fn
* Returns - This is retuns
* Return - This is return
* Variadic - This is variadic
* Boolean - This is true or false
* LParen - This is (
* RParen - This is )
* LBrace - This is [
* RBrace - This is ]
* Colon - This is :
* Comma - This is ,
* String - This is "like this"
* Hex - This is like 0x0914
* Octal - This is like 0o123
* Binary - This is like 0b1010
* Float - This is like 3.14
* Integer - This is like 9184
* Identifier - This is everything else.

The parser turns this token stream and produces an abstract syntax tree. I list of statements.

The AST nodes are:
* UnaryOperationNode - Represents a unary operation such as not or negative numbers.
* BinaryOperationNode - Represents a binary function such as addition and subtraction.
* LetStatementNode - Represents a declaration and assignment of a variable.
* PrintStatementNode - Represents a print statement.
* IfStatementNode - Is the if block. Contains a condtion and all ElifStatementNodes and ElseStatementNode if present.
* ElifStatementNode - These get nested inside the if.
* ElseStatementNode - These get nesetd inside the if.
* FnStatementNode - Defines a function with label.
* AnonymousFnExpressionNode - Defines an anonymous function.
* FnParameter - These go in FnStatementNodes and AnonymousFnExpressionNodes
* CaseStatementNode - The state of a case statement. Contains a condition and all the when blocks and possibly an otherwise block.
* WhenStatementNode - These go inside the case statements.
* OtherwiseStatementNode - This goes inside the case statement.
* UntilStatementNode - A loop construct.
* IterateStatementNode - Another loop construct
* ReturnStatementNode - The return statement of a function.
* AssignStatementNode - Reassign variables
* UseExpressionNode() - A default and ternary statement.
* CallStatementNode - Represents a call made to a function.
* ExpressionStatementNode - Expression wrapper.
* ConstantStatementNode - Like let, but for constants.
* ShadowStatementNode - Like let, but for shadowing ONLY.
* ListLiteralNode - For lists.
* IndexAccessNode - For conveying access to list items by index.

Let expressions look like this:
let a = "Test"
let a : String = "Test"
let a : Integer
etc

And (re)assignment expressions
a = "Test"
a = 1
etc

If statements look like this
if condition_expression then
    # statements
elif condition_expression then
    # statements
else
    # statements
endif

Case statements look like this
case expression
    when expression
    when other_expression
        # statements
    otherwise
        # statement
endif

Until statements look like this
until expression repeat
    # statements
enduntil

Iterate statements look like this
iterate expression with identifer
    # statements
enditerate

Function creation is done this way.
fn my_func(param1 : Type, param2 : Type) returns AType
    # statements
    return value
endfn

But returns are optional
fn my_func()
    # statements
endfn

A parameter in a function may be declared variadic. Only the last parameter may do so.
fn my_variadic_func(param1 : Integer, variadic my_params : String)
    # statements
endfn

A user can spread iterables into variadic parameters on call.
my_variadic_func(spread(my_list))

A form of default and ternary is supposed in the `use` statment.

If you wanted to default a variable to another value if the first is falsey, you'd do:
let a = use b over c # If b is falsey, a is equal to c, otherwise b will be used.

If you wanted to assign a variable based on a condition in a single line, this is the ternary use of `use`.
let a = use b over c unless c > 50

You can define an anonymous function with the following syntax
let str_join =
    fn (variadic params : String) returns String
        let str = ""
        iterate params with param
            if length(str) > 0 then
                str += ", "
            endif
            str += param
        enditerate

        return str
    endfn

Most of the mathy or programming symbols are binary infix, some are unary prefixes.

Shadowing. Any developer worth their salt will know that shadowing variables is borrowing trouble, so in Chestnut, I'm disabling shadowing with the `let` syntax.

If the user tries to shadow a variable, they will be met with an exception message explaining the next concept.

We need shadowing sometimes. And I've disabled it. What now? I've disabled implicit shadowing, but I've opened up a way to explicitly shadow.

If the user wants to shadow a variable, they must use the `shadow` keyword instead of the `let` keyword.

let x = 0
let my_list = [1, 2, 3, 4]
iterate my_list with item
    let x = x + item # This will trigger an error.
    print(item)
enditerate

let x = 0
let my_list = [1, 2, 3, 4]
iterate my_list with item
    shadow x = x + item # This will NOT trigger an error.
    print(item)
enditerate

`shadow` comes with a few rules of it's own though.

1. shadowed variables MUST exist in a parent scope.
2. Variables cannot shadow themselves the scope they were defined.
