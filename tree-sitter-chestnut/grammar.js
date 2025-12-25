module.exports = grammar({
  name: 'chestnut',

  extras: $ => [
    /\s/,
    $.comment,
  ],
  conflicts: $ => [
    [$.parameter_list, $.type_identifier], // Add this line
    [$.parameter_list, $._receiver],       // If you added the _receiver rule
    [$.call_expression, $.tuple_literal],
  ],

  word: $ => $.identifier,

  rules: {
    source_file: $ => repeat($._definition),

    _definition: $ => choice(
      $.import_statement,
      $.struct_definition,
      $.function_definition,
      $.constant_definition,
      $._statement
    ),

    // --- Top Level Definitions ---

    import_statement: $ => seq('import', $.string),

    struct_definition: $ => seq(
      'struct',
      $.identifier,
      optional(seq('inherits', '(', commaSep1($.identifier), ')')),
      repeat($.struct_property),
      'endstruct'
    ),

    struct_property: $ => seq(
      field('name', $.identifier),
      ':',
      $.type_identifier
    ),

    function_definition: $ => choice(
      $.function,
      $.anonymous_function,
      $.struct_function
    ),

    // Standard named function: fn my_func(a, b)
    function: $ => seq(
      'fn',
      field('name', $.identifier),
      $.parameter_list,
      $._function_body
    ),

    // Anonymous function: fn(a, b)
    // We give this a lower precedence so 'fn (' prefers struct_function if possible
    anonymous_function: $ => prec(-1, seq(
      'fn',
      $.parameter_list,
      $._function_body
    )),

    // Struct/Method function: fn(u: User) my_func(a, b)
    struct_function: $ => seq(
      'fn',
      $._receiver,
      field('name', $.identifier),
      $.parameter_list,
      $._function_body
    ),

    _receiver: $ => seq(
      '(',
      choice(
        seq($.identifier, ':', $.type_identifier),
        $.type_identifier
      ),
      ')'
    ),

    // Shared body logic to keep code DRY
    _function_body: $ => seq(
      optional(seq('brings', '(', commaSep1($.identifier), ')')),
      optional(seq('returns', commaSep1($.type_identifier))),
      repeat($._statement),
      'endfn'
    ),

    constant_definition: $ => seq('constant', $.identifier, '=', $._expression),

    // --- Statements ---

    _statement: $ => choice(
      $.let_statement,
      $.shadow_statement,
      $.assignment_statement,
      $.if_statement,
      $.while_loop,
      $.until_loop,
      $.for_loop,
      $.loop_loop,
      $.case_statement,
      $.return_statement,
      $.break_statement,
      $.expression_statement
    ),

    let_statement: $ => seq(
      'let',
      commaSep1($.identifier),
      optional(seq(':', $.type_identifier)),
      '=',
      $._expression
    ),

    shadow_statement: $ => seq('shadow', $.identifier, '=', $._expression),

    assignment_statement: $ => seq(
      choice($.identifier, $.member_expression, $.subscript_expression),
      '=',
      $._expression
    ),

    if_statement: $ => seq(
      'if', $._expression,
      repeat($._statement),
      repeat(seq('elif', $._expression, repeat($._statement))),
      optional(seq('else', repeat($._statement))),
      'endif'
    ),

    while_loop: $ => seq('while', $._expression, repeat($._statement), 'endwhile'),

    until_loop: $ => seq('do', repeat($._statement), 'until', $._expression),

    for_loop: $ => seq('for', $._expression, 'as', $.identifier, repeat($._statement), 'endfor'),

    loop_loop: $ => seq('loop', repeat($._statement), 'endloop'),

    case_statement: $ => seq(
      'case', $._expression,
      repeat1(seq('when', $._expression, repeat($._statement))),
      optional(seq('otherwise', repeat($._statement))),
      'endcase'
    ),

    return_statement: $ => prec.left(seq(
      'return',
      optional($._expression)
    )),

    break_statement: $ => 'break',

    expression_statement: $ => $._expression,

    // --- Expressions ---

    _expression: $ => choice(
      $.identifier,
      $.number,
      $.string,
      $.boolean,
      $.null,
      $.list_literal,
      $.tuple_literal,
      $.binary_expression,
      $.unary_expression,
      $.call_expression,
      $.member_expression,
      $.subscript_expression,
      $.use_expression,
      $.interpolation,
      $.parenthesized_expression
    ),

    binary_expression: $ => choice(
      ...[
        ['**', 14],
        ['*', 13], ['/', 13], ['%', 13],
        ['+', 12], ['-', 12],
        ['<<', 11], ['>>', 11], ['<<<', 11], ['>>>', 11],
        ['<', 10], ['<=', 10], ['>', 10], ['>=', 10],
        ['==', 9], ['!=', 9],
        ['&', 8], ['~&', 8],
        ['^', 7], ['~^', 7],
        ['|', 6], ['~|', 6],
        ['and', 5],
        ['or', 4],
        ['xor', 4]
      ].map(([op, precedence]) => prec.left(precedence, seq(
        $._expression,
        op,
        $._expression
      )))
    ),

    unary_expression: $ => choice(
      prec(15, seq('-', $._expression)),
      prec(15, seq('not', $._expression)),
      prec(15, seq('~', $._expression)),
      prec(15, seq('outer', $.identifier)),
      prec(15, seq('spread', $._expression))
    ),
    use_expression: $ => prec.right(seq(
      'use', $._expression,
      'over', $._expression,
      optional(seq('unless', $._expression))
    )),

    call_expression: $ => prec(16, seq(
      $._expression,
      '(',
      commaSep(choice($._expression, seq('spread', $._expression))),
      ')'
    )),

    member_expression: $ => prec(17, seq($._expression, '.', $.identifier)),

    subscript_expression: $ => prec(17, seq($._expression, '[', $._expression, ']')),

    // --- Literals & Fragments ---

    parameter_list: $ => seq(
      '(',
      commaSep(seq(optional('variadic'), $.identifier, optional(seq(':', $.type_identifier)), optional(seq('=', $._expression)))),
      ')'
    ),

    list_literal: $ => seq('[', commaSep($._expression), ']'),

    tuple_literal: $ => prec(1, seq('(', commaSep1($._expression), ')')),

    interpolation: $ => seq('{{', $._expression, '}}'),

    parenthesized_expression: $ => prec(2, seq('(', $._expression, ')')),

    type_identifier: $ => $.identifier,

    identifier: $ => /[a-zA-Z_][a-zA-Z0-9_]*/,

    number: $ => /\d+(\.\d+)?/,

    string: $ => choice(
      seq('"', repeat(choice(/[^"\\]/, $.escape_sequence)), '"'),
      seq("'", repeat(choice(/[^'\\]/, $.escape_sequence)), "'"),
      seq('`', repeat(/[^`]/), '`')
    ),
    escape_sequence: $ => token(seq(
      '\\',
      choice(
        /[^xuU]/,                // Single characters like \n, \t, \\, \", \'
        /x[0-9a-fA-F]{2}/,       // Hex: \xff
        /u[0-9a-fA-F]{4}/,       // Unicode: \uabcd
        /U[0-9a-fA-F]{8}/        // Unicode: \U0010ffff
      )
    )),

    boolean: $ => choice('true', 'false'),

    null: $ => 'null',

    comment: $ => choice(
      seq('#', /.*/),
      seq('###', repeat(choice(/[^#]/, /#[^#]/, /##[^#]/)), '###')
    ),
  }
});

function commaSep(rule) {
  return optional(commaSep1(rule));
}

function commaSep1(rule) {
  return seq(rule, repeat(seq(',', rule)));
}
