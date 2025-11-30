#include <ctype.h>
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

typedef enum {
    // Type token types
    TK_NULL,
    TK_INT,
    TK_INT8,
    TK_INT16,
    TK_INT32,
    TK_INT64,
    TK_UINT8,
    TK_UINT16,
    TK_UINT32,
    TK_UINT64,
    TK_FLOAT,
    TK_FLOAT32,
    TK_FLOAT64,
    TK_BOOL,
    TK_STR,
    TK_CALL_DEPTH,
    TK_LOOP_INDEX,
    TK_ENDSTRUCT,
    TK_OTHERWISE,
    TK_CONSTANT,
    TK_CONTINUE,
    TK_ENDWHILE,
    TK_VARIADIC,
    TK_ENDCASE,
    TK_ENDLOOP,
    TK_RETURNS,
    TK_BRINGS,
    TK_ENDFOR,
    TK_IMPORT,
    TK_RETURN,
    TK_SHADOW,
    TK_SPREAD,
    TK_STRUCT,
    TK_UNLESS,
    TK_BREAK,
    TK_ENDFN,
    TK_ENDIF,
    TK_OUTER,
    TK_UNTIL,
    TK_WHILE,
    TK_CASE,
    TK_ELIF,
    TK_ELSE,
    TK_LOOP,
    TK_OVER,
    TK_WHEN,
    TK_FOR,
    TK_LET,
    TK_USE,
    TK_DO,
    TK_IF,
    TK_OP_IPA_ADD,
    TK_OP_IPA_SUB,
    TK_OP_IPA_MUL,
    TK_OP_IPA_DIV,
    TK_OP_IPA_EXP,
    TK_OP_IPA_MOD,
    TK_OP_NOT,
    TK_OP_AND,
    TK_OP_OR,
    TK_OP_LTE,
    TK_OP_LT,
    TK_OP_EQ,
    TK_OP_NEQ,
    TK_OP_GT,
    TK_OP_GTE,
    TK_OP_EXP,
    TK_OP_BIN_ROTL,
    TK_OP_BIN_ROTR,
    TK_OP_BIN_SHTL,
    TK_OP_BIN_SHTR,
    TK_OP_BIN_AND,
    TK_OP_BIN_OR,
    TK_OP_BIN_XOR,
    TK_OP_BIN_NOT,
    TK_OP_BIN_NAND,
    TK_OP_BIN_NOR,
    TK_OP_BIN_XNOR,
} TokenType;

typedef union {
    // Integer    
    int8_t i8;
    int16_t i16;
    int32_t i32;
    int64_t i64;

    // UnsignedInteger
    uint8_t u8;
    uint16_t u16;
    uint32_t u32;
    uint64_t u64;

    // Boolean
    bool boolean;

    // String
    char* str;
} TokenData;

typedef struct {
    uint64_t line;
    uint64_t col;
} Location;

typedef struct {
    TokenType type;
    TokenData data;
    Location location;
} Token;

int main() {
    FILE *fptr = fopen("../examples/hello.nuts", "r");
    char data[50];
    if (fptr == NULL) {
        printf("The file couldn't be opened.");
        return -1;
    }
    while(fgets(data, 50, fptr) != NULL) {
        printf("%s", data);
    }
    fclose(fptr);
    return 0;
}
