# A greeting function that prints Hello and a list of names.
fn greet (variadic names : String) returns String
    let str = "Hello "
    iterate names with name
        if str != "Hello " then
	    str = str + " and "
	endif
	str = str + name
    enditerate
    return str
endfn

# Tests local scope assignment
let greeting = greet("wizard", "the cat")
print("I am now going to greet you. " + greeting)

# Testing anonymous functions
let a = fn (name : String) print("Hello " + name) endfn
a("anonymous function call success.")

# Testing list iteration
let b = [1, 2, 3]
iterate b with num
    print("Testing list iteration: " + num)
enditerate
print("Testing index access: " + b[0])

# Testing shadowing
let x = 0
let my_list = [1, 2, 3, 4]
iterate my_list with item
    shadow x = x + item # This will NOT trigger an error.
    print("Testing shadowing " + x)
enditerate

