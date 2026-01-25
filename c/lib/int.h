#ifndef CHESTNUT_LIB_INT_H
#define CHESTNUT_LIB_INT_H

#include <stddef.h>
#include <stdint.h>

// Base primitives set.
typedef int8_t chestnut_int8_t;
typedef uint8_t chestnut_uint8_t;

typedef int16_t chestnut_int16_t;
typedef uint16_t chestnut_uint16_t;

typedef int32_t chestnut_int32_t;
typedef uint32_t chestnut_uint32_t;

typedef int64_t chestnut_int64_t;
typedef uint64_t chestnut_uint64_t;

// Extended primitives.
typedef struct {
    _Alignas(16) chestnut_uint64_t limbs[2];
} chestnut_uint128_t;

typedef struct {
    _Alignas(32) chestnut_uint64_t limbs[4];
} chestnut_uint256_t;

typedef struct {
    _Alignas(64) chestnut_uint64_t limbs[8];
} chestnut_uint512_t;

typedef struct {
    _Alignas(64) chestnut_uint64_t limbs[16];
} chestnut_uint1024_t;


// Extended int primitives
typedef struct {
    _Alignas(16) chestnut_uint64_t limbs[2];
} chestnut_int128_t;

typedef struct {
    _Alignas(32) chestnut_uint64_t limbs[4];
} chestnut_int256_t;

typedef struct {
    _Alignas(64) chestnut_uint64_t limbs[8];
} chestnut_int512_t;

typedef struct {
    _Alignas(64) chestnut_uint64_t limbs[16];
} chestnut_int1024_t;

// Arbitrary
typedef struct {
    chestnut_uint64_t *limbs;
    size_t limb_size;
} chestnut_uint_t;

typedef struct {
    chestnut_uint64_t *limbs;
    size_t limb_size;
} chestnut_int_t;

#endif
