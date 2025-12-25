; --- Keywords & Control ---
[
  "if"
  "elif"
  "else"
  "endif"
  "case"
  "when"
  "otherwise"
  "endcase"
  "while"
  "endwhile"
  "do"
  "until"
  "for"
  "as"
  "endfor"
  "loop"
  "endloop"
  "return"
  (break_statement)
] @keyword.control

[
  "fn"
  "endfn"
  "struct"
  "endstruct"
  "import"
  "let"
  "shadow"
  "constant"
  "use"
  "over"
  "unless"
  "brings"
  "returns"
  "inherits"
  "variadic"
  "spread"
  "outer"
] @keyword

; --- Literals ---
(number) @number
(string) @string
(boolean) @boolean
(null) @constant.builtin

; --- Identifiers & Types ---
(type_identifier) @type
((identifier) @variable (#not-has-ancestor? @variable "type_identifier"))

; Function definitions
(function name: (identifier) @function)
(struct_function name: (identifier) @method)

; Function calls
(call_expression (identifier) @function.call)
(call_expression (member_expression (identifier) @method.call))

; --- Operators & Punctuation ---
[
  "="
  "=="
  "!="
  "+"
  "-"
  "*"
  "/"
  "%"
  "**"
  "<"
  "<="
  ">"
  ">="
  "and"
  "or"
  "xor"
  "not"
  "&"
  "|"
  "^"
  "~"
  "<<"
  ">>"
  "<<<"
  ">>>"
  "~&"
  "~|"
  "~^"
] @operator

[
  "("
  ")"
  "["
  "]"
  "{{"
  "}}"
] @punctuation.bracket

[
  "."
  ","
  ":"
] @punctuation.delimiter

; --- Comments ---
(comment) @comment @spell
