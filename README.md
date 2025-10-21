# Chestnut Reference

## I. Core Design Philosophy

Chestnut is a general-purpose programming language that aims to be robust and prose-like.

* **Implementation:** Currently written in Python, but the future goal is **LLVM IR** and self-hosting.
* **Parsing:** Chestnut uses a left-to-right, **recursive descent LL parser** to lex and parse tokens into an Abstract Syntax Tree.
* **Whitespace:** It is not whitespace sensitive (aside from the newline at the end of a single line comment)
* **Comments:**
    * **Inline:** # Inline comments start with a hash sign.
    * **Multi-line:** ### Multi-line comments start with three hash signs and end with three hash signs. ###

## II Types

| Type    | Example(s)     | Notes                                    |
| ------- | -------------- | ---------------------------------------- |
| Any     | 0              | Represents ANY value. Even null.         |
| Null    | null           | For now. Maybe Removed later.            |
| String  | "Hello"        |                                          |
| Boolean | true, false    |                                          |
| Integer | 10             | Inferred type of any non-decimal number. |
| Float   | 3.14           | Inferred type of any decimal number.     |
| List    | [1, 2, 3]      | Provides index access and assignment     |
| Tuple   | (1, 2, 3)      | Provides index access. Immutable.        |
| Error   | error("Error") | A way to provide errors                  |


## III. Variable declaration

### let / shadow / constant

Chestnut enforces strict lexical scoping, forcing developers to be clear and intentional with declaration.

| Keyword    | Purpose                                   | Rule                                                                   |
| ---------- | ----------------------------------------- | ---------------------------------------------------------------------- |
| `let`      | Standard variable declaration.            | Can't be used to shadow variables.                                     |
| `shadow`   | Redeclaration of a non-constant variable. | **Must** be used to shadow an already declared, non-constant variable. |
| `constant` | Declaration of a constant variable.       | **Cannot** be overwritten.                                             |

#### Usage:

```
# let syntax
let my_var = "Hello, world!" # This variable doesn't have an explicit type.
let my_var2 : String = "Hi!" # This variable has String type.
let my_var = 1               # This is an illegal shadowing of my_var.

# shadow syntax
shadow my_var = 1            # This is an illegal shadowing. It took place in the same scope as declaration.
if condition_expression then
    shadow my_var = 1        # This sets my_var in this scope to 1 with an inferred type of Integer.
    shadow my_var2 = false   # This sets my_var2 in this scope to false with an inferred type of Boolean.
endif

# constant syntax
constant PI = 3.141519           # This sets PI to 3.141519 with an inferred type of Float
```

## IV. Operators

### Assignment Operators

The usual operators are all here. The caveat is that they may not be used on undeclared variables.

| Operator | Purpose                      | Example |
| -------- | ---------------------------- | ------- |
| =        | Simple assignment            |  a = 5  |
| +=       | Add in-place assignment      | a += 5  |
| -=       | Subtract in-place assignment | a -= 5  |
| *=       | Multiply in-place assignment | a *= 5  |
| /=       | Divide in-place assignment   | a /= 5  |

### Mathematical Operators

| Operator | Purpose                        | Example | Result |
| -------- | ------------------------------ | ------- | ------ |
| +        | Addition, String concatenation |  15 + 5 |     20 |
| -        | Subtraction                    |  15 - 5 |     10 |
| *        | Multiplication                 |  15 * 5 |     75 |
| /        | Division                       |  15 / 5 |      3 |
| %        | Modulo                         |  15 % 5 |      0 |
| **       | Exponent                       | 15 ** 5 | 759375 |

### Boolean Operators

| Operator | Purpose               | Example    |
| -------- | --------------------- | ---------- |
| and      | Logical and           | a and b    |
| &&       | Logical and           | a && b     |
| or       | Logical or            | a || b     |
| not      | Logical not           | not a      |
| !        | Logical not           | !a         |
| ==       | Equality              | a == b     |
| !=       | Inequality            | a != b     |
| <        | Less than             | a < b      |
| <=       | Less than or equal    | a <= b     |
| >        | Greater than          | a > b      |
| >=       | Greater than or equal | a >= b     |
| xor      | Logical xor function  | xor(a, b)  |
| nand     | Logical nand function | nand(a, b) |
| nor      | Logical nor function  | nor(a, b)  |
| xnor     | Logical xnor function | xnor(a, b) |

Those last four aren't infix to not have them confused with the bitwise operators, which I'll go into next.

### Bitwise Operators

| Operator | Purpose      | Example     | Result     |
| -------- | ------------ | ----------- | ---------- |
|  ~       | Not          |        ~0xa |        -11 |
|  &       | And          |  0xa &  0x3 |          2 |
| \|       | Or           | 0xa \|  0x3 |         11 |
|  ^       | Xor          |  0xa ^  0x3 |          9 |
| ~&       | Nand         | 0xa ~&  0x3 |         -3 |
| ~\|      | Nor          | 0xa ~\| 0x3 |        -12 |
| ~^       | Xnor         | 0xa ~^  0x3 |        -10 |
| <<       | Shift left   | 0xa <<    3 |         80 |
| >>       | Shift right  | 0xa >>    3 |          1 |
| <<<      | Rotate left  | 0xa <<<   3 |         80 |
| >>>      | Rotate right | 0xa >>>   3 | 1073741825 |

* **Rotate left** and **rotate right** are not yet implemented.

## V. Control Flow Statements

### if / elif / else / endif

if statements begin with `if` and end with `endif`. In between there are optional `elif` blocks and an optional `else` block as well.

#### Usage

```
if condition_expression then
    # Inside these blocks is an isolated scope.
    # This is where your statements go.
elif condition_expression2 then
    # More statements
else
    # Even more statements
endif
```

### case / when / otherwise / endcase

case statements start with `case` and end with `endcase`. In between are `when`, which can be grouped together and an optional `otherwise` block.

#### Usage

```
case expression
when condition_expression
    # Statements here
when condition_expression2
when condition_expression3
    # Other statements here.
otherwise
    # Fall-though statements here.
endcase
```

### use / over / unless

use statements serve **two** purposes.

1. A **null** coalescing expression.
2. A **ternary** statement.

#### Usage

```
let a = null
let b = 10

# This is an example of null coalescing. c is equal to 10.
let c = use a over b 

# This is an example of a ternary. d is equal to null because b is greater than or equal to 10.
let d = use a over b unless b >= 10 
```

## VI. Looping

### iterate / with / enditerate & continue

An **iterate** statement loops over a List, Tuple, or String type. The `with` keyword specifies the local reference.

The following example also introduces the **continue** keyword, which skips the rest of the loop and goes to the next iteration.

#### Usage

```
let my_numbers = [3, 2, 1]
iterate my_numbers with number
    print(number)
enditerate

let my_numbers2 = (1, 2, 3)
iterate my_numbers2 with number
    print(number)
enditerate

# An extremely simplistic lexer.
let my_string = "let my_string = \"Hello, world\" "
let tokens = []
let collected = ""
iterate my_string with chr
    if chr == " " then
        if collected == "let" then
            push(tokens, ["let", collected])
            collected = ""
            continue
        elif collected[0] == "\"" and collected[length(collected)-1] == "\"" then
            push(tokens, ["string", collected])
            collected = ""
            continue
        elif collected == "=" then
            push(tokens, ["equals", collected])
            collected = ""
            continue
        else
            push(tokens, ["identifier", collected])
            collected = ""
            continue
        endif
    endif
    collected += chr
enditerate
print(tokens[3]) # Prints "Hello, world"
```
### while & break

The **while** loop is a fairly traditional construct where the statements in the block repeat until the condition is false.

The following example also introduces the **break** keyword, which is used to break out of loops.

#### Usage:

```
let i = 10
while i > 0 repeat
    print(i)
    i -= 1
endwhile

while true repeat
    print("Looping")
    break
endwhile
```
### until & loop_index

The **until** loop is the invert of the while loop, where it loops until a condition is true.

The following example also introduces the **loop_index** keyword, as well as the **outer** unary as well as string interpolation.

1. **loop_index** is an automatically allocated counter for loop iterations available as a convenience in every loop type.
2. **outer** is a unary operator that allows you to fetch values from shadowed variables.
    1. In this example, loop_index is implicitly shadowed by the inner loop.
    2. To access the outer loop's loop_index inside the inner loop, we say `outer loop_index`.
    3. This is stackable, so `outer outer loop_index` would theoretically fetch a reference to loop_index two definitions backward.
    4. `outer` also works on other shadowed variables, not just `loop_index`.
3. **String interpolation** is a feature of strings that allow you to embed values or expressions inside strings.
    1. A string interpolation starts with `{{` and ends with `}}`.
    2. Inside, you can do simple replacement such as "{{ a }}" or complicated things like calling functions! "This is {{ my_func() }}!"

Without further adieu, the usage.

#### Usage:

```
until loop_index == 1 repeat
    until loop_index == 1 repeat
        print("Outer loop_index: {{ outer loop_index }}, Inner loop_index: {{ loop_index }} ")
    enduntil
enduntil
```

## VII. Structs

What good is a language if you can't structure data with it easily? Chestnut uses structs.

### Example:

```
struct MineralProperty
    name : String
    value : Any
endstruct

struct Mineral
    name : String
    properties : List
endstruct

let diamond = Mineral()
diamond.name = "Diamond"
diamond.properties = []

let diamond_hardness = MineralProperty()
diamond_hardness.name = "Hardness"
diamond_hardness.value = 10

push(diamond.properties, diamond_hardness)

print("{{ diamond.name }}: {{ diamond.properties[0].name }} - {{ diamond.properties[0].value }}") # Prints Diamond: Hardness - 10
```

## VIII. Functions

All functions in Chestnut are first-class functions. When a function is defined, it copies a reference to the scope it was born into. And when functions move beyond the call boundaries they were defined in, they can be recaptured by the parent scope. This means that you can return functions defined inside functions and other cool stuff.

In Chestnut, we have 3 types of functions.

1. Named functions.
    1. These functions are defined with a label.
    2. These are stand-alone statements.
2. Anonymous functions.
    1. These functions don't have a name.
    2. Anonymous functions can be assigned with **let** / **shadow** / **const**.
    2. These are expressions, but can be turned into a statement by calling them inline.
3. Struct functions.
    1. These functions are defined with a label and a struct type receiver.
    1. They are also stand-alone statements.

### Examples

```
fn basic()
    print("This is a super basic function. It takes no arguments.")
endfn

fn get_name_from_user(name : String)
    print("This function takes an argument, name, which is \"{{ name }}\".")
endfn

# This function returns a value.
fn add_float(a : Float, b : Float) returns Float
    return a + b
endfn

# This function uses a default value.
fn default_values(a : String, b : String = "None given")
    print(a, b)
endfn
```

These were all examples of named functions.

Default values can be specific as the above example, but they cannot appear before a required argument or on a **variadic**.
Variadic values allow the developer to use as many arguments of one type as they like for that parameter. Keep in mind, variadics can only appear once, as the last argument.

### Example
```
fn greet(variadic names : String)
    iterate names with name
        print("Hello {{ name }}. ")
    enditerate
endfn
greet("Chestnut", "User") # Prints Hello Chestnut. Hello User.
```

Anonymous functions are specified by leaving off the variable label. These are considered expressions, not full statements, so they can be assigned or used directly after creation.

### Example
```
let a = fn (variadic names : String)
    iterate names with name
        print("Hello {{ name }}. ")
    enditerate
endfn

a()

# This is an example of an inline anonymous function call.
print("{{ fn(name) returns String return "Hello, " endfn("world") }}")
```

Struct functions allow us to add methods to structs. Let's refer to the mineral code above and do something about that boilerplate.

```
fn new_mineral_type(name : String, value : Any) returns MineralType
    let mt = MineralType()
    mt.name = name
    mt.value = value

    return mt
endfn

fn new_mineral(name) returns Mineral
     let m = Mineral()
     m.name = name
     m.properties = []

     return m
endfn

# This next one is where the receiver pattern comes into play.
fn (m : Mineral) add_property(name : String, value : Any)
    push(m, new_mineral_type(name, value)
endfn

let diamond = new_mineral("Diamond")
let ruby = new_mineral("Ruby")
diamond.add_property("Hardness", 10)
ruby.add_property("Hardness", 7)

let minerals = [diamond, ruby]
iterate minerals with mineral
    print("{{ mineral.name }}: {{ mineral.properties[0].name }} - {{ mineral.properties[0].value }}")
enditerate
```

Ok. So, functions can have parameters that can default or be variadic return values, and even do a receiver pattern. What else?

Variable captures.

Functions are closures. To explicitly capture a variable from an external scope not in the closure's scope, use the `brings` keyword.

```
let a = 10
fn outer_func()
    fn brings_test(b : Integer) brings(a)
        print("a", a, "b", b, a * b)
    endfn
    brings_test(5)
endfn
outer_func()
```
The capture is done in a way that assures you that only that specific variable will be brought into the inner function scope.
