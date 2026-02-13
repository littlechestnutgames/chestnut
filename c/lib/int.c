#ifndef CHESTNUT_INT_C
#define CHESTNUT_INT_C

#include "./int.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifdef _MSC_VER
        #include <intrin.h>
#endif

static inline __attribute__((always_inline)) chestnut_uint8_t __chestnut_add_overflow(
    const chestnut_uint8_t carry_in,
    const chestnut_uint64_t a,
    const chestnut_uint64_t b,
    chestnut_uint64_t *out
) {
    #if defined(__GNUC__) || defined(__clang__)
        chestnut_uint64_t partial;
        chestnut_uint8_t carry1 = __builtin_add_overflow(a, b, &partial);
        chestnut_uint8_t carry2 = __builtin_add_overflow(partial, (chestnut_uint64_t)carry_in, out); 
        return carry1 | carry2;
    #elif defined(_MSC_VER)
        return _addcarry_u64(carry_in, a, b, out);
    #else
        chestnut_uint64_t res = a + b;
        chestnut_uint8_t carry1 = (res < a);
        *out = res + carry_in;
        chestnut_uint8_t carry2 = (*out < res);
        return carry1 | carry2;
    #endif
}

chestnut_uint8_t chestnut_uint128_t_add(
    chestnut_uint128_t *out,
    const chestnut_uint128_t *a,
    const chestnut_uint128_t *b
) {
    chestnut_uint8_t carry = 0;
    carry = __chestnut_add_overflow(carry, a->limbs[0], b->limbs[0], &out->limbs[0]);
    carry = __chestnut_add_overflow(carry, a->limbs[1], b->limbs[1], &out->limbs[1]);
    return carry;
}

chestnut_uint8_t chestnut_uint256_t_add(
    chestnut_uint256_t *out,
    const chestnut_uint256_t *a,
    const chestnut_uint256_t *b
) {
    chestnut_uint8_t carry = 0;
    carry = __chestnut_add_overflow(carry, a->limbs[0], b->limbs[0], &out->limbs[0]);
    carry = __chestnut_add_overflow(carry, a->limbs[1], b->limbs[1], &out->limbs[1]);
    carry = __chestnut_add_overflow(carry, a->limbs[2], b->limbs[2], &out->limbs[2]);
    carry = __chestnut_add_overflow(carry, a->limbs[3], b->limbs[3], &out->limbs[3]);
    return carry;
}

chestnut_uint8_t chestnut_uint512_t_add(
    chestnut_uint512_t *out,
    const chestnut_uint512_t *a,
    const chestnut_uint512_t *b
) {
    chestnut_uint8_t carry = 0;
    carry = __chestnut_add_overflow(carry, a->limbs[0], b->limbs[0], &out->limbs[0]);
    carry = __chestnut_add_overflow(carry, a->limbs[1], b->limbs[1], &out->limbs[1]);
    carry = __chestnut_add_overflow(carry, a->limbs[2], b->limbs[2], &out->limbs[2]);
    carry = __chestnut_add_overflow(carry, a->limbs[3], b->limbs[3], &out->limbs[3]);
    carry = __chestnut_add_overflow(carry, a->limbs[4], b->limbs[4], &out->limbs[4]);
    carry = __chestnut_add_overflow(carry, a->limbs[5], b->limbs[5], &out->limbs[5]);
    carry = __chestnut_add_overflow(carry, a->limbs[6], b->limbs[6], &out->limbs[6]);
    carry = __chestnut_add_overflow(carry, a->limbs[7], b->limbs[7], &out->limbs[7]);
    return carry;
}

chestnut_uint8_t chestnut_uint1024_t_add(
    chestnut_uint1024_t *out,
    const chestnut_uint1024_t *a,
    const chestnut_uint1024_t *b
) {
    chestnut_uint8_t carry = 0;
    carry = __chestnut_add_overflow(carry, a->limbs[0], b->limbs[0], &out->limbs[0]);
    carry = __chestnut_add_overflow(carry, a->limbs[1], b->limbs[1], &out->limbs[1]);
    carry = __chestnut_add_overflow(carry, a->limbs[2], b->limbs[2], &out->limbs[2]);
    carry = __chestnut_add_overflow(carry, a->limbs[3], b->limbs[3], &out->limbs[3]);
    carry = __chestnut_add_overflow(carry, a->limbs[4], b->limbs[4], &out->limbs[4]);
    carry = __chestnut_add_overflow(carry, a->limbs[5], b->limbs[5], &out->limbs[5]);
    carry = __chestnut_add_overflow(carry, a->limbs[6], b->limbs[6], &out->limbs[6]);
    carry = __chestnut_add_overflow(carry, a->limbs[7], b->limbs[7], &out->limbs[7]);
    carry = __chestnut_add_overflow(carry, a->limbs[8], b->limbs[8], &out->limbs[8]);
    carry = __chestnut_add_overflow(carry, a->limbs[9], b->limbs[9], &out->limbs[9]);
    carry = __chestnut_add_overflow(carry, a->limbs[10], b->limbs[10], &out->limbs[10]);
    carry = __chestnut_add_overflow(carry, a->limbs[11], b->limbs[11], &out->limbs[11]);
    carry = __chestnut_add_overflow(carry, a->limbs[12], b->limbs[12], &out->limbs[12]);
    carry = __chestnut_add_overflow(carry, a->limbs[13], b->limbs[13], &out->limbs[13]);
    carry = __chestnut_add_overflow(carry, a->limbs[14], b->limbs[14], &out->limbs[14]);
    carry = __chestnut_add_overflow(carry, a->limbs[15], b->limbs[15], &out->limbs[15]);
    return carry;
}

void chestnut_uint_t_add(
    chestnut_uint_t *out,
    const chestnut_uint_t *a,
    const chestnut_uint_t *b
) {
}

static inline __attribute__((always_inline)) chestnut_uint8_t __chestnut_sub_overflow(
    const chestnut_uint8_t borrow_in,
    const chestnut_uint64_t a,
    const chestnut_uint64_t b,
    chestnut_uint64_t *out
) {
    #if defined(__GNUC__) || defined(__clang__)
        chestnut_uint64_t partial;
        chestnut_uint8_t borrow1 = __builtin_sub_overflow(a, b, &partial);
        chestnut_uint8_t borrow2 = __builtin_sub_overflow(partial, (chestnut_uint64_t)borrow_in, out);
        return borrow1 | borrow2;
    #elif defined(_MSC_VER)
        return _subborrow_u64(borrow_in, a, b, out);
    #else
        chestnut_uint64_t res = a - b;
        chestnut_uint8_t borrow1 = (a < b);
        *out = res - (chestnut_uint64_t)borrow_in;
        chestnut_uint8_t borrow2 = (res < (chestnut_uint64_t)borrow_in);
        return borrow1 | borrow2;
    #endif
}

chestnut_uint8_t chestnut_uint128_t_sub(
    chestnut_uint128_t *out,
    const chestnut_uint128_t *a,
    const chestnut_uint128_t *b
) {
    chestnut_uint8_t borrow = 0;
    borrow = __chestnut_sub_overflow(borrow, a->limbs[0], b->limbs[0], &out->limbs[0]);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[1], b->limbs[1], &out->limbs[1]);
    return borrow;
}

chestnut_uint8_t chestnut_uint256_t_sub(
    chestnut_uint256_t *out,
    const chestnut_uint256_t *a,
    const chestnut_uint256_t *b
) {
    chestnut_uint8_t borrow = 0;
    borrow = __chestnut_sub_overflow(borrow, a->limbs[0], b->limbs[0], &out->limbs[0]);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[1], b->limbs[1], &out->limbs[1]);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[2], b->limbs[2], &out->limbs[2]);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[3], b->limbs[3], &out->limbs[3]);
    return borrow;
}

chestnut_uint8_t chestnut_uint512_t_sub(
    chestnut_uint512_t *out,
    const chestnut_uint512_t *a,
    const chestnut_uint512_t *b
) {
    chestnut_uint8_t borrow = 0;
    borrow = __chestnut_sub_overflow(borrow, a->limbs[0], b->limbs[0], &out->limbs[0]);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[1], b->limbs[1], &out->limbs[1]);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[2], b->limbs[2], &out->limbs[2]);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[3], b->limbs[3], &out->limbs[3]);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[4], b->limbs[4], &out->limbs[4]);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[5], b->limbs[5], &out->limbs[5]);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[6], b->limbs[6], &out->limbs[6]);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[7], b->limbs[7], &out->limbs[7]);
    return borrow;
}

chestnut_uint8_t chestnut_uint1024_t_sub(
    chestnut_uint1024_t *out,
    const chestnut_uint1024_t *a,
    const chestnut_uint1024_t *b
) {
    chestnut_uint8_t borrow = 0;
    borrow = __chestnut_sub_overflow(borrow, a->limbs[0], b->limbs[0], &out->limbs[0]);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[1], b->limbs[1], &out->limbs[1]);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[2], b->limbs[2], &out->limbs[2]);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[3], b->limbs[3], &out->limbs[3]);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[4], b->limbs[4], &out->limbs[4]);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[5], b->limbs[5], &out->limbs[5]);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[6], b->limbs[6], &out->limbs[6]);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[7], b->limbs[7], &out->limbs[7]);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[8], b->limbs[8], &out->limbs[8]);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[9], b->limbs[9], &out->limbs[9]);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[10], b->limbs[10], &out->limbs[10]);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[11], b->limbs[11], &out->limbs[11]);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[12], b->limbs[12], &out->limbs[12]);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[13], b->limbs[13], &out->limbs[13]);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[14], b->limbs[14], &out->limbs[14]);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[15], b->limbs[15], &out->limbs[15]);
    return borrow;
}


chestnut_uint8_t chestnut_uint128_t_cmp_eq(
    const chestnut_uint128_t *a,
    const chestnut_uint128_t *b
) {
    chestnut_uint64_t diff = 0;
    diff |= a->limbs[0] ^ b->limbs[0];
    diff |= a->limbs[1] ^ b->limbs[1];
    return (chestnut_uint8_t)(((diff | -diff) >> 63) ^ 1);
}

chestnut_uint8_t chestnut_uint256_t_cmp_eq(
    const chestnut_uint256_t *a,
    const chestnut_uint256_t *b
) {
    chestnut_uint64_t diff = 0;
    diff |= a->limbs[0] ^ b->limbs[0];
    diff |= a->limbs[1] ^ b->limbs[1];
    diff |= a->limbs[2] ^ b->limbs[2];
    diff |= a->limbs[3] ^ b->limbs[3];
    return (chestnut_uint8_t)(((diff | -diff) >> 63) ^ 1);
}

chestnut_uint8_t chestnut_uint512_t_cmp_eq(
    const chestnut_uint512_t *a,
    const chestnut_uint512_t *b
) {
    chestnut_uint64_t diff = 0;
    diff |= a->limbs[0] ^ b->limbs[0];
    diff |= a->limbs[1] ^ b->limbs[1];
    diff |= a->limbs[2] ^ b->limbs[2];
    diff |= a->limbs[3] ^ b->limbs[3];
    diff |= a->limbs[4] ^ b->limbs[4];
    diff |= a->limbs[5] ^ b->limbs[5];
    diff |= a->limbs[6] ^ b->limbs[6];
    diff |= a->limbs[7] ^ b->limbs[7];
    return (chestnut_uint8_t)(((diff | -diff) >> 63) ^ 1);
}

chestnut_uint8_t chestnut_uint1024_t_cmp_eq(
    const chestnut_uint1024_t *a,
    const chestnut_uint1024_t *b
) {
    chestnut_uint64_t diff = 0;
    diff |= a->limbs[0] ^ b->limbs[0];
    diff |= a->limbs[1] ^ b->limbs[1];
    diff |= a->limbs[2] ^ b->limbs[2];
    diff |= a->limbs[3] ^ b->limbs[3];
    diff |= a->limbs[4] ^ b->limbs[4];
    diff |= a->limbs[5] ^ b->limbs[5];
    diff |= a->limbs[6] ^ b->limbs[6];
    diff |= a->limbs[7] ^ b->limbs[7];
    diff |= a->limbs[8] ^ b->limbs[8];
    diff |= a->limbs[9] ^ b->limbs[9];
    diff |= a->limbs[10] ^ b->limbs[10];
    diff |= a->limbs[11] ^ b->limbs[11];
    diff |= a->limbs[12] ^ b->limbs[12];
    diff |= a->limbs[13] ^ b->limbs[13];
    diff |= a->limbs[14] ^ b->limbs[14];
    diff |= a->limbs[15] ^ b->limbs[15];
    return (chestnut_uint8_t)(((diff | -diff) >> 63) ^ 1);
}

chestnut_uint8_t chestnut_uint128_t_cmp_lt(
    const chestnut_uint128_t *a,
    const chestnut_uint128_t *b
) {
    chestnut_uint64_t discard;
    chestnut_uint8_t borrow = 0;
    borrow = __chestnut_sub_overflow(borrow, a->limbs[0], b->limbs[0], & discard);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[1], b->limbs[1], & discard);
    return borrow;
}

chestnut_uint8_t chestnut_uint256_t_cmp_lt(
    const chestnut_uint256_t *a,
    const chestnut_uint256_t *b
) {
    chestnut_uint64_t discard;
    chestnut_uint8_t borrow = 0;
    borrow = __chestnut_sub_overflow(borrow, a->limbs[0], b->limbs[0], & discard);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[1], b->limbs[1], & discard);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[2], b->limbs[2], & discard);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[3], b->limbs[3], & discard);
    return borrow;
}

chestnut_uint8_t chestnut_uint512_t_cmp_lt(
    const chestnut_uint512_t *a,
    const chestnut_uint512_t *b
) {
    chestnut_uint64_t discard;
    chestnut_uint8_t borrow = 0;
    borrow = __chestnut_sub_overflow(borrow, a->limbs[0], b->limbs[0], & discard);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[1], b->limbs[1], & discard);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[2], b->limbs[2], & discard);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[3], b->limbs[3], & discard);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[4], b->limbs[4], & discard);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[5], b->limbs[5], & discard);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[6], b->limbs[6], & discard);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[7], b->limbs[7], & discard);
    return borrow;
}

chestnut_uint8_t chestnut_uint1024_t_cmp_lt(
    const chestnut_uint1024_t *a,
    const chestnut_uint1024_t *b
) {
    chestnut_uint64_t discard;
    chestnut_uint8_t borrow = 0;
    borrow = __chestnut_sub_overflow(borrow, a->limbs[0], b->limbs[0], & discard);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[1], b->limbs[1], & discard);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[2], b->limbs[2], & discard);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[3], b->limbs[3], & discard);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[4], b->limbs[4], & discard);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[5], b->limbs[5], & discard);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[6], b->limbs[6], & discard);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[7], b->limbs[7], & discard);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[8], b->limbs[8], & discard);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[9], b->limbs[9], & discard);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[10], b->limbs[10], & discard);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[11], b->limbs[11], & discard);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[12], b->limbs[12], & discard);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[13], b->limbs[13], & discard);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[14], b->limbs[14], & discard);
    borrow = __chestnut_sub_overflow(borrow, a->limbs[15], b->limbs[15], & discard);
    return borrow;
}


chestnut_uint8_t chestnut_uint128_t_cmp_lte(
    const chestnut_uint128_t *a,
    const chestnut_uint128_t *b
) {
    return chestnut_uint128_t_cmp_lt(a, b) | chestnut_uint128_t_cmp_eq(a, b);
}

chestnut_uint8_t chestnut_uint256_t_cmp_lte(
    const chestnut_uint256_t *a,
    const chestnut_uint256_t *b
) {
    return chestnut_uint256_t_cmp_lt(a, b) | chestnut_uint256_t_cmp_eq(a, b);
}

chestnut_uint8_t chestnut_uint512_t_cmp_lte(
    const chestnut_uint512_t *a,
    const chestnut_uint512_t *b
) {
    return chestnut_uint512_t_cmp_lt(a, b) | chestnut_uint512_t_cmp_eq(a, b);
}

chestnut_uint8_t chestnut_uint1024_t_cmp_lte(
    const chestnut_uint1024_t *a,
    const chestnut_uint1024_t *b
) {
    return chestnut_uint1024_t_cmp_lt(a, b) | chestnut_uint1024_t_cmp_eq(a, b);
}

chestnut_uint8_t chestnut_uint128_t_cmp_gt(
    const chestnut_uint128_t *a,
    const chestnut_uint128_t *b
) {
    return chestnut_uint128_t_cmp_lt(b, a);
}

chestnut_uint8_t chestnut_uint256_t_cmp_gt(
    const chestnut_uint256_t *a,
    const chestnut_uint256_t *b
) {
    return chestnut_uint256_t_cmp_lt(b, a);
}

chestnut_uint8_t chestnut_uint512_t_cmp_gt(
    const chestnut_uint512_t *a,
    const chestnut_uint512_t *b
) {
    return chestnut_uint512_t_cmp_lt(b, a);
}

chestnut_uint8_t chestnut_uint1024_t_cmp_gt(
    const chestnut_uint1024_t *a,
    const chestnut_uint1024_t *b
) {
    return chestnut_uint1024_t_cmp_lt(b, a);
}

chestnut_uint8_t chestnut_uint128_t_cmp_gte(
    const chestnut_uint128_t *a,
    const chestnut_uint128_t *b
) {
    return chestnut_uint128_t_cmp_lte(b, a);
}

chestnut_uint8_t chestnut_uint256_t_cmp_gte(
    const chestnut_uint256_t *a,
    const chestnut_uint256_t *b
) {
    return chestnut_uint256_t_cmp_lte(b, a);
}

chestnut_uint8_t chestnut_uint512_t_cmp_gte(
    const chestnut_uint512_t *a,
    const chestnut_uint512_t *b
) {
    return chestnut_uint512_t_cmp_lte(b, a);
}

chestnut_uint8_t chestnut_uint1024_t_cmp_gte(
    const chestnut_uint1024_t *a,
    const chestnut_uint1024_t *b
) {
    return chestnut_uint1024_t_cmp_lte(b, a);
}

void chestnut_uint128_t_and(
    chestnut_uint128_t *out,
    const chestnut_uint128_t *a,
    const chestnut_uint128_t *b
){
    out->limbs[0] = a->limbs[0] & b->limbs[0];
    out->limbs[1] = a->limbs[1] & b->limbs[1];
}

void chestnut_uint256_t_and(
    chestnut_uint256_t *out,
    const chestnut_uint256_t *a,
    const chestnut_uint256_t *b
) {
    out->limbs[0] = a->limbs[0] & b->limbs[0];
    out->limbs[1] = a->limbs[1] & b->limbs[1];
    out->limbs[2] = a->limbs[2] & b->limbs[2];
    out->limbs[3] = a->limbs[3] & b->limbs[3];
}

void chestnut_uint512_t_and(
    chestnut_uint512_t *out,
    chestnut_uint512_t *a,
    chestnut_uint512_t *b
) {
    out->limbs[0] = a->limbs[0] & b->limbs[0];
    out->limbs[1] = a->limbs[1] & b->limbs[1];
    out->limbs[2] = a->limbs[2] & b->limbs[2];
    out->limbs[3] = a->limbs[3] & b->limbs[3];
    out->limbs[4] = a->limbs[4] & b->limbs[4];
    out->limbs[5] = a->limbs[5] & b->limbs[5];
    out->limbs[6] = a->limbs[6] & b->limbs[6];
    out->limbs[7] = a->limbs[7] & b->limbs[7];
}

void chestnut_uint1024_t_and(
    chestnut_uint1024_t *out,
    chestnut_uint1024_t *a,
    chestnut_uint1024_t *b
) {
    out->limbs[0] = a->limbs[0] & b->limbs[0];
    out->limbs[1] = a->limbs[1] & b->limbs[1];
    out->limbs[2] = a->limbs[2] & b->limbs[2];
    out->limbs[3] = a->limbs[3] & b->limbs[3];
    out->limbs[4] = a->limbs[4] & b->limbs[4];
    out->limbs[5] = a->limbs[5] & b->limbs[5];
    out->limbs[6] = a->limbs[6] & b->limbs[6];
    out->limbs[7] = a->limbs[7] & b->limbs[7];
    out->limbs[8] = a->limbs[8] & b->limbs[8];
    out->limbs[9] = a->limbs[9] & b->limbs[9];
    out->limbs[10] = a->limbs[10] & b->limbs[10];
    out->limbs[11] = a->limbs[11] & b->limbs[11];
    out->limbs[12] = a->limbs[12] & b->limbs[12];
    out->limbs[13] = a->limbs[13] & b->limbs[13];
    out->limbs[14] = a->limbs[14] & b->limbs[14];
    out->limbs[15] = a->limbs[15] & b->limbs[15];
}

void chestnut_uint128_t_or(
    chestnut_uint128_t *out,
    chestnut_uint128_t *a,
    chestnut_uint128_t *b
) {
    out->limbs[0] = a->limbs[0] | b->limbs[0];
    out->limbs[1] = a->limbs[1] | b->limbs[1];
}

void chestnut_uint256_t_or(
    chestnut_uint256_t *out,
    chestnut_uint256_t *a,
    chestnut_uint256_t *b
) {
    out->limbs[0] = a->limbs[0] | b->limbs[0];
    out->limbs[1] = a->limbs[1] | b->limbs[1];
    out->limbs[2] = a->limbs[2] | b->limbs[2];
    out->limbs[3] = a->limbs[3] | b->limbs[3];
}

void chestnut_uint512_t_or(
    chestnut_uint512_t *out,
    chestnut_uint512_t *a,
    chestnut_uint512_t *b
) {
    out->limbs[0] = a->limbs[0] | b->limbs[0];
    out->limbs[1] = a->limbs[1] | b->limbs[1];
    out->limbs[2] = a->limbs[2] | b->limbs[2];
    out->limbs[3] = a->limbs[3] | b->limbs[3];
    out->limbs[4] = a->limbs[4] | b->limbs[4];
    out->limbs[5] = a->limbs[5] | b->limbs[5];
    out->limbs[6] = a->limbs[6] | b->limbs[6];
    out->limbs[7] = a->limbs[7] | b->limbs[7];
}

void chestnut_uint1024_or_t(
    chestnut_uint1024_t *out,
    const chestnut_uint1024_t *a,
    const chestnut_uint1024_t *b
) {
    out->limbs[0] = a->limbs[0] | b->limbs[0];
    out->limbs[1] = a->limbs[1] | b->limbs[1];
    out->limbs[2] = a->limbs[2] | b->limbs[2];
    out->limbs[3] = a->limbs[3] | b->limbs[3];
    out->limbs[4] = a->limbs[4] | b->limbs[4];
    out->limbs[5] = a->limbs[5] | b->limbs[5];
    out->limbs[6] = a->limbs[6] | b->limbs[6];
    out->limbs[7] = a->limbs[7] | b->limbs[7];
    out->limbs[8] = a->limbs[8] | b->limbs[8];
    out->limbs[9] = a->limbs[9] | b->limbs[9];
    out->limbs[10] = a->limbs[10] | b->limbs[10];
    out->limbs[11] = a->limbs[11] | b->limbs[11];
    out->limbs[12] = a->limbs[12] | b->limbs[12];
    out->limbs[13] = a->limbs[13] | b->limbs[13];
    out->limbs[14] = a->limbs[14] | b->limbs[14];
    out->limbs[15] = a->limbs[15] | b->limbs[15]; 
}

void chestnut_uint128_xor_t(
    chestnut_uint128_t *out,
    const chestnut_uint128_t *a,
    const chestnut_uint128_t *b
) {
    out->limbs[0] = a->limbs[0] ^ b->limbs[0];
    out->limbs[1] = a->limbs[1] ^ b->limbs[1];
}

void chestnut_uint256_t_xor(
    chestnut_uint256_t *out,
    const chestnut_uint256_t *a,
    const chestnut_uint256_t *b
) {
    out->limbs[0] = a->limbs[0] ^ b->limbs[0];
    out->limbs[1] = a->limbs[1] ^ b->limbs[1];
    out->limbs[2] = a->limbs[2] ^ b->limbs[2];
    out->limbs[3] = a->limbs[3] ^ b->limbs[3];
}

void chestnut_uint512_t_xor(
    chestnut_uint512_t *out,
    const chestnut_uint512_t *a,
    const chestnut_uint512_t *b
) {
    out->limbs[0] = a->limbs[0] ^ b->limbs[0];
    out->limbs[1] = a->limbs[1] ^ b->limbs[1];
    out->limbs[2] = a->limbs[2] ^ b->limbs[2];
    out->limbs[3] = a->limbs[3] ^ b->limbs[3];
    out->limbs[4] = a->limbs[4] ^ b->limbs[4];
    out->limbs[5] = a->limbs[5] ^ b->limbs[5];
    out->limbs[6] = a->limbs[6] ^ b->limbs[6];
    out->limbs[7] = a->limbs[7] ^ b->limbs[7];
}

void chestnut_uint1024_t_xor(
    chestnut_uint1024_t *out,
    const chestnut_uint1024_t *a,
    const chestnut_uint1024_t *b
) {
    out->limbs[0] = a->limbs[0] ^ b->limbs[0];
    out->limbs[1] = a->limbs[1] ^ b->limbs[1];
    out->limbs[2] = a->limbs[2] ^ b->limbs[2];
    out->limbs[3] = a->limbs[3] ^ b->limbs[3];
    out->limbs[4] = a->limbs[4] ^ b->limbs[4];
    out->limbs[5] = a->limbs[5] ^ b->limbs[5];
    out->limbs[6] = a->limbs[6] ^ b->limbs[6];
    out->limbs[7] = a->limbs[7] ^ b->limbs[7];
    out->limbs[8] = a->limbs[8] ^ b->limbs[8];
    out->limbs[9] = a->limbs[9] ^ b->limbs[9];
    out->limbs[10] = a->limbs[10] ^ b->limbs[10];
    out->limbs[11] = a->limbs[11] ^ b->limbs[11];
    out->limbs[12] = a->limbs[12] ^ b->limbs[12];
    out->limbs[13] = a->limbs[13] ^ b->limbs[13];
    out->limbs[14] = a->limbs[14] ^ b->limbs[14];
    out->limbs[15] = a->limbs[15] ^ b->limbs[15];
}

void chestnut_uint128_t_not(
    chestnut_uint128_t *out,
    const chestnut_uint128_t *in
) {
    out->limbs[0] = ~in->limbs[0];
    out->limbs[1] = ~in->limbs[1];
}

void chestnut_uint256_t_not(
    chestnut_uint256_t *out,
    const chestnut_uint256_t *in
) {
    out->limbs[0] = ~in->limbs[0];
    out->limbs[1] = ~in->limbs[1];
    out->limbs[2] = ~in->limbs[2];
    out->limbs[3] = ~in->limbs[3];
}

void chestnut_uint512_t_not(
    chestnut_uint512_t *out,
    const chestnut_uint512_t *in
) {
    out->limbs[0] = ~in->limbs[0]; 
    out->limbs[1] = ~in->limbs[1]; 
    out->limbs[2] = ~in->limbs[2]; 
    out->limbs[3] = ~in->limbs[3]; 
    out->limbs[4] = ~in->limbs[4]; 
    out->limbs[5] = ~in->limbs[5]; 
    out->limbs[6] = ~in->limbs[6]; 
    out->limbs[7] = ~in->limbs[7]; 
}

void chestnut_uint1024_t_not(
    chestnut_uint1024_t *out,
    const chestnut_uint1024_t *in
) {
    out->limbs[0] = ~in->limbs[0];
    out->limbs[1] = ~in->limbs[1];
    out->limbs[2] = ~in->limbs[2];
    out->limbs[3] = ~in->limbs[3];
    out->limbs[4] = ~in->limbs[4];
    out->limbs[5] = ~in->limbs[5];
    out->limbs[6] = ~in->limbs[6];
    out->limbs[7] = ~in->limbs[7];
    out->limbs[8] = ~in->limbs[8];
    out->limbs[9] = ~in->limbs[9];
    out->limbs[10] = ~in->limbs[10];
    out->limbs[11] = ~in->limbs[11];
    out->limbs[12] = ~in->limbs[12];
    out->limbs[13] = ~in->limbs[13];
    out->limbs[14] = ~in->limbs[14];
    out->limbs[15] = ~in->limbs[15];
}

chestnut_uint8_t chestnut_uint128_t_negate(
    chestnut_uint128_t *out,
    const chestnut_uint128_t *in
) {
    chestnut_uint128_t_not(out, in);

    chestnut_uint64_t carry = 1;

    carry = __chestnut_add_overflow(0, out->limbs[0], carry, &out->limbs[0]);
    carry = __chestnut_add_overflow(0, out->limbs[1], carry, &out->limbs[1]);

    return (chestnut_uint8_t)carry;
}

chestnut_uint8_t chestnut_uint256_t_negate(
    chestnut_uint256_t *out,
    const chestnut_uint256_t *in
) {
    chestnut_uint256_t_not(out, in);
    
    chestnut_uint8_t carry = 1;

    carry = __chestnut_add_overflow(0, out->limbs[0], carry, &out->limbs[0]);
    carry = __chestnut_add_overflow(0, out->limbs[1], carry, &out->limbs[1]);
    carry = __chestnut_add_overflow(0, out->limbs[2], carry, &out->limbs[2]);
    carry = __chestnut_add_overflow(0, out->limbs[3], carry, &out->limbs[3]);

    return (chestnut_uint8_t)carry;
}

chestnut_uint8_t chestnut_uint512_t_negate(
    chestnut_uint512_t *out,
    const chestnut_uint512_t *in
) {
    chestnut_uint512_t_not(out, in);

    chestnut_uint64_t carry = 1;

    carry = __chestnut_add_overflow(0, out->limbs[0], carry, &out->limbs[0]);
    carry = __chestnut_add_overflow(0, out->limbs[1], carry, &out->limbs[1]);
    carry = __chestnut_add_overflow(0, out->limbs[2], carry, &out->limbs[2]);
    carry = __chestnut_add_overflow(0, out->limbs[3], carry, &out->limbs[3]);
    carry = __chestnut_add_overflow(0, out->limbs[4], carry, &out->limbs[4]);
    carry = __chestnut_add_overflow(0, out->limbs[5], carry, &out->limbs[5]);
    carry = __chestnut_add_overflow(0, out->limbs[6], carry, &out->limbs[6]);
    carry = __chestnut_add_overflow(0, out->limbs[7], carry, &out->limbs[7]);

    return (chestnut_uint8_t)carry;
}

chestnut_uint8_t chestnut_uint1024_t_negate(
    chestnut_uint1024_t *out,
    const chestnut_uint1024_t *in
) {
    chestnut_uint1024_t_not(out, in);

    chestnut_uint64_t carry = 1;

    carry = __chestnut_add_overflow(0, out->limbs[0], carry, &out->limbs[0]);
    carry = __chestnut_add_overflow(0, out->limbs[1], carry, &out->limbs[1]);
    carry = __chestnut_add_overflow(0, out->limbs[2], carry, &out->limbs[2]);
    carry = __chestnut_add_overflow(0, out->limbs[3], carry, &out->limbs[3]);
    carry = __chestnut_add_overflow(0, out->limbs[4], carry, &out->limbs[4]);
    carry = __chestnut_add_overflow(0, out->limbs[5], carry, &out->limbs[5]);
    carry = __chestnut_add_overflow(0, out->limbs[6], carry, &out->limbs[6]);
    carry = __chestnut_add_overflow(0, out->limbs[7], carry, &out->limbs[7]);
    carry = __chestnut_add_overflow(0, out->limbs[8], carry, &out->limbs[8]);
    carry = __chestnut_add_overflow(0, out->limbs[9], carry, &out->limbs[9]);
    carry = __chestnut_add_overflow(0, out->limbs[10], carry, &out->limbs[10]);
    carry = __chestnut_add_overflow(0, out->limbs[11], carry, &out->limbs[11]);
    carry = __chestnut_add_overflow(0, out->limbs[12], carry, &out->limbs[12]);
    carry = __chestnut_add_overflow(0, out->limbs[13], carry, &out->limbs[13]);
    carry = __chestnut_add_overflow(0, out->limbs[14], carry, &out->limbs[14]);
    carry = __chestnut_add_overflow(0, out->limbs[15], carry, &out->limbs[15]);

    return (chestnut_uint8_t)carry;
}

static inline __attribute__((always_inline)) void chestnut_uint128_t_clear(
    chestnut_uint128_t *in
) {
    in->limbs[0] = 0;
    in->limbs[1] = 0;
}

static inline __attribute__((always_inline)) void chestnut_uint256_t_clear(
    chestnut_uint256_t *in
) {
    in->limbs[0] = 0;
    in->limbs[1] = 0;
    in->limbs[2] = 0;
    in->limbs[3] = 0;
}

static inline __attribute__((always_inline)) void chestnut_uint512_t_clear(
    chestnut_uint512_t *in
) {
    in->limbs[0] = 0;
    in->limbs[1] = 0;
    in->limbs[2] = 0;
    in->limbs[3] = 0;
    in->limbs[4] = 0;
    in->limbs[5] = 0;
    in->limbs[6] = 0;
    in->limbs[7] = 0;
}

static inline __attribute__((always_inline)) void chestnut_uint1024_t_clear(
    chestnut_uint1024_t *in
) {
    in->limbs[0] = 0;
    in->limbs[1] = 0;
    in->limbs[2] = 0;
    in->limbs[3] = 0;
    in->limbs[4] = 0;
    in->limbs[5] = 0;
    in->limbs[6] = 0;
    in->limbs[7] = 0;
    in->limbs[8] = 0;
    in->limbs[9] = 0;
    in->limbs[10] = 0;
    in->limbs[11] = 0;
    in->limbs[12] = 0;
    in->limbs[13] = 0;
    in->limbs[14] = 0;
    in->limbs[15] = 0;
}

static inline __attribute__((always_inline)) chestnut_uint64_t __chestnut_mul(
    chestnut_uint64_t *high,
    const chestnut_uint64_t a,
    const chestnut_uint64_t b
) {
    #if defined(__GNUC__) || defined(__clang__)
        unsigned __int128 res = (unsigned __int128)a * b;
        *high = (chestnut_uint64_t)(res >> 64);
        return (chestnut_uint64_t)res;
    #elif defined(_MSC_VER)
        return (chestnut_uint64_t)_umul128(a, b, high);
    #else
        const chestnut_uint64_t MAX = 0xFFFFFFFF;
        const chestnut_uint64_t SHIFT = 32;

        chestnut_uint64_t a_low = a & MAX;
        chestnut_uint64_t a_high = a >> SHIFT;
        chestnut_uint64_t b_low = b & MAX;
        chestnut_uint64_t b_high = b >> SHIFT;
        
        chestnut_uint64_t p0 = a_low * b_low;
        chestnut_uint64_t p1 = a_low * b_high;
        chestnut_uint64_t p2 = a_high * b_low;
        chestnut_uint64_t p3 = a_high * b_high;

        chestnut_uint64_t cy = (p0 >> SHIFT) + (p1 & MAX) + (p2 & MAX);

        chestnut_uint64_t low_out = (p0 & MAX) | (cy << SHIFT);

        // Combine the high values.
        *high = p3 + (p1 >> SHIFT) + (p2 >> SHIFT) + (cy >> SHIFT);

        // Return the low values.
        return low_out;
    #endif
}

static inline __attribute__((always_inline)) chestnut_uint64_t __chestnut_mul_acc(
    chestnut_uint64_t *acc_high,
    chestnut_uint64_t acc_low,
    const chestnut_uint64_t a,
    const chestnut_uint64_t b
) {
    chestnut_uint64_t mul_high;
    chestnut_uint64_t mul_low = __chestnut_mul(&mul_high, a, b);

    chestnut_uint64_t carry = __chestnut_add_overflow(0, acc_low, mul_low, &acc_low);
    *acc_high += mul_high + carry;

    return acc_low;
}

// Will be used in multiplications with *
chestnut_uint64_t chestnut_uint128_t_mul(
    chestnut_uint128_t *out,
    chestnut_uint128_t *a,
    chestnut_uint128_t *b
) {
    chestnut_uint64_t carry_out = 0, overflow = 0;
    // Limb 0
    out->limbs[0] = __chestnut_mul(&carry_out, a->limbs[0], b->limbs[0]);

    // Limb 1
    out->limbs[1] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[1]);
    carry_out = overflow;
    out->limbs[1] = __chestnut_mul_acc(&overflow, out->limbs[1], a->limbs[1], b->limbs[0]);
    carry_out += overflow;

    return carry_out;
}

// Will be used in multiplications with ×
chestnut_uint128_t chestnut_uint128_t_mul_full(
    chestnut_uint128_t *out_low,
    const chestnut_uint128_t *a,
    const chestnut_uint128_t *b
) {
    chestnut_uint128_t out_high;
    chestnut_uint64_t carry_out = 0, overflow = 0;

    // Lower limb 0
    out_low->limbs[0] = __chestnut_mul(&carry_out, a->limbs[0], b->limbs[0]);

    // Lower limb 1
    out_low->limbs[1] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[1]);
    carry_out = overflow;
    out_low->limbs[1] = __chestnut_mul_acc(&overflow, out_low->limbs[1], a->limbs[1], b->limbs[0]);
    carry_out += overflow;

    // High limb 0 & limb 1
    out_high.limbs[0] = __chestnut_mul_acc(&out_high.limbs[1], carry_out, a->limbs[1], b->limbs[1]);

    return out_high;
}

chestnut_uint64_t chestnut_uint256_t_mul(
    chestnut_uint256_t *out,
    chestnut_uint256_t *a,
    chestnut_uint256_t *b
) {
    chestnut_uint64_t carry_out = 0, overflow = 0;

    // Limb 0
    out->limbs[0] = __chestnut_mul(&carry_out, a->limbs[0], b->limbs[0]);

    // Limb 1
    out->limbs[1] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[1]);
    carry_out = overflow;
    out->limbs[1] = __chestnut_mul_acc(&overflow, out->limbs[1], a->limbs[1], b->limbs[0]);
    carry_out += overflow;

    // Limb 2
    out->limbs[2] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[2]);
    carry_out = overflow;
    out->limbs[2] = __chestnut_mul_acc(&overflow, out->limbs[2], a->limbs[1], b->limbs[1]);
    carry_out += overflow;
    out->limbs[2] = __chestnut_mul_acc(&overflow, out->limbs[2], a->limbs[2], b->limbs[0]);
    carry_out += overflow;

    // Limb 3
    out->limbs[3] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[3]);
    carry_out = overflow;
    out->limbs[3] = __chestnut_mul_acc(&overflow, out->limbs[3], a->limbs[1], b->limbs[2]);
    carry_out += overflow;
    out->limbs[3] = __chestnut_mul_acc(&overflow, out->limbs[3], a->limbs[2], b->limbs[1]);
    carry_out += overflow;
    out->limbs[3] = __chestnut_mul_acc(&overflow, out->limbs[3], a->limbs[3], b->limbs[0]);
    carry_out += overflow;

    return carry_out;
}

chestnut_uint256_t chestnut_uint256_t_mul_full(
    chestnut_uint256_t *out_low,
    chestnut_uint256_t *a,
    chestnut_uint256_t *b
) {
    chestnut_uint256_t out_high;
    chestnut_uint64_t carry_in = 0, carry_out = 0, overflow = 0;

    // Low limb 0
    out_low->limbs[0] = __chestnut_mul(&overflow, a->limbs[0], b->limbs[0]);
    carry_out += overflow;

    // Low limb 1
    carry_in = carry_out;
    carry_out = 0;
    out_low->limbs[1] = __chestnut_mul_acc(&overflow, carry_in, a->limbs[0], b->limbs[1]);
    carry_out += overflow;
    out_low->limbs[1] = __chestnut_mul_acc(&overflow, out_low->limbs[1], a->limbs[1], b->limbs[0]);
    carry_out += overflow;

    // Low limb 2
    carry_in = carry_out;
    carry_out = 0;
    out_low->limbs[2] = __chestnut_mul_acc(&overflow, carry_in, a->limbs[0], b->limbs[2]);
    carry_out += overflow;
    out_low->limbs[2] = __chestnut_mul_acc(&overflow, out_low->limbs[2], a->limbs[1], b->limbs[1]);
    carry_out += overflow;
    out_low->limbs[2] = __chestnut_mul_acc(&overflow, out_low->limbs[2], a->limbs[2], b->limbs[0]);
    carry_out += overflow;

    // Low limb 3
    carry_in = carry_out;
    carry_out = 0;
    out_low->limbs[3] = __chestnut_mul_acc(&overflow, carry_in, a->limbs[0], b->limbs[3]);
    carry_out += overflow;
    out_low->limbs[3] = __chestnut_mul_acc(&overflow, out_low->limbs[3], a->limbs[1], b->limbs[2]);
    carry_out += overflow;
    out_low->limbs[3] = __chestnut_mul_acc(&overflow, out_low->limbs[3], a->limbs[2], b->limbs[1]);
    carry_out += overflow;
    out_low->limbs[3] = __chestnut_mul_acc(&overflow, out_low->limbs[3], a->limbs[3], b->limbs[0]);
    carry_out += overflow;

    // High limb 0
    carry_in = carry_out;
    carry_out = 0;
    out_high.limbs[0] = __chestnut_mul_acc(&overflow, carry_in, a->limbs[1], b->limbs[3]);
    carry_out += overflow;
    out_high.limbs[0] = __chestnut_mul_acc(&overflow, out_high.limbs[0], a->limbs[2], b->limbs[2]);
    carry_out += overflow;
    out_high.limbs[0] = __chestnut_mul_acc(&overflow, out_high.limbs[0], a->limbs[3], b->limbs[1]);
    carry_out += overflow;

    // High limb 1
    carry_in = carry_out;
    carry_out = 0;
    out_high.limbs[1] = __chestnut_mul_acc(&overflow, carry_in, a->limbs[2], b->limbs[3]);
    carry_out += overflow;
    out_high.limbs[1] = __chestnut_mul_acc(&overflow, out_high.limbs[1], a->limbs[3], b->limbs[2]);
    carry_out += overflow;

    // High limb 2 & 3.
    out_high.limbs[2] = __chestnut_mul_acc(&out_high.limbs[3], carry_out, a->limbs[3], b->limbs[3]);

    return out_high;
}

chestnut_uint64_t chestnut_uint512_t_mul(
    chestnut_uint512_t *out,
    chestnut_uint512_t *a,
    chestnut_uint512_t *b
) {
    chestnut_uint64_t carry_out = 0, overflow = 0;

    // Limb 0
    out->limbs[0] = __chestnut_mul(&carry_out, a->limbs[0], b->limbs[0]);

    // Limb 1
    out->limbs[1] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[1]);
    carry_out = overflow;
    out->limbs[1] = __chestnut_mul_acc(&overflow, out->limbs[1], a->limbs[1], b->limbs[0]);
    carry_out += overflow;

    // Limb 2
    out->limbs[2] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[2]);
    carry_out = overflow;
    out->limbs[2] = __chestnut_mul_acc(&overflow, out->limbs[2], a->limbs[1], b->limbs[1]);
    carry_out += overflow;
    out->limbs[2] = __chestnut_mul_acc(&overflow, out->limbs[2], a->limbs[2], b->limbs[0]);
    carry_out += overflow;

    // Limb 3
    out->limbs[3] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[3]);
    carry_out = overflow;
    out->limbs[3] = __chestnut_mul_acc(&overflow, out->limbs[3], a->limbs[1], b->limbs[2]);
    carry_out += overflow;
    out->limbs[3] = __chestnut_mul_acc(&overflow, out->limbs[3], a->limbs[2], b->limbs[1]);
    carry_out += overflow;
    out->limbs[3] = __chestnut_mul_acc(&overflow, out->limbs[3], a->limbs[3], b->limbs[0]);
    carry_out += overflow;

    // Limb 4
    out->limbs[4] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[4]);
    carry_out = overflow;
    out->limbs[4] = __chestnut_mul_acc(&overflow, out->limbs[4], a->limbs[1], b->limbs[3]);
    carry_out += overflow;
    out->limbs[4] = __chestnut_mul_acc(&overflow, out->limbs[4], a->limbs[2], b->limbs[2]);
    carry_out += overflow;
    out->limbs[4] = __chestnut_mul_acc(&overflow, out->limbs[4], a->limbs[3], b->limbs[1]);
    carry_out += overflow;
    out->limbs[4] = __chestnut_mul_acc(&overflow, out->limbs[4], a->limbs[4], b->limbs[0]);
    carry_out += overflow;

    // Limb 5
    out->limbs[5] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[5]);
    carry_out = overflow;
    out->limbs[5] = __chestnut_mul_acc(&overflow, out->limbs[5], a->limbs[1], b->limbs[4]);
    carry_out += overflow;
    out->limbs[5] = __chestnut_mul_acc(&overflow, out->limbs[5], a->limbs[2], b->limbs[3]);
    carry_out += overflow;
    out->limbs[5] = __chestnut_mul_acc(&overflow, out->limbs[5], a->limbs[3], b->limbs[2]);
    carry_out += overflow;
    out->limbs[5] = __chestnut_mul_acc(&overflow, out->limbs[5], a->limbs[4], b->limbs[1]);
    carry_out += overflow;
    out->limbs[5] = __chestnut_mul_acc(&overflow, out->limbs[5], a->limbs[5], b->limbs[0]);
    carry_out += overflow;

    // Limb 6
    out->limbs[6] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[6]);
    carry_out = overflow;
    out->limbs[6] = __chestnut_mul_acc(&overflow, out->limbs[6], a->limbs[1], b->limbs[5]);
    carry_out += overflow;
    out->limbs[6] = __chestnut_mul_acc(&overflow, out->limbs[6], a->limbs[2], b->limbs[4]);
    carry_out += overflow;
    out->limbs[6] = __chestnut_mul_acc(&overflow, out->limbs[6], a->limbs[3], b->limbs[3]);
    carry_out += overflow;
    out->limbs[6] = __chestnut_mul_acc(&overflow, out->limbs[6], a->limbs[4], b->limbs[2]);
    carry_out += overflow;
    out->limbs[6] = __chestnut_mul_acc(&overflow, out->limbs[6], a->limbs[5], b->limbs[1]);
    carry_out += overflow;
    out->limbs[6] = __chestnut_mul_acc(&overflow, out->limbs[6], a->limbs[6], b->limbs[0]);
    carry_out += overflow;

    // Limb 7
    out->limbs[7] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[7]);
    carry_out = overflow;
    out->limbs[7] = __chestnut_mul_acc(&overflow, out->limbs[7], a->limbs[1], b->limbs[6]);
    carry_out += overflow;
    out->limbs[7] = __chestnut_mul_acc(&overflow, out->limbs[7], a->limbs[2], b->limbs[5]);
    carry_out += overflow;
    out->limbs[7] = __chestnut_mul_acc(&overflow, out->limbs[7], a->limbs[3], b->limbs[4]);
    carry_out += overflow;
    out->limbs[7] = __chestnut_mul_acc(&overflow, out->limbs[7], a->limbs[4], b->limbs[3]);
    carry_out += overflow;
    out->limbs[7] = __chestnut_mul_acc(&overflow, out->limbs[7], a->limbs[5], b->limbs[2]);
    carry_out += overflow;
    out->limbs[7] = __chestnut_mul_acc(&overflow, out->limbs[7], a->limbs[6], b->limbs[1]);
    carry_out += overflow;
    out->limbs[7] = __chestnut_mul_acc(&overflow, out->limbs[7], a->limbs[7], b->limbs[0]);
    carry_out += overflow;

    return carry_out;
}

chestnut_uint512_t chestnut_uint512_t_mul_full(
    chestnut_uint512_t *out_low,
    chestnut_uint512_t *a,
    chestnut_uint512_t *b
) {
    chestnut_uint512_t out_high;
    chestnut_uint64_t carry_out = 0, overflow = 0;

    // Lower limb 0
    out_low->limbs[0] = __chestnut_mul(&carry_out, a->limbs[0], b->limbs[0]);

    // Lower limb 1
    out_low->limbs[1] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[1]);
    carry_out = overflow;
    out_low->limbs[1] = __chestnut_mul_acc(&overflow, out_low->limbs[1], a->limbs[1], b->limbs[0]);
    carry_out += overflow;

    // Lower limb 2
    out_low->limbs[2] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[2]);
    carry_out = overflow;
    out_low->limbs[2] = __chestnut_mul_acc(&overflow, out_low->limbs[2], a->limbs[1], b->limbs[1]);
    carry_out += overflow;
    out_low->limbs[2] = __chestnut_mul_acc(&overflow, out_low->limbs[2], a->limbs[2], b->limbs[0]);
    carry_out += overflow;

    // Lower limb 3
    out_low->limbs[3] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[3]);
    carry_out = overflow;
    out_low->limbs[3] = __chestnut_mul_acc(&overflow, out_low->limbs[3], a->limbs[1], b->limbs[2]);
    carry_out += overflow;
    out_low->limbs[3] = __chestnut_mul_acc(&overflow, out_low->limbs[3], a->limbs[2], b->limbs[1]);
    carry_out += overflow;
    out_low->limbs[3] = __chestnut_mul_acc(&overflow, out_low->limbs[3], a->limbs[3], b->limbs[0]);
    carry_out += overflow;

    // Lower limb 4
    out_low->limbs[4] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[4]);
    carry_out = overflow;
    out_low->limbs[4] = __chestnut_mul_acc(&overflow, out_low->limbs[4], a->limbs[1], b->limbs[3]);
    carry_out += overflow;
    out_low->limbs[4] = __chestnut_mul_acc(&overflow, out_low->limbs[4], a->limbs[2], b->limbs[2]);
    carry_out += overflow;
    out_low->limbs[4] = __chestnut_mul_acc(&overflow, out_low->limbs[4], a->limbs[3], b->limbs[1]);
    carry_out += overflow;
    out_low->limbs[4] = __chestnut_mul_acc(&overflow, out_low->limbs[4], a->limbs[4], b->limbs[0]);
    carry_out += overflow;

    // Lower limb 5
    out_low->limbs[5] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[5]);
    carry_out = overflow;
    out_low->limbs[5] = __chestnut_mul_acc(&overflow, out_low->limbs[5], a->limbs[1], b->limbs[4]);
    carry_out += overflow;
    out_low->limbs[5] = __chestnut_mul_acc(&overflow, out_low->limbs[5], a->limbs[2], b->limbs[3]);
    carry_out += overflow;
    out_low->limbs[5] = __chestnut_mul_acc(&overflow, out_low->limbs[5], a->limbs[3], b->limbs[2]);
    carry_out += overflow;
    out_low->limbs[5] = __chestnut_mul_acc(&overflow, out_low->limbs[5], a->limbs[4], b->limbs[1]);
    carry_out += overflow;
    out_low->limbs[5] = __chestnut_mul_acc(&overflow, out_low->limbs[5], a->limbs[5], b->limbs[0]);
    carry_out += overflow;

    // Lower limb 6
    out_low->limbs[6] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[6]);
    carry_out = overflow;
    out_low->limbs[6] = __chestnut_mul_acc(&overflow, out_low->limbs[6], a->limbs[1], b->limbs[5]);
    carry_out += overflow;
    out_low->limbs[6] = __chestnut_mul_acc(&overflow, out_low->limbs[6], a->limbs[2], b->limbs[4]);
    carry_out += overflow;
    out_low->limbs[6] = __chestnut_mul_acc(&overflow, out_low->limbs[6], a->limbs[3], b->limbs[3]);
    carry_out += overflow;
    out_low->limbs[6] = __chestnut_mul_acc(&overflow, out_low->limbs[6], a->limbs[4], b->limbs[2]);
    carry_out += overflow;
    out_low->limbs[6] = __chestnut_mul_acc(&overflow, out_low->limbs[6], a->limbs[5], b->limbs[1]);
    carry_out += overflow;
    out_low->limbs[6] = __chestnut_mul_acc(&overflow, out_low->limbs[6], a->limbs[6], b->limbs[0]);
    carry_out += overflow;

    // Lower limb 7
    out_low->limbs[7] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[7]);
    carry_out = overflow;
    out_low->limbs[7] = __chestnut_mul_acc(&overflow, out_low->limbs[7], a->limbs[1], b->limbs[6]);
    carry_out += overflow;
    out_low->limbs[7] = __chestnut_mul_acc(&overflow, out_low->limbs[7], a->limbs[2], b->limbs[5]);
    carry_out += overflow;
    out_low->limbs[7] = __chestnut_mul_acc(&overflow, out_low->limbs[7], a->limbs[3], b->limbs[4]);
    carry_out += overflow;
    out_low->limbs[7] = __chestnut_mul_acc(&overflow, out_low->limbs[7], a->limbs[4], b->limbs[3]);
    carry_out += overflow;
    out_low->limbs[7] = __chestnut_mul_acc(&overflow, out_low->limbs[7], a->limbs[5], b->limbs[2]);
    carry_out += overflow;
    out_low->limbs[7] = __chestnut_mul_acc(&overflow, out_low->limbs[7], a->limbs[6], b->limbs[1]);
    carry_out += overflow;
    out_low->limbs[7] = __chestnut_mul_acc(&overflow, out_low->limbs[7], a->limbs[7], b->limbs[0]);
    carry_out += overflow;

    // Upper limb 0
    out_high.limbs[0] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[1], b->limbs[7]);
    carry_out = overflow;
    out_high.limbs[0] = __chestnut_mul_acc(&overflow, out_high.limbs[0], a->limbs[2], b->limbs[6]);
    carry_out += overflow;
    out_high.limbs[0] = __chestnut_mul_acc(&overflow, out_high.limbs[0], a->limbs[3], b->limbs[5]);
    carry_out += overflow;
    out_high.limbs[0] = __chestnut_mul_acc(&overflow, out_high.limbs[0], a->limbs[4], b->limbs[4]);
    carry_out += overflow;
    out_high.limbs[0] = __chestnut_mul_acc(&overflow, out_high.limbs[0], a->limbs[5], b->limbs[3]);
    carry_out += overflow;
    out_high.limbs[0] = __chestnut_mul_acc(&overflow, out_high.limbs[0], a->limbs[6], b->limbs[2]);
    carry_out += overflow;
    out_high.limbs[0] = __chestnut_mul_acc(&overflow, out_high.limbs[0], a->limbs[7], b->limbs[1]);
    carry_out += overflow;

    // Upper limb 1
    out_high.limbs[1] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[2], b->limbs[7]);
    carry_out = overflow;
    out_high.limbs[1] = __chestnut_mul_acc(&overflow, out_high.limbs[1], a->limbs[3], b->limbs[6]);
    carry_out += overflow;
    out_high.limbs[1] = __chestnut_mul_acc(&overflow, out_high.limbs[1], a->limbs[4], b->limbs[5]);
    carry_out += overflow;
    out_high.limbs[1] = __chestnut_mul_acc(&overflow, out_high.limbs[1], a->limbs[5], b->limbs[4]);
    carry_out += overflow;
    out_high.limbs[1] = __chestnut_mul_acc(&overflow, out_high.limbs[1], a->limbs[6], b->limbs[3]);
    carry_out += overflow;
    out_high.limbs[1] = __chestnut_mul_acc(&overflow, out_high.limbs[1], a->limbs[7], b->limbs[2]);
    carry_out += overflow;

    // Upper limb 2
    out_high.limbs[2] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[3], b->limbs[7]);
    carry_out = overflow;
    out_high.limbs[2] = __chestnut_mul_acc(&overflow, out_high.limbs[2], a->limbs[4], b->limbs[6]);
    carry_out += overflow;
    out_high.limbs[2] = __chestnut_mul_acc(&overflow, out_high.limbs[2], a->limbs[5], b->limbs[5]);
    carry_out += overflow;
    out_high.limbs[2] = __chestnut_mul_acc(&overflow, out_high.limbs[2], a->limbs[6], b->limbs[4]);
    carry_out += overflow;
    out_high.limbs[2] = __chestnut_mul_acc(&overflow, out_high.limbs[2], a->limbs[7], b->limbs[3]);
    carry_out += overflow;

    // Upper limb 3
    out_high.limbs[3] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[4], b->limbs[7]);
    carry_out = overflow;
    out_high.limbs[3] = __chestnut_mul_acc(&overflow, out_high.limbs[3], a->limbs[5], b->limbs[6]);
    carry_out += overflow;
    out_high.limbs[3] = __chestnut_mul_acc(&overflow, out_high.limbs[3], a->limbs[6], b->limbs[5]);
    carry_out += overflow;
    out_high.limbs[3] = __chestnut_mul_acc(&overflow, out_high.limbs[3], a->limbs[7], b->limbs[4]);
    carry_out += overflow;

    // Upper limb 4
    out_high.limbs[4] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[5], b->limbs[7]);
    carry_out = overflow;
    out_high.limbs[4] = __chestnut_mul_acc(&overflow, out_high.limbs[4], a->limbs[6], b->limbs[6]);
    carry_out += overflow;
    out_high.limbs[4] = __chestnut_mul_acc(&overflow, out_high.limbs[4], a->limbs[7], b->limbs[5]);
    carry_out += overflow;

    // Upper limb 5
    out_high.limbs[5] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[6], b->limbs[7]);
    carry_out = overflow;
    out_high.limbs[5] = __chestnut_mul_acc(&overflow, out_high.limbs[5], a->limbs[7], b->limbs[6]);
    carry_out += overflow;

    // Upper limb 6 & 7
    out_high.limbs[6] = __chestnut_mul_acc(&out_high.limbs[7], carry_out, a->limbs[7], b->limbs[7]);

    return out_high;
}

chestnut_uint8_t chestnut_uint1024_t_mul(
    chestnut_uint1024_t *out,
    chestnut_uint1024_t *a,
    chestnut_uint1024_t *b
) {
    chestnut_uint64_t carry_out = 0, overflow = 0;

    // Limb 0
    out->limbs[0] = __chestnut_mul(&overflow, a->limbs[0], b->limbs[0]);

    // Limb 1
    carry_out = overflow;
    out->limbs[1] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[1]);
    carry_out += overflow;
    out->limbs[1] = __chestnut_mul_acc(&overflow, out->limbs[1], a->limbs[1], b->limbs[0]);
    carry_out += overflow;

    // Limb 2
    out->limbs[2] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[2]);
    carry_out = overflow;
    out->limbs[2] = __chestnut_mul_acc(&overflow, out->limbs[2], a->limbs[1], b->limbs[1]);
    carry_out += overflow;
    out->limbs[2] = __chestnut_mul_acc(&overflow, out->limbs[2], a->limbs[2], b->limbs[0]);
    carry_out += overflow;

    // Limb 3
    out->limbs[3] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[3]);
    carry_out = overflow;
    out->limbs[3] = __chestnut_mul_acc(&overflow, out->limbs[3], a->limbs[1], b->limbs[2]);
    carry_out += overflow;
    out->limbs[3] = __chestnut_mul_acc(&overflow, out->limbs[3], a->limbs[2], b->limbs[1]);
    carry_out += overflow;
    out->limbs[3] = __chestnut_mul_acc(&overflow, out->limbs[3], a->limbs[3], b->limbs[0]);
    carry_out += overflow;

    // Limb 4
    out->limbs[4] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[4]);
    carry_out = overflow;
    out->limbs[4] = __chestnut_mul_acc(&overflow, out->limbs[4], a->limbs[1], b->limbs[3]);
    carry_out += overflow;
    out->limbs[4] = __chestnut_mul_acc(&overflow, out->limbs[4], a->limbs[2], b->limbs[2]);
    carry_out += overflow;
    out->limbs[4] = __chestnut_mul_acc(&overflow, out->limbs[4], a->limbs[3], b->limbs[1]);
    carry_out += overflow;
    out->limbs[4] = __chestnut_mul_acc(&overflow, out->limbs[4], a->limbs[4], b->limbs[0]);
    carry_out += overflow;

    // Limb 5
    out->limbs[5] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[5]);
    carry_out = overflow;
    out->limbs[5] = __chestnut_mul_acc(&overflow, out->limbs[5], a->limbs[1], b->limbs[4]);
    carry_out += overflow;
    out->limbs[5] = __chestnut_mul_acc(&overflow, out->limbs[5], a->limbs[2], b->limbs[3]);
    carry_out += overflow;
    out->limbs[5] = __chestnut_mul_acc(&overflow, out->limbs[5], a->limbs[3], b->limbs[2]);
    carry_out += overflow;
    out->limbs[5] = __chestnut_mul_acc(&overflow, out->limbs[5], a->limbs[4], b->limbs[1]);
    carry_out += overflow;
    out->limbs[5] = __chestnut_mul_acc(&overflow, out->limbs[5], a->limbs[5], b->limbs[0]);
    carry_out += overflow;

    // Limb 6
    out->limbs[6] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[6]);
    carry_out = overflow;
    out->limbs[6] = __chestnut_mul_acc(&overflow, out->limbs[6], a->limbs[1], b->limbs[5]);
    carry_out += overflow;
    out->limbs[6] = __chestnut_mul_acc(&overflow, out->limbs[6], a->limbs[2], b->limbs[4]);
    carry_out += overflow;
    out->limbs[6] = __chestnut_mul_acc(&overflow, out->limbs[6], a->limbs[3], b->limbs[3]);
    carry_out += overflow;
    out->limbs[6] = __chestnut_mul_acc(&overflow, out->limbs[6], a->limbs[4], b->limbs[2]);
    carry_out += overflow;
    out->limbs[6] = __chestnut_mul_acc(&overflow, out->limbs[6], a->limbs[5], b->limbs[1]);
    carry_out += overflow;
    out->limbs[6] = __chestnut_mul_acc(&overflow, out->limbs[6], a->limbs[6], b->limbs[0]);
    carry_out += overflow;

    // Limb 7
    out->limbs[7] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[7]);
    carry_out = overflow;
    out->limbs[7] = __chestnut_mul_acc(&overflow, out->limbs[7], a->limbs[1], b->limbs[6]);
    carry_out += overflow;
    out->limbs[7] = __chestnut_mul_acc(&overflow, out->limbs[7], a->limbs[2], b->limbs[5]);
    carry_out += overflow;
    out->limbs[7] = __chestnut_mul_acc(&overflow, out->limbs[7], a->limbs[3], b->limbs[4]);
    carry_out += overflow;
    out->limbs[7] = __chestnut_mul_acc(&overflow, out->limbs[7], a->limbs[4], b->limbs[3]);
    carry_out += overflow;
    out->limbs[7] = __chestnut_mul_acc(&overflow, out->limbs[7], a->limbs[5], b->limbs[2]);
    carry_out += overflow;
    out->limbs[7] = __chestnut_mul_acc(&overflow, out->limbs[7], a->limbs[6], b->limbs[1]);
    carry_out += overflow;
    out->limbs[7] = __chestnut_mul_acc(&overflow, out->limbs[7], a->limbs[7], b->limbs[0]);
    carry_out += overflow;

    // Limb 8
    out->limbs[8] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[8]);
    carry_out = overflow;
    out->limbs[8] = __chestnut_mul_acc(&overflow, out->limbs[8], a->limbs[1], b->limbs[7]);
    carry_out += overflow;
    out->limbs[8] = __chestnut_mul_acc(&overflow, out->limbs[8], a->limbs[2], b->limbs[6]);
    carry_out += overflow;
    out->limbs[8] = __chestnut_mul_acc(&overflow, out->limbs[8], a->limbs[3], b->limbs[5]);
    carry_out += overflow;
    out->limbs[8] = __chestnut_mul_acc(&overflow, out->limbs[8], a->limbs[4], b->limbs[4]);
    carry_out += overflow;
    out->limbs[8] = __chestnut_mul_acc(&overflow, out->limbs[8], a->limbs[5], b->limbs[3]);
    carry_out += overflow;
    out->limbs[8] = __chestnut_mul_acc(&overflow, out->limbs[8], a->limbs[6], b->limbs[2]);
    carry_out += overflow;
    out->limbs[8] = __chestnut_mul_acc(&overflow, out->limbs[8], a->limbs[7], b->limbs[1]);
    carry_out += overflow;
    out->limbs[8] = __chestnut_mul_acc(&overflow, out->limbs[8], a->limbs[8], b->limbs[0]);
    carry_out += overflow;

    // Limb 9
    out->limbs[9] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[9]);
    carry_out = overflow;
    out->limbs[9] = __chestnut_mul_acc(&overflow, out->limbs[9], a->limbs[1], b->limbs[8]);
    carry_out += overflow;
    out->limbs[9] = __chestnut_mul_acc(&overflow, out->limbs[9], a->limbs[2], b->limbs[7]);
    carry_out += overflow;
    out->limbs[9] = __chestnut_mul_acc(&overflow, out->limbs[9], a->limbs[3], b->limbs[6]);
    carry_out += overflow;
    out->limbs[9] = __chestnut_mul_acc(&overflow, out->limbs[9], a->limbs[4], b->limbs[5]);
    carry_out += overflow;
    out->limbs[9] = __chestnut_mul_acc(&overflow, out->limbs[9], a->limbs[5], b->limbs[4]);
    carry_out += overflow;
    out->limbs[9] = __chestnut_mul_acc(&overflow, out->limbs[9], a->limbs[6], b->limbs[3]);
    carry_out += overflow;
    out->limbs[9] = __chestnut_mul_acc(&overflow, out->limbs[9], a->limbs[7], b->limbs[2]);
    carry_out += overflow;
    out->limbs[9] = __chestnut_mul_acc(&overflow, out->limbs[9], a->limbs[8], b->limbs[1]);
    carry_out += overflow;
    out->limbs[9] = __chestnut_mul_acc(&overflow, out->limbs[9], a->limbs[9], b->limbs[0]);
    carry_out += overflow;

    // Limb 10
    out->limbs[10] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[10]);
    carry_out = overflow;
    out->limbs[10] = __chestnut_mul_acc(&overflow, out->limbs[10], a->limbs[1], b->limbs[9]);
    carry_out += overflow;
    out->limbs[10] = __chestnut_mul_acc(&overflow, out->limbs[10], a->limbs[2], b->limbs[8]);
    carry_out += overflow;
    out->limbs[10] = __chestnut_mul_acc(&overflow, out->limbs[10], a->limbs[3], b->limbs[7]);
    carry_out += overflow;
    out->limbs[10] = __chestnut_mul_acc(&overflow, out->limbs[10], a->limbs[4], b->limbs[6]);
    carry_out += overflow;
    out->limbs[10] = __chestnut_mul_acc(&overflow, out->limbs[10], a->limbs[5], b->limbs[5]);
    carry_out += overflow;
    out->limbs[10] = __chestnut_mul_acc(&overflow, out->limbs[10], a->limbs[6], b->limbs[4]);
    carry_out += overflow;
    out->limbs[10] = __chestnut_mul_acc(&overflow, out->limbs[10], a->limbs[7], b->limbs[3]);
    carry_out += overflow;
    out->limbs[10] = __chestnut_mul_acc(&overflow, out->limbs[10], a->limbs[8], b->limbs[2]);
    carry_out += overflow;
    out->limbs[10] = __chestnut_mul_acc(&overflow, out->limbs[10], a->limbs[9], b->limbs[1]);
    carry_out += overflow;
    out->limbs[10] = __chestnut_mul_acc(&overflow, out->limbs[10], a->limbs[10], b->limbs[0]);
    carry_out += overflow;

    // Limb 11
    out->limbs[11] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[11]);
    carry_out = overflow;
    out->limbs[11] = __chestnut_mul_acc(&overflow, out->limbs[11], a->limbs[1], b->limbs[10]);
    carry_out += overflow;
    out->limbs[11] = __chestnut_mul_acc(&overflow, out->limbs[11], a->limbs[2], b->limbs[9]);
    carry_out += overflow;
    out->limbs[11] = __chestnut_mul_acc(&overflow, out->limbs[11], a->limbs[3], b->limbs[8]);
    carry_out += overflow;
    out->limbs[11] = __chestnut_mul_acc(&overflow, out->limbs[11], a->limbs[4], b->limbs[7]);
    carry_out += overflow;
    out->limbs[11] = __chestnut_mul_acc(&overflow, out->limbs[11], a->limbs[5], b->limbs[6]);
    carry_out += overflow;
    out->limbs[11] = __chestnut_mul_acc(&overflow, out->limbs[11], a->limbs[6], b->limbs[5]);
    carry_out += overflow;
    out->limbs[11] = __chestnut_mul_acc(&overflow, out->limbs[11], a->limbs[7], b->limbs[4]);
    carry_out += overflow;
    out->limbs[11] = __chestnut_mul_acc(&overflow, out->limbs[11], a->limbs[8], b->limbs[3]);
    carry_out += overflow;
    out->limbs[11] = __chestnut_mul_acc(&overflow, out->limbs[11], a->limbs[9], b->limbs[2]);
    carry_out += overflow;
    out->limbs[11] = __chestnut_mul_acc(&overflow, out->limbs[11], a->limbs[10], b->limbs[1]);
    carry_out += overflow;
    out->limbs[11] = __chestnut_mul_acc(&overflow, out->limbs[11], a->limbs[11], b->limbs[0]);
    carry_out += overflow;

    // Limb 12
    out->limbs[12] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[12]);
    carry_out = overflow;
    out->limbs[12] = __chestnut_mul_acc(&overflow, out->limbs[12], a->limbs[1], b->limbs[11]);
    carry_out += overflow;
    out->limbs[12] = __chestnut_mul_acc(&overflow, out->limbs[12], a->limbs[2], b->limbs[10]);
    carry_out += overflow;
    out->limbs[12] = __chestnut_mul_acc(&overflow, out->limbs[12], a->limbs[3], b->limbs[9]);
    carry_out += overflow;
    out->limbs[12] = __chestnut_mul_acc(&overflow, out->limbs[12], a->limbs[4], b->limbs[8]);
    carry_out += overflow;
    out->limbs[12] = __chestnut_mul_acc(&overflow, out->limbs[12], a->limbs[5], b->limbs[7]);
    carry_out += overflow;
    out->limbs[12] = __chestnut_mul_acc(&overflow, out->limbs[12], a->limbs[6], b->limbs[6]);
    carry_out += overflow;
    out->limbs[12] = __chestnut_mul_acc(&overflow, out->limbs[12], a->limbs[7], b->limbs[5]);
    carry_out += overflow;
    out->limbs[12] = __chestnut_mul_acc(&overflow, out->limbs[12], a->limbs[8], b->limbs[4]);
    carry_out += overflow;
    out->limbs[12] = __chestnut_mul_acc(&overflow, out->limbs[12], a->limbs[9], b->limbs[3]);
    carry_out += overflow;
    out->limbs[12] = __chestnut_mul_acc(&overflow, out->limbs[12], a->limbs[10], b->limbs[2]);
    carry_out += overflow;
    out->limbs[12] = __chestnut_mul_acc(&overflow, out->limbs[12], a->limbs[11], b->limbs[1]);
    carry_out += overflow;
    out->limbs[12] = __chestnut_mul_acc(&overflow, out->limbs[12], a->limbs[12], b->limbs[0]);
    carry_out += overflow;

    // Limb 13
    out->limbs[13] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[13]);
    carry_out = overflow;
    out->limbs[13] = __chestnut_mul_acc(&overflow, out->limbs[13], a->limbs[1], b->limbs[12]);
    carry_out += overflow;
    out->limbs[13] = __chestnut_mul_acc(&overflow, out->limbs[13], a->limbs[2], b->limbs[11]);
    carry_out += overflow;
    out->limbs[13] = __chestnut_mul_acc(&overflow, out->limbs[13], a->limbs[3], b->limbs[10]);
    carry_out += overflow;
    out->limbs[13] = __chestnut_mul_acc(&overflow, out->limbs[13], a->limbs[4], b->limbs[9]);
    carry_out += overflow;
    out->limbs[13] = __chestnut_mul_acc(&overflow, out->limbs[13], a->limbs[5], b->limbs[8]);
    carry_out += overflow;
    out->limbs[13] = __chestnut_mul_acc(&overflow, out->limbs[13], a->limbs[6], b->limbs[7]);
    carry_out += overflow;
    out->limbs[13] = __chestnut_mul_acc(&overflow, out->limbs[13], a->limbs[7], b->limbs[6]);
    carry_out += overflow;
    out->limbs[13] = __chestnut_mul_acc(&overflow, out->limbs[13], a->limbs[8], b->limbs[5]);
    carry_out += overflow;
    out->limbs[13] = __chestnut_mul_acc(&overflow, out->limbs[13], a->limbs[9], b->limbs[4]);
    carry_out += overflow;
    out->limbs[13] = __chestnut_mul_acc(&overflow, out->limbs[13], a->limbs[10], b->limbs[3]);
    carry_out += overflow;
    out->limbs[13] = __chestnut_mul_acc(&overflow, out->limbs[13], a->limbs[11], b->limbs[2]);
    carry_out += overflow;
    out->limbs[13] = __chestnut_mul_acc(&overflow, out->limbs[13], a->limbs[12], b->limbs[1]);
    carry_out += overflow;
    out->limbs[13] = __chestnut_mul_acc(&overflow, out->limbs[13], a->limbs[13], b->limbs[0]);
    carry_out += overflow;

    // Limb 14
    out->limbs[14] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[14]);
    carry_out = overflow;
    out->limbs[14] = __chestnut_mul_acc(&overflow, out->limbs[14], a->limbs[1], b->limbs[13]);
    carry_out += overflow;
    out->limbs[14] = __chestnut_mul_acc(&overflow, out->limbs[14], a->limbs[2], b->limbs[12]);
    carry_out += overflow;
    out->limbs[14] = __chestnut_mul_acc(&overflow, out->limbs[14], a->limbs[3], b->limbs[11]);
    carry_out += overflow;
    out->limbs[14] = __chestnut_mul_acc(&overflow, out->limbs[14], a->limbs[4], b->limbs[10]);
    carry_out += overflow;
    out->limbs[14] = __chestnut_mul_acc(&overflow, out->limbs[14], a->limbs[5], b->limbs[9]);
    carry_out += overflow;
    out->limbs[14] = __chestnut_mul_acc(&overflow, out->limbs[14], a->limbs[6], b->limbs[8]);
    carry_out += overflow;
    out->limbs[14] = __chestnut_mul_acc(&overflow, out->limbs[14], a->limbs[7], b->limbs[7]);
    carry_out += overflow;
    out->limbs[14] = __chestnut_mul_acc(&overflow, out->limbs[14], a->limbs[8], b->limbs[6]);
    carry_out += overflow;
    out->limbs[14] = __chestnut_mul_acc(&overflow, out->limbs[14], a->limbs[9], b->limbs[5]);
    carry_out += overflow;
    out->limbs[14] = __chestnut_mul_acc(&overflow, out->limbs[14], a->limbs[10], b->limbs[4]);
    carry_out += overflow;
    out->limbs[14] = __chestnut_mul_acc(&overflow, out->limbs[14], a->limbs[11], b->limbs[3]);
    carry_out += overflow;
    out->limbs[14] = __chestnut_mul_acc(&overflow, out->limbs[14], a->limbs[12], b->limbs[2]);
    carry_out += overflow;
    out->limbs[14] = __chestnut_mul_acc(&overflow, out->limbs[14], a->limbs[13], b->limbs[1]);
    carry_out += overflow;
    out->limbs[14] = __chestnut_mul_acc(&overflow, out->limbs[14], a->limbs[14], b->limbs[0]);
    carry_out += overflow;

    // Limb 15
    out->limbs[15] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[15]);
    carry_out = overflow;
    out->limbs[15] = __chestnut_mul_acc(&overflow, out->limbs[15], a->limbs[1], b->limbs[14]);
    carry_out += overflow;
    out->limbs[15] = __chestnut_mul_acc(&overflow, out->limbs[15], a->limbs[2], b->limbs[13]);
    carry_out += overflow;
    out->limbs[15] = __chestnut_mul_acc(&overflow, out->limbs[15], a->limbs[3], b->limbs[12]);
    carry_out += overflow;
    out->limbs[15] = __chestnut_mul_acc(&overflow, out->limbs[15], a->limbs[4], b->limbs[11]);
    carry_out += overflow;
    out->limbs[15] = __chestnut_mul_acc(&overflow, out->limbs[15], a->limbs[5], b->limbs[10]);
    carry_out += overflow;
    out->limbs[15] = __chestnut_mul_acc(&overflow, out->limbs[15], a->limbs[6], b->limbs[9]);
    carry_out += overflow;
    out->limbs[15] = __chestnut_mul_acc(&overflow, out->limbs[15], a->limbs[7], b->limbs[8]);
    carry_out += overflow;
    out->limbs[15] = __chestnut_mul_acc(&overflow, out->limbs[15], a->limbs[8], b->limbs[7]);
    carry_out += overflow;
    out->limbs[15] = __chestnut_mul_acc(&overflow, out->limbs[15], a->limbs[9], b->limbs[6]);
    carry_out += overflow;
    out->limbs[15] = __chestnut_mul_acc(&overflow, out->limbs[15], a->limbs[10], b->limbs[5]);
    carry_out += overflow;
    out->limbs[15] = __chestnut_mul_acc(&overflow, out->limbs[15], a->limbs[11], b->limbs[4]);
    carry_out += overflow;
    out->limbs[15] = __chestnut_mul_acc(&overflow, out->limbs[15], a->limbs[12], b->limbs[3]);
    carry_out += overflow;
    out->limbs[15] = __chestnut_mul_acc(&overflow, out->limbs[15], a->limbs[13], b->limbs[2]);
    carry_out += overflow;
    out->limbs[15] = __chestnut_mul_acc(&overflow, out->limbs[15], a->limbs[14], b->limbs[1]);
    carry_out += overflow;
    out->limbs[15] = __chestnut_mul_acc(&overflow, out->limbs[15], a->limbs[15], b->limbs[0]);
    carry_out += overflow;

    return (chestnut_uint8_t)(!!carry_out);
}

chestnut_uint1024_t chestnut_uint1024_t_mul_full(
    chestnut_uint1024_t *out_low,
    chestnut_uint1024_t *a,
    chestnut_uint1024_t *b
) {
    chestnut_uint1024_t out_high;
    chestnut_uint64_t carry_in = 0, carry_out = 0, overflow = 0;

    // Low limb 0
    out_low->limbs[0] = __chestnut_mul(&carry_out, a->limbs[0], b->limbs[0]);

    // Lower limb 1
    out_low->limbs[1] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[1]);
    carry_out = overflow;
    out_low->limbs[1] = __chestnut_mul_acc(&overflow, out_low->limbs[1], a->limbs[1], b->limbs[0]);
    carry_out += overflow;

    // Lower limb 2
    out_low->limbs[2] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[2]);
    carry_out = overflow;
    out_low->limbs[2] = __chestnut_mul_acc(&overflow, out_low->limbs[2], a->limbs[1], b->limbs[1]);
    carry_out += overflow;
    out_low->limbs[2] = __chestnut_mul_acc(&overflow, out_low->limbs[2], a->limbs[2], b->limbs[0]);
    carry_out += overflow;

    // Lower limb 3
    out_low->limbs[3] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[3]);
    carry_out = overflow;
    out_low->limbs[3] = __chestnut_mul_acc(&overflow, out_low->limbs[3], a->limbs[1], b->limbs[2]);
    carry_out += overflow;
    out_low->limbs[3] = __chestnut_mul_acc(&overflow, out_low->limbs[3], a->limbs[2], b->limbs[1]);
    carry_out += overflow;
    out_low->limbs[3] = __chestnut_mul_acc(&overflow, out_low->limbs[3], a->limbs[3], b->limbs[0]);
    carry_out += overflow;

    // Lower limb 4
    out_low->limbs[4] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[4]);
    carry_out = overflow;
    out_low->limbs[4] = __chestnut_mul_acc(&overflow, out_low->limbs[4], a->limbs[1], b->limbs[3]);
    carry_out += overflow;
    out_low->limbs[4] = __chestnut_mul_acc(&overflow, out_low->limbs[4], a->limbs[2], b->limbs[2]);
    carry_out += overflow;
    out_low->limbs[4] = __chestnut_mul_acc(&overflow, out_low->limbs[4], a->limbs[3], b->limbs[1]);
    carry_out += overflow;
    out_low->limbs[4] = __chestnut_mul_acc(&overflow, out_low->limbs[4], a->limbs[4], b->limbs[0]);
    carry_out += overflow;

    // Lower limb 5
    out_low->limbs[5] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[5]);
    carry_out = overflow;
    out_low->limbs[5] = __chestnut_mul_acc(&overflow, out_low->limbs[5], a->limbs[1], b->limbs[4]);
    carry_out += overflow;
    out_low->limbs[5] = __chestnut_mul_acc(&overflow, out_low->limbs[5], a->limbs[2], b->limbs[3]);
    carry_out += overflow;
    out_low->limbs[5] = __chestnut_mul_acc(&overflow, out_low->limbs[5], a->limbs[3], b->limbs[2]);
    carry_out += overflow;
    out_low->limbs[5] = __chestnut_mul_acc(&overflow, out_low->limbs[5], a->limbs[4], b->limbs[1]);
    carry_out += overflow;
    out_low->limbs[5] = __chestnut_mul_acc(&overflow, out_low->limbs[5], a->limbs[5], b->limbs[0]);
    carry_out += overflow;

    // Lower limb 6
    out_low->limbs[6] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[6]);
    carry_out = overflow;
    out_low->limbs[6] = __chestnut_mul_acc(&overflow, out_low->limbs[6], a->limbs[1], b->limbs[5]);
    carry_out += overflow;
    out_low->limbs[6] = __chestnut_mul_acc(&overflow, out_low->limbs[6], a->limbs[2], b->limbs[4]);
    carry_out += overflow;
    out_low->limbs[6] = __chestnut_mul_acc(&overflow, out_low->limbs[6], a->limbs[3], b->limbs[3]);
    carry_out += overflow;
    out_low->limbs[6] = __chestnut_mul_acc(&overflow, out_low->limbs[6], a->limbs[4], b->limbs[2]);
    carry_out += overflow;
    out_low->limbs[6] = __chestnut_mul_acc(&overflow, out_low->limbs[6], a->limbs[5], b->limbs[1]);
    carry_out += overflow;
    out_low->limbs[6] = __chestnut_mul_acc(&overflow, out_low->limbs[6], a->limbs[6], b->limbs[0]);
    carry_out += overflow;

    // Lower limb 7
    out_low->limbs[7] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[7]);
    carry_out = overflow;
    out_low->limbs[7] = __chestnut_mul_acc(&overflow, out_low->limbs[7], a->limbs[1], b->limbs[6]);
    carry_out += overflow;
    out_low->limbs[7] = __chestnut_mul_acc(&overflow, out_low->limbs[7], a->limbs[2], b->limbs[5]);
    carry_out += overflow;
    out_low->limbs[7] = __chestnut_mul_acc(&overflow, out_low->limbs[7], a->limbs[3], b->limbs[4]);
    carry_out += overflow;
    out_low->limbs[7] = __chestnut_mul_acc(&overflow, out_low->limbs[7], a->limbs[4], b->limbs[3]);
    carry_out += overflow;
    out_low->limbs[7] = __chestnut_mul_acc(&overflow, out_low->limbs[7], a->limbs[5], b->limbs[2]);
    carry_out += overflow;
    out_low->limbs[7] = __chestnut_mul_acc(&overflow, out_low->limbs[7], a->limbs[6], b->limbs[1]);
    carry_out += overflow;
    out_low->limbs[7] = __chestnut_mul_acc(&overflow, out_low->limbs[7], a->limbs[7], b->limbs[0]);
    carry_out += overflow;

    // Lower limb 8
    out_low->limbs[8] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[8]);
    carry_out = overflow;
    out_low->limbs[8] = __chestnut_mul_acc(&overflow, out_low->limbs[8], a->limbs[1], b->limbs[7]);
    carry_out += overflow;
    out_low->limbs[8] = __chestnut_mul_acc(&overflow, out_low->limbs[8], a->limbs[2], b->limbs[6]);
    carry_out += overflow;
    out_low->limbs[8] = __chestnut_mul_acc(&overflow, out_low->limbs[8], a->limbs[3], b->limbs[5]);
    carry_out += overflow;
    out_low->limbs[8] = __chestnut_mul_acc(&overflow, out_low->limbs[8], a->limbs[4], b->limbs[4]);
    carry_out += overflow;
    out_low->limbs[8] = __chestnut_mul_acc(&overflow, out_low->limbs[8], a->limbs[5], b->limbs[3]);
    carry_out += overflow;
    out_low->limbs[8] = __chestnut_mul_acc(&overflow, out_low->limbs[8], a->limbs[6], b->limbs[2]);
    carry_out += overflow;
    out_low->limbs[8] = __chestnut_mul_acc(&overflow, out_low->limbs[8], a->limbs[7], b->limbs[1]);
    carry_out += overflow;
    out_low->limbs[8] = __chestnut_mul_acc(&overflow, out_low->limbs[8], a->limbs[8], b->limbs[0]);
    carry_out += overflow;

    // Lower limb 9
    out_low->limbs[9] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[9]);
    carry_out = overflow;
    out_low->limbs[9] = __chestnut_mul_acc(&overflow, out_low->limbs[9], a->limbs[1], b->limbs[8]);
    carry_out += overflow;
    out_low->limbs[9] = __chestnut_mul_acc(&overflow, out_low->limbs[9], a->limbs[2], b->limbs[7]);
    carry_out += overflow;
    out_low->limbs[9] = __chestnut_mul_acc(&overflow, out_low->limbs[9], a->limbs[3], b->limbs[6]);
    carry_out += overflow;
    out_low->limbs[9] = __chestnut_mul_acc(&overflow, out_low->limbs[9], a->limbs[4], b->limbs[5]);
    carry_out += overflow;
    out_low->limbs[9] = __chestnut_mul_acc(&overflow, out_low->limbs[9], a->limbs[5], b->limbs[4]);
    carry_out += overflow;
    out_low->limbs[9] = __chestnut_mul_acc(&overflow, out_low->limbs[9], a->limbs[6], b->limbs[3]);
    carry_out += overflow;
    out_low->limbs[9] = __chestnut_mul_acc(&overflow, out_low->limbs[9], a->limbs[7], b->limbs[2]);
    carry_out += overflow;
    out_low->limbs[9] = __chestnut_mul_acc(&overflow, out_low->limbs[9], a->limbs[8], b->limbs[1]);
    carry_out += overflow;
    out_low->limbs[9] = __chestnut_mul_acc(&overflow, out_low->limbs[9], a->limbs[9], b->limbs[0]);
    carry_out += overflow;

    // Lower limb 10
    out_low->limbs[10] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[10]);
    carry_out = overflow;
    out_low->limbs[10] = __chestnut_mul_acc(&overflow, out_low->limbs[10], a->limbs[1], b->limbs[9]);
    carry_out += overflow;
    out_low->limbs[10] = __chestnut_mul_acc(&overflow, out_low->limbs[10], a->limbs[2], b->limbs[8]);
    carry_out += overflow;
    out_low->limbs[10] = __chestnut_mul_acc(&overflow, out_low->limbs[10], a->limbs[3], b->limbs[7]);
    carry_out += overflow;
    out_low->limbs[10] = __chestnut_mul_acc(&overflow, out_low->limbs[10], a->limbs[4], b->limbs[6]);
    carry_out += overflow;
    out_low->limbs[10] = __chestnut_mul_acc(&overflow, out_low->limbs[10], a->limbs[5], b->limbs[5]);
    carry_out += overflow;
    out_low->limbs[10] = __chestnut_mul_acc(&overflow, out_low->limbs[10], a->limbs[6], b->limbs[4]);
    carry_out += overflow;
    out_low->limbs[10] = __chestnut_mul_acc(&overflow, out_low->limbs[10], a->limbs[7], b->limbs[3]);
    carry_out += overflow;
    out_low->limbs[10] = __chestnut_mul_acc(&overflow, out_low->limbs[10], a->limbs[8], b->limbs[2]);
    carry_out += overflow;
    out_low->limbs[10] = __chestnut_mul_acc(&overflow, out_low->limbs[10], a->limbs[9], b->limbs[1]);
    carry_out += overflow;
    out_low->limbs[10] = __chestnut_mul_acc(&overflow, out_low->limbs[10], a->limbs[10], b->limbs[0]);
    carry_out += overflow;

    // Lower limb 11
    out_low->limbs[11] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[11]);
    carry_out = overflow;
    out_low->limbs[11] = __chestnut_mul_acc(&overflow, out_low->limbs[11], a->limbs[1], b->limbs[10]);
    carry_out += overflow;
    out_low->limbs[11] = __chestnut_mul_acc(&overflow, out_low->limbs[11], a->limbs[2], b->limbs[9]);
    carry_out += overflow;
    out_low->limbs[11] = __chestnut_mul_acc(&overflow, out_low->limbs[11], a->limbs[3], b->limbs[8]);
    carry_out += overflow;
    out_low->limbs[11] = __chestnut_mul_acc(&overflow, out_low->limbs[11], a->limbs[4], b->limbs[7]);
    carry_out += overflow;
    out_low->limbs[11] = __chestnut_mul_acc(&overflow, out_low->limbs[11], a->limbs[5], b->limbs[6]);
    carry_out += overflow;
    out_low->limbs[11] = __chestnut_mul_acc(&overflow, out_low->limbs[11], a->limbs[6], b->limbs[5]);
    carry_out += overflow;
    out_low->limbs[11] = __chestnut_mul_acc(&overflow, out_low->limbs[11], a->limbs[7], b->limbs[4]);
    carry_out += overflow;
    out_low->limbs[11] = __chestnut_mul_acc(&overflow, out_low->limbs[11], a->limbs[8], b->limbs[3]);
    carry_out += overflow;
    out_low->limbs[11] = __chestnut_mul_acc(&overflow, out_low->limbs[11], a->limbs[9], b->limbs[2]);
    carry_out += overflow;
    out_low->limbs[11] = __chestnut_mul_acc(&overflow, out_low->limbs[11], a->limbs[10], b->limbs[1]);
    carry_out += overflow;
    out_low->limbs[11] = __chestnut_mul_acc(&overflow, out_low->limbs[11], a->limbs[11], b->limbs[0]);
    carry_out += overflow;

    // Lower limb 12
    out_low->limbs[12] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[12]);
    carry_out = overflow;
    out_low->limbs[12] = __chestnut_mul_acc(&overflow, out_low->limbs[12], a->limbs[1], b->limbs[11]);
    carry_out += overflow;
    out_low->limbs[12] = __chestnut_mul_acc(&overflow, out_low->limbs[12], a->limbs[2], b->limbs[10]);
    carry_out += overflow;
    out_low->limbs[12] = __chestnut_mul_acc(&overflow, out_low->limbs[12], a->limbs[3], b->limbs[9]);
    carry_out += overflow;
    out_low->limbs[12] = __chestnut_mul_acc(&overflow, out_low->limbs[12], a->limbs[4], b->limbs[8]);
    carry_out += overflow;
    out_low->limbs[12] = __chestnut_mul_acc(&overflow, out_low->limbs[12], a->limbs[5], b->limbs[7]);
    carry_out += overflow;
    out_low->limbs[12] = __chestnut_mul_acc(&overflow, out_low->limbs[12], a->limbs[6], b->limbs[6]);
    carry_out += overflow;
    out_low->limbs[12] = __chestnut_mul_acc(&overflow, out_low->limbs[12], a->limbs[7], b->limbs[5]);
    carry_out += overflow;
    out_low->limbs[12] = __chestnut_mul_acc(&overflow, out_low->limbs[12], a->limbs[8], b->limbs[4]);
    carry_out += overflow;
    out_low->limbs[12] = __chestnut_mul_acc(&overflow, out_low->limbs[12], a->limbs[9], b->limbs[3]);
    carry_out += overflow;
    out_low->limbs[12] = __chestnut_mul_acc(&overflow, out_low->limbs[12], a->limbs[10], b->limbs[2]);
    carry_out += overflow;
    out_low->limbs[12] = __chestnut_mul_acc(&overflow, out_low->limbs[12], a->limbs[11], b->limbs[1]);
    carry_out += overflow;
    out_low->limbs[12] = __chestnut_mul_acc(&overflow, out_low->limbs[12], a->limbs[12], b->limbs[0]);
    carry_out += overflow;

    // Lower limb 13
    out_low->limbs[13] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[13]);
    carry_out = overflow;
    out_low->limbs[13] = __chestnut_mul_acc(&overflow, out_low->limbs[13], a->limbs[1], b->limbs[12]);
    carry_out += overflow;
    out_low->limbs[13] = __chestnut_mul_acc(&overflow, out_low->limbs[13], a->limbs[2], b->limbs[11]);
    carry_out += overflow;
    out_low->limbs[13] = __chestnut_mul_acc(&overflow, out_low->limbs[13], a->limbs[3], b->limbs[10]);
    carry_out += overflow;
    out_low->limbs[13] = __chestnut_mul_acc(&overflow, out_low->limbs[13], a->limbs[4], b->limbs[9]);
    carry_out += overflow;
    out_low->limbs[13] = __chestnut_mul_acc(&overflow, out_low->limbs[13], a->limbs[5], b->limbs[8]);
    carry_out += overflow;
    out_low->limbs[13] = __chestnut_mul_acc(&overflow, out_low->limbs[13], a->limbs[6], b->limbs[7]);
    carry_out += overflow;
    out_low->limbs[13] = __chestnut_mul_acc(&overflow, out_low->limbs[13], a->limbs[7], b->limbs[6]);
    carry_out += overflow;
    out_low->limbs[13] = __chestnut_mul_acc(&overflow, out_low->limbs[13], a->limbs[8], b->limbs[5]);
    carry_out += overflow;
    out_low->limbs[13] = __chestnut_mul_acc(&overflow, out_low->limbs[13], a->limbs[9], b->limbs[4]);
    carry_out += overflow;
    out_low->limbs[13] = __chestnut_mul_acc(&overflow, out_low->limbs[13], a->limbs[10], b->limbs[3]);
    carry_out += overflow;
    out_low->limbs[13] = __chestnut_mul_acc(&overflow, out_low->limbs[13], a->limbs[11], b->limbs[2]);
    carry_out += overflow;
    out_low->limbs[13] = __chestnut_mul_acc(&overflow, out_low->limbs[13], a->limbs[12], b->limbs[1]);
    carry_out += overflow;
    out_low->limbs[13] = __chestnut_mul_acc(&overflow, out_low->limbs[13], a->limbs[13], b->limbs[0]);
    carry_out += overflow;

    // Lower limb 14
    out_low->limbs[14] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[14]);
    carry_out = overflow;
    out_low->limbs[14] = __chestnut_mul_acc(&overflow, out_low->limbs[14], a->limbs[1], b->limbs[13]);
    carry_out += overflow;
    out_low->limbs[14] = __chestnut_mul_acc(&overflow, out_low->limbs[14], a->limbs[2], b->limbs[12]);
    carry_out += overflow;
    out_low->limbs[14] = __chestnut_mul_acc(&overflow, out_low->limbs[14], a->limbs[3], b->limbs[11]);
    carry_out += overflow;
    out_low->limbs[14] = __chestnut_mul_acc(&overflow, out_low->limbs[14], a->limbs[4], b->limbs[10]);
    carry_out += overflow;
    out_low->limbs[14] = __chestnut_mul_acc(&overflow, out_low->limbs[14], a->limbs[5], b->limbs[9]);
    carry_out += overflow;
    out_low->limbs[14] = __chestnut_mul_acc(&overflow, out_low->limbs[14], a->limbs[6], b->limbs[8]);
    carry_out += overflow;
    out_low->limbs[14] = __chestnut_mul_acc(&overflow, out_low->limbs[14], a->limbs[7], b->limbs[7]);
    carry_out += overflow;
    out_low->limbs[14] = __chestnut_mul_acc(&overflow, out_low->limbs[14], a->limbs[8], b->limbs[6]);
    carry_out += overflow;
    out_low->limbs[14] = __chestnut_mul_acc(&overflow, out_low->limbs[14], a->limbs[9], b->limbs[5]);
    carry_out += overflow;
    out_low->limbs[14] = __chestnut_mul_acc(&overflow, out_low->limbs[14], a->limbs[10], b->limbs[4]);
    carry_out += overflow;
    out_low->limbs[14] = __chestnut_mul_acc(&overflow, out_low->limbs[14], a->limbs[11], b->limbs[3]);
    carry_out += overflow;
    out_low->limbs[14] = __chestnut_mul_acc(&overflow, out_low->limbs[14], a->limbs[12], b->limbs[2]);
    carry_out += overflow;
    out_low->limbs[14] = __chestnut_mul_acc(&overflow, out_low->limbs[14], a->limbs[13], b->limbs[1]);
    carry_out += overflow;
    out_low->limbs[14] = __chestnut_mul_acc(&overflow, out_low->limbs[14], a->limbs[14], b->limbs[0]);
    carry_out += overflow;

    // Lower limb 15
    out_low->limbs[15] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[0], b->limbs[15]);
    carry_out = overflow;
    out_low->limbs[15] = __chestnut_mul_acc(&overflow, out_low->limbs[15], a->limbs[1], b->limbs[14]);
    carry_out += overflow;
    out_low->limbs[15] = __chestnut_mul_acc(&overflow, out_low->limbs[15], a->limbs[2], b->limbs[13]);
    carry_out += overflow;
    out_low->limbs[15] = __chestnut_mul_acc(&overflow, out_low->limbs[15], a->limbs[3], b->limbs[12]);
    carry_out += overflow;
    out_low->limbs[15] = __chestnut_mul_acc(&overflow, out_low->limbs[15], a->limbs[4], b->limbs[11]);
    carry_out += overflow;
    out_low->limbs[15] = __chestnut_mul_acc(&overflow, out_low->limbs[15], a->limbs[5], b->limbs[10]);
    carry_out += overflow;
    out_low->limbs[15] = __chestnut_mul_acc(&overflow, out_low->limbs[15], a->limbs[6], b->limbs[9]);
    carry_out += overflow;
    out_low->limbs[15] = __chestnut_mul_acc(&overflow, out_low->limbs[15], a->limbs[7], b->limbs[8]);
    carry_out += overflow;
    out_low->limbs[15] = __chestnut_mul_acc(&overflow, out_low->limbs[15], a->limbs[8], b->limbs[7]);
    carry_out += overflow;
    out_low->limbs[15] = __chestnut_mul_acc(&overflow, out_low->limbs[15], a->limbs[9], b->limbs[6]);
    carry_out += overflow;
    out_low->limbs[15] = __chestnut_mul_acc(&overflow, out_low->limbs[15], a->limbs[10], b->limbs[5]);
    carry_out += overflow;
    out_low->limbs[15] = __chestnut_mul_acc(&overflow, out_low->limbs[15], a->limbs[11], b->limbs[4]);
    carry_out += overflow;
    out_low->limbs[15] = __chestnut_mul_acc(&overflow, out_low->limbs[15], a->limbs[12], b->limbs[3]);
    carry_out += overflow;
    out_low->limbs[15] = __chestnut_mul_acc(&overflow, out_low->limbs[15], a->limbs[13], b->limbs[2]);
    carry_out += overflow;
    out_low->limbs[15] = __chestnut_mul_acc(&overflow, out_low->limbs[15], a->limbs[14], b->limbs[1]);
    carry_out += overflow;
    out_low->limbs[15] = __chestnut_mul_acc(&overflow, out_low->limbs[15], a->limbs[15], b->limbs[0]);
    carry_out += overflow;

    // Upper limb 0
    out_high.limbs[0] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[1], b->limbs[15]);
    carry_out = overflow;
    out_high.limbs[0] = __chestnut_mul_acc(&overflow, out_high.limbs[0], a->limbs[2], b->limbs[14]);
    carry_out += overflow;
    out_high.limbs[0] = __chestnut_mul_acc(&overflow, out_high.limbs[0], a->limbs[3], b->limbs[13]);
    carry_out += overflow;
    out_high.limbs[0] = __chestnut_mul_acc(&overflow, out_high.limbs[0], a->limbs[4], b->limbs[12]);
    carry_out += overflow;
    out_high.limbs[0] = __chestnut_mul_acc(&overflow, out_high.limbs[0], a->limbs[5], b->limbs[11]);
    carry_out += overflow;
    out_high.limbs[0] = __chestnut_mul_acc(&overflow, out_high.limbs[0], a->limbs[6], b->limbs[10]);
    carry_out += overflow;
    out_high.limbs[0] = __chestnut_mul_acc(&overflow, out_high.limbs[0], a->limbs[7], b->limbs[9]);
    carry_out += overflow;
    out_high.limbs[0] = __chestnut_mul_acc(&overflow, out_high.limbs[0], a->limbs[8], b->limbs[8]);
    carry_out += overflow;
    out_high.limbs[0] = __chestnut_mul_acc(&overflow, out_high.limbs[0], a->limbs[9], b->limbs[7]);
    carry_out += overflow;
    out_high.limbs[0] = __chestnut_mul_acc(&overflow, out_high.limbs[0], a->limbs[10], b->limbs[6]);
    carry_out += overflow;
    out_high.limbs[0] = __chestnut_mul_acc(&overflow, out_high.limbs[0], a->limbs[11], b->limbs[5]);
    carry_out += overflow;
    out_high.limbs[0] = __chestnut_mul_acc(&overflow, out_high.limbs[0], a->limbs[12], b->limbs[4]);
    carry_out += overflow;
    out_high.limbs[0] = __chestnut_mul_acc(&overflow, out_high.limbs[0], a->limbs[13], b->limbs[3]);
    carry_out += overflow;
    out_high.limbs[0] = __chestnut_mul_acc(&overflow, out_high.limbs[0], a->limbs[14], b->limbs[2]);
    carry_out += overflow;
    out_high.limbs[0] = __chestnut_mul_acc(&overflow, out_high.limbs[0], a->limbs[15], b->limbs[1]);
    carry_out += overflow;

    // Upper limb 1
    out_high.limbs[1] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[2], b->limbs[15]);
    carry_out = overflow;
    out_high.limbs[1] = __chestnut_mul_acc(&overflow, out_high.limbs[1], a->limbs[3], b->limbs[14]);
    carry_out += overflow;
    out_high.limbs[1] = __chestnut_mul_acc(&overflow, out_high.limbs[1], a->limbs[4], b->limbs[13]);
    carry_out += overflow;
    out_high.limbs[1] = __chestnut_mul_acc(&overflow, out_high.limbs[1], a->limbs[5], b->limbs[12]);
    carry_out += overflow;
    out_high.limbs[1] = __chestnut_mul_acc(&overflow, out_high.limbs[1], a->limbs[6], b->limbs[11]);
    carry_out += overflow;
    out_high.limbs[1] = __chestnut_mul_acc(&overflow, out_high.limbs[1], a->limbs[7], b->limbs[10]);
    carry_out += overflow;
    out_high.limbs[1] = __chestnut_mul_acc(&overflow, out_high.limbs[1], a->limbs[8], b->limbs[9]);
    carry_out += overflow;
    out_high.limbs[1] = __chestnut_mul_acc(&overflow, out_high.limbs[1], a->limbs[9], b->limbs[8]);
    carry_out += overflow;
    out_high.limbs[1] = __chestnut_mul_acc(&overflow, out_high.limbs[1], a->limbs[10], b->limbs[7]);
    carry_out += overflow;
    out_high.limbs[1] = __chestnut_mul_acc(&overflow, out_high.limbs[1], a->limbs[11], b->limbs[6]);
    carry_out += overflow;
    out_high.limbs[1] = __chestnut_mul_acc(&overflow, out_high.limbs[1], a->limbs[12], b->limbs[5]);
    carry_out += overflow;
    out_high.limbs[1] = __chestnut_mul_acc(&overflow, out_high.limbs[1], a->limbs[13], b->limbs[4]);
    carry_out += overflow;
    out_high.limbs[1] = __chestnut_mul_acc(&overflow, out_high.limbs[1], a->limbs[14], b->limbs[3]);
    carry_out += overflow;
    out_high.limbs[1] = __chestnut_mul_acc(&overflow, out_high.limbs[1], a->limbs[15], b->limbs[2]);
    carry_out += overflow;

    // Upper limb 2
    out_high.limbs[2] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[3], b->limbs[15]);
    carry_out = overflow;
    out_high.limbs[2] = __chestnut_mul_acc(&overflow, out_high.limbs[2], a->limbs[4], b->limbs[14]);
    carry_out += overflow;
    out_high.limbs[2] = __chestnut_mul_acc(&overflow, out_high.limbs[2], a->limbs[5], b->limbs[13]);
    carry_out += overflow;
    out_high.limbs[2] = __chestnut_mul_acc(&overflow, out_high.limbs[2], a->limbs[6], b->limbs[12]);
    carry_out += overflow;
    out_high.limbs[2] = __chestnut_mul_acc(&overflow, out_high.limbs[2], a->limbs[7], b->limbs[11]);
    carry_out += overflow;
    out_high.limbs[2] = __chestnut_mul_acc(&overflow, out_high.limbs[2], a->limbs[8], b->limbs[10]);
    carry_out += overflow;
    out_high.limbs[2] = __chestnut_mul_acc(&overflow, out_high.limbs[2], a->limbs[9], b->limbs[9]);
    carry_out += overflow;
    out_high.limbs[2] = __chestnut_mul_acc(&overflow, out_high.limbs[2], a->limbs[10], b->limbs[8]);
    carry_out += overflow;
    out_high.limbs[2] = __chestnut_mul_acc(&overflow, out_high.limbs[2], a->limbs[11], b->limbs[7]);
    carry_out += overflow;
    out_high.limbs[2] = __chestnut_mul_acc(&overflow, out_high.limbs[2], a->limbs[12], b->limbs[6]);
    carry_out += overflow;
    out_high.limbs[2] = __chestnut_mul_acc(&overflow, out_high.limbs[2], a->limbs[13], b->limbs[5]);
    carry_out += overflow;
    out_high.limbs[2] = __chestnut_mul_acc(&overflow, out_high.limbs[2], a->limbs[14], b->limbs[4]);
    carry_out += overflow;
    out_high.limbs[2] = __chestnut_mul_acc(&overflow, out_high.limbs[2], a->limbs[15], b->limbs[3]);
    carry_out += overflow;

    // Upper limb 3
    out_high.limbs[3] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[4], b->limbs[15]);
    carry_out = overflow;
    out_high.limbs[3] = __chestnut_mul_acc(&overflow, out_high.limbs[3], a->limbs[5], b->limbs[14]);
    carry_out += overflow;
    out_high.limbs[3] = __chestnut_mul_acc(&overflow, out_high.limbs[3], a->limbs[6], b->limbs[13]);
    carry_out += overflow;
    out_high.limbs[3] = __chestnut_mul_acc(&overflow, out_high.limbs[3], a->limbs[7], b->limbs[12]);
    carry_out += overflow;
    out_high.limbs[3] = __chestnut_mul_acc(&overflow, out_high.limbs[3], a->limbs[8], b->limbs[11]);
    carry_out += overflow;
    out_high.limbs[3] = __chestnut_mul_acc(&overflow, out_high.limbs[3], a->limbs[9], b->limbs[10]);
    carry_out += overflow;
    out_high.limbs[3] = __chestnut_mul_acc(&overflow, out_high.limbs[3], a->limbs[10], b->limbs[9]);
    carry_out += overflow;
    out_high.limbs[3] = __chestnut_mul_acc(&overflow, out_high.limbs[3], a->limbs[11], b->limbs[8]);
    carry_out += overflow;
    out_high.limbs[3] = __chestnut_mul_acc(&overflow, out_high.limbs[3], a->limbs[12], b->limbs[7]);
    carry_out += overflow;
    out_high.limbs[3] = __chestnut_mul_acc(&overflow, out_high.limbs[3], a->limbs[13], b->limbs[6]);
    carry_out += overflow;
    out_high.limbs[3] = __chestnut_mul_acc(&overflow, out_high.limbs[3], a->limbs[14], b->limbs[5]);
    carry_out += overflow;
    out_high.limbs[3] = __chestnut_mul_acc(&overflow, out_high.limbs[3], a->limbs[15], b->limbs[4]);
    carry_out += overflow;
    
    // Upper limb 4
    out_high.limbs[4] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[5], b->limbs[15]);
    carry_out = overflow;
    out_high.limbs[4] = __chestnut_mul_acc(&overflow, out_high.limbs[4], a->limbs[6], b->limbs[14]);
    carry_out += overflow;
    out_high.limbs[4] = __chestnut_mul_acc(&overflow, out_high.limbs[4], a->limbs[7], b->limbs[13]);
    carry_out += overflow;
    out_high.limbs[4] = __chestnut_mul_acc(&overflow, out_high.limbs[4], a->limbs[8], b->limbs[12]);
    carry_out += overflow;
    out_high.limbs[4] = __chestnut_mul_acc(&overflow, out_high.limbs[4], a->limbs[9], b->limbs[11]);
    carry_out += overflow;
    out_high.limbs[4] = __chestnut_mul_acc(&overflow, out_high.limbs[4], a->limbs[10], b->limbs[10]);
    carry_out += overflow;
    out_high.limbs[4] = __chestnut_mul_acc(&overflow, out_high.limbs[4], a->limbs[11], b->limbs[9]);
    carry_out += overflow;
    out_high.limbs[4] = __chestnut_mul_acc(&overflow, out_high.limbs[4], a->limbs[12], b->limbs[8]);
    carry_out += overflow;
    out_high.limbs[4] = __chestnut_mul_acc(&overflow, out_high.limbs[4], a->limbs[13], b->limbs[7]);
    carry_out += overflow;
    out_high.limbs[4] = __chestnut_mul_acc(&overflow, out_high.limbs[4], a->limbs[14], b->limbs[6]);
    carry_out += overflow;
    out_high.limbs[4] = __chestnut_mul_acc(&overflow, out_high.limbs[4], a->limbs[15], b->limbs[5]);
    carry_out += overflow;
    
    // Upper limb 5
    out_high.limbs[5] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[6], b->limbs[15]);
    carry_out = overflow;
    out_high.limbs[5] = __chestnut_mul_acc(&overflow, out_high.limbs[5], a->limbs[7], b->limbs[14]);
    carry_out += overflow;
    out_high.limbs[5] = __chestnut_mul_acc(&overflow, out_high.limbs[5], a->limbs[8], b->limbs[13]);
    carry_out += overflow;
    out_high.limbs[5] = __chestnut_mul_acc(&overflow, out_high.limbs[5], a->limbs[9], b->limbs[12]);
    carry_out += overflow;
    out_high.limbs[5] = __chestnut_mul_acc(&overflow, out_high.limbs[5], a->limbs[10], b->limbs[11]);
    carry_out += overflow;
    out_high.limbs[5] = __chestnut_mul_acc(&overflow, out_high.limbs[5], a->limbs[11], b->limbs[10]);
    carry_out += overflow;
    out_high.limbs[5] = __chestnut_mul_acc(&overflow, out_high.limbs[5], a->limbs[12], b->limbs[9]);
    carry_out += overflow;
    out_high.limbs[5] = __chestnut_mul_acc(&overflow, out_high.limbs[5], a->limbs[13], b->limbs[8]);
    carry_out += overflow;
    out_high.limbs[5] = __chestnut_mul_acc(&overflow, out_high.limbs[5], a->limbs[14], b->limbs[7]);
    carry_out += overflow;
    out_high.limbs[5] = __chestnut_mul_acc(&overflow, out_high.limbs[5], a->limbs[15], b->limbs[6]);
    carry_out += overflow;
    
    // Upper limb 6
    out_high.limbs[6] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[7], b->limbs[15]);
    carry_out = overflow;
    out_high.limbs[6] = __chestnut_mul_acc(&overflow, out_high.limbs[6], a->limbs[8], b->limbs[14]);
    carry_out += overflow;
    out_high.limbs[6] = __chestnut_mul_acc(&overflow, out_high.limbs[6], a->limbs[9], b->limbs[13]);
    carry_out += overflow;
    out_high.limbs[6] = __chestnut_mul_acc(&overflow, out_high.limbs[6], a->limbs[10], b->limbs[12]);
    carry_out += overflow;
    out_high.limbs[6] = __chestnut_mul_acc(&overflow, out_high.limbs[6], a->limbs[11], b->limbs[11]);
    carry_out += overflow;
    out_high.limbs[6] = __chestnut_mul_acc(&overflow, out_high.limbs[6], a->limbs[12], b->limbs[10]);
    carry_out += overflow;
    out_high.limbs[6] = __chestnut_mul_acc(&overflow, out_high.limbs[6], a->limbs[13], b->limbs[9]);
    carry_out += overflow;
    out_high.limbs[6] = __chestnut_mul_acc(&overflow, out_high.limbs[6], a->limbs[14], b->limbs[8]);
    carry_out += overflow;
    out_high.limbs[6] = __chestnut_mul_acc(&overflow, out_high.limbs[6], a->limbs[15], b->limbs[7]);
    carry_out += overflow;

    // Upper limb 7
    out_high.limbs[7] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[8], b->limbs[15]);
    carry_out = overflow;
    out_high.limbs[7] = __chestnut_mul_acc(&overflow, out_high.limbs[7], a->limbs[9], b->limbs[14]);
    carry_out += overflow;
    out_high.limbs[7] = __chestnut_mul_acc(&overflow, out_high.limbs[7], a->limbs[10], b->limbs[13]);
    carry_out += overflow;
    out_high.limbs[7] = __chestnut_mul_acc(&overflow, out_high.limbs[7], a->limbs[11], b->limbs[12]);
    carry_out += overflow;
    out_high.limbs[7] = __chestnut_mul_acc(&overflow, out_high.limbs[7], a->limbs[12], b->limbs[11]);
    carry_out += overflow;
    out_high.limbs[7] = __chestnut_mul_acc(&overflow, out_high.limbs[7], a->limbs[13], b->limbs[10]);
    carry_out += overflow;
    out_high.limbs[7] = __chestnut_mul_acc(&overflow, out_high.limbs[7], a->limbs[14], b->limbs[9]);
    carry_out += overflow;
    out_high.limbs[7] = __chestnut_mul_acc(&overflow, out_high.limbs[7], a->limbs[15], b->limbs[8]);
    carry_out += overflow;

    // Upper limb 8
    out_high.limbs[8] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[9], b->limbs[15]);
    carry_out = overflow;
    out_high.limbs[8] = __chestnut_mul_acc(&overflow, out_high.limbs[8], a->limbs[10], b->limbs[14]);
    carry_out += overflow;
    out_high.limbs[8] = __chestnut_mul_acc(&overflow, out_high.limbs[8], a->limbs[11], b->limbs[13]);
    carry_out += overflow;
    out_high.limbs[8] = __chestnut_mul_acc(&overflow, out_high.limbs[8], a->limbs[12], b->limbs[12]);
    carry_out += overflow;
    out_high.limbs[8] = __chestnut_mul_acc(&overflow, out_high.limbs[8], a->limbs[13], b->limbs[11]);
    carry_out += overflow;
    out_high.limbs[8] = __chestnut_mul_acc(&overflow, out_high.limbs[8], a->limbs[14], b->limbs[10]);
    carry_out += overflow;
    out_high.limbs[8] = __chestnut_mul_acc(&overflow, out_high.limbs[8], a->limbs[15], b->limbs[9]);
    carry_out += overflow;

    // Upper limb 9
    out_high.limbs[9] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[10], b->limbs[15]);
    carry_out = overflow;
    out_high.limbs[9] = __chestnut_mul_acc(&overflow, out_high.limbs[9], a->limbs[11], b->limbs[14]);
    carry_out += overflow;
    out_high.limbs[9] = __chestnut_mul_acc(&overflow, out_high.limbs[9], a->limbs[12], b->limbs[13]);
    carry_out += overflow;
    out_high.limbs[9] = __chestnut_mul_acc(&overflow, out_high.limbs[9], a->limbs[13], b->limbs[12]);
    carry_out += overflow;
    out_high.limbs[9] = __chestnut_mul_acc(&overflow, out_high.limbs[9], a->limbs[14], b->limbs[11]);
    carry_out += overflow;
    out_high.limbs[9] = __chestnut_mul_acc(&overflow, out_high.limbs[9], a->limbs[15], b->limbs[10]);
    carry_out += overflow;

    // Upper limb 10
    out_high.limbs[10] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[11], b->limbs[15]);
    carry_out = overflow;
    out_high.limbs[10] = __chestnut_mul_acc(&overflow, out_high.limbs[10], a->limbs[12], b->limbs[14]);
    carry_out += overflow;
    out_high.limbs[10] = __chestnut_mul_acc(&overflow, out_high.limbs[10], a->limbs[13], b->limbs[13]);
    carry_out += overflow;
    out_high.limbs[10] = __chestnut_mul_acc(&overflow, out_high.limbs[10], a->limbs[14], b->limbs[12]);
    carry_out += overflow;
    out_high.limbs[10] = __chestnut_mul_acc(&overflow, out_high.limbs[10], a->limbs[15], b->limbs[11]);
    carry_out += overflow;

    // Upper limb 11
    out_high.limbs[11] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[12], b->limbs[15]);
    carry_out = overflow;
    out_high.limbs[11] = __chestnut_mul_acc(&overflow, out_high.limbs[11], a->limbs[13], b->limbs[14]);
    carry_out += overflow;
    out_high.limbs[11] = __chestnut_mul_acc(&overflow, out_high.limbs[11], a->limbs[14], b->limbs[13]);
    carry_out += overflow;
    out_high.limbs[11] = __chestnut_mul_acc(&overflow, out_high.limbs[11], a->limbs[15], b->limbs[12]);
    carry_out += overflow;

    // Upper limb 12
    out_high.limbs[12] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[13], b->limbs[15]);
    carry_out = overflow;
    out_high.limbs[12] = __chestnut_mul_acc(&overflow, out_high.limbs[12], a->limbs[14], b->limbs[14]);
    carry_out += overflow;
    out_high.limbs[12] = __chestnut_mul_acc(&overflow, out_high.limbs[12], a->limbs[15], b->limbs[13]);
    carry_out += overflow;

    // Upper limb 13
    out_high.limbs[13] = __chestnut_mul_acc(&overflow, carry_out, a->limbs[14], b->limbs[15]);
    carry_out = overflow;
    out_high.limbs[13] = __chestnut_mul_acc(&overflow, out_high.limbs[13], a->limbs[15], b->limbs[14]);
    carry_out += overflow;

    // Upper limb 14 & 15
    out_high.limbs[14] = __chestnut_mul_acc(&out_high.limbs[15], carry_out, a->limbs[15], b->limbs[15]);

    return out_high;
}

static inline __attribute__((always_inline)) void __chestnut_uint128_t_select(
    chestnut_uint64_t mask,
    chestnut_uint128_t *out,
    const chestnut_uint128_t *if_true,
    const chestnut_uint128_t *if_false
) {
    out->limbs[0] = (if_true->limbs[0] & mask) | (if_false->limbs[0] & ~mask);
    out->limbs[1] = (if_true->limbs[1] & mask) | (if_false->limbs[1] & ~mask);
}

static inline __attribute__((always_inline)) void __chestnut_uint256_t_select(
    chestnut_uint64_t mask,
    chestnut_uint256_t *out,
    const chestnut_uint256_t *if_true,
    const chestnut_uint256_t *if_false
) {
    out->limbs[0] = (if_true->limbs[0] & mask) | (if_false->limbs[0] & ~mask);
    out->limbs[1] = (if_true->limbs[1] & mask) | (if_false->limbs[1] & ~mask);
    out->limbs[2] = (if_true->limbs[2] & mask) | (if_false->limbs[2] & ~mask);
    out->limbs[3] = (if_true->limbs[3] & mask) | (if_false->limbs[3] & ~mask);
}

static inline __attribute__((always_inline)) void __chestnut_uint512_t_select(
    chestnut_uint64_t mask,
    chestnut_uint512_t *out,
    const chestnut_uint512_t *if_true,
    const chestnut_uint512_t *if_false
) {
    out->limbs[0] = (if_true->limbs[0] & mask) | (if_false->limbs[0] & ~mask);
    out->limbs[1] = (if_true->limbs[1] & mask) | (if_false->limbs[1] & ~mask);
    out->limbs[2] = (if_true->limbs[2] & mask) | (if_false->limbs[2] & ~mask);
    out->limbs[3] = (if_true->limbs[3] & mask) | (if_false->limbs[3] & ~mask);
    out->limbs[4] = (if_true->limbs[4] & mask) | (if_false->limbs[4] & ~mask);
    out->limbs[5] = (if_true->limbs[5] & mask) | (if_false->limbs[5] & ~mask);
    out->limbs[6] = (if_true->limbs[6] & mask) | (if_false->limbs[6] & ~mask);
    out->limbs[7] = (if_true->limbs[7] & mask) | (if_false->limbs[7] & ~mask);
}

static inline __attribute__((always_inline)) void __chestnut_uint1024_t_select(
    chestnut_uint64_t mask,
    chestnut_uint1024_t *out,
    const chestnut_uint1024_t *if_true,
    const chestnut_uint1024_t *if_false
) {
    out->limbs[0] = (if_true->limbs[0] & mask) | (if_false->limbs[0] & ~mask);
    out->limbs[1] = (if_true->limbs[1] & mask) | (if_false->limbs[1] & ~mask);
    out->limbs[2] = (if_true->limbs[2] & mask) | (if_false->limbs[2] & ~mask);
    out->limbs[3] = (if_true->limbs[3] & mask) | (if_false->limbs[3] & ~mask);
    out->limbs[4] = (if_true->limbs[4] & mask) | (if_false->limbs[4] & ~mask);
    out->limbs[5] = (if_true->limbs[5] & mask) | (if_false->limbs[5] & ~mask);
    out->limbs[6] = (if_true->limbs[6] & mask) | (if_false->limbs[6] & ~mask);
    out->limbs[7] = (if_true->limbs[7] & mask) | (if_false->limbs[7] & ~mask);
    out->limbs[8] = (if_true->limbs[8] & mask) | (if_false->limbs[8] & ~mask);
    out->limbs[9] = (if_true->limbs[9] & mask) | (if_false->limbs[9] & ~mask);
    out->limbs[10] = (if_true->limbs[10] & mask) | (if_false->limbs[10] & ~mask);
    out->limbs[11] = (if_true->limbs[11] & mask) | (if_false->limbs[11] & ~mask);
    out->limbs[12] = (if_true->limbs[12] & mask) | (if_false->limbs[12] & ~mask);
    out->limbs[13] = (if_true->limbs[13] & mask) | (if_false->limbs[13] & ~mask);
    out->limbs[14] = (if_true->limbs[14] & mask) | (if_false->limbs[14] & ~mask);
    out->limbs[15] = (if_true->limbs[15] & mask) | (if_false->limbs[15] & ~mask);
}

void chestnut_int128_t_mul(
    chestnut_int128_t *out,
    const chestnut_int128_t *a,
    const chestnut_int128_t *b
) {
    // Get the mask for both a and b.
    chestnut_uint64_t mask_a = a->limbs[1] >> 63;
    chestnut_uint64_t mask_b = b->limbs[1] >> 63;

    // Get the negated versions of a and b.
    chestnut_uint128_t neg_a, neg_b;
    chestnut_uint128_t_negate(&neg_a, (chestnut_uint128_t*)a);
    chestnut_uint128_t_negate(&neg_b, (chestnut_uint128_t*)b);

    // Get the absolute values of a and b.
    chestnut_uint128_t abs_a, abs_b;
    __chestnut_uint128_t_select(mask_a, &abs_a, &neg_a, (chestnut_uint128_t*)a);
    __chestnut_uint128_t_select(mask_b, &abs_b, &neg_b, (chestnut_uint128_t*)b);

    // Do unsigned multiplication
    chestnut_uint128_t_mul((chestnut_uint128_t*)out, (chestnut_uint128_t*)&abs_a, (chestnut_uint128_t*)&abs_b);

    // Calculate the result mask
    chestnut_uint64_t result_mask = mask_a ^ mask_b;

    chestnut_uint128_t neg_out;
    chestnut_uint128_t_negate(&neg_out, (chestnut_uint128_t*)out);

    // Apply the result mask to output.
    __chestnut_uint128_t_select(result_mask, (chestnut_uint128_t*)out, &neg_out, (chestnut_uint128_t*)out);
}

void chestnut_int256_t_mul(
    chestnut_int256_t *out,
    const chestnut_int256_t *a,
    const chestnut_int256_t *b
) {
    chestnut_uint64_t mask_a = a->limbs[3] >> 63;
    chestnut_uint64_t mask_b = b->limbs[3] >> 63;

    chestnut_uint256_t neg_a, neg_b;
    chestnut_uint256_t_negate(&neg_a, (chestnut_uint256_t*)a);
    chestnut_uint256_t_negate(&neg_b, (chestnut_uint256_t*)b);

    chestnut_uint256_t abs_a, abs_b;
    __chestnut_uint256_t_select(mask_a, &abs_a, &neg_a, (chestnut_uint256_t*)a);
    __chestnut_uint256_t_select(mask_b, &abs_b, &neg_b, (chestnut_uint256_t*)b);

    chestnut_uint256_t_mul((chestnut_uint256_t*)out, (chestnut_uint256_t*)&abs_a, (chestnut_uint256_t*)&abs_b);

    chestnut_uint64_t result_mask = mask_a ^ mask_b;

    chestnut_uint256_t neg_out;
    chestnut_uint256_t_negate(&neg_out, (chestnut_uint256_t*)out);

    __chestnut_uint256_t_select(result_mask, (chestnut_uint256_t*)out, &neg_out, (chestnut_uint256_t*)out);
}

void chestnut_int512_t_mul(
    chestnut_int512_t *out,
    const chestnut_int512_t *a,
    const chestnut_int512_t *b
) {
    chestnut_uint64_t mask_a = a->limbs[7] >> 63;
    chestnut_uint64_t mask_b = b->limbs[7] >> 63;

    chestnut_uint512_t neg_a, neg_b;
    chestnut_uint512_t_negate(&neg_a, (chestnut_uint512_t*)a);
    chestnut_uint512_t_negate(&neg_b, (chestnut_uint512_t*)b);

    chestnut_uint512_t abs_a, abs_b;
    __chestnut_uint512_t_select(mask_a, &abs_a, &neg_a, (chestnut_uint512_t*)a);
    __chestnut_uint512_t_select(mask_b, &abs_b, &neg_b, (chestnut_uint512_t*)b);

    chestnut_uint512_t_mul((chestnut_uint512_t*)out, (chestnut_uint512_t*)&abs_a, (chestnut_uint512_t*)&abs_b);

    chestnut_uint64_t result_mask = mask_a ^ mask_b;

    chestnut_uint512_t neg_out;
    chestnut_uint512_t_negate(&neg_out, (chestnut_uint512_t*)out);

    __chestnut_uint512_t_select(result_mask, (chestnut_uint512_t*)out, &neg_out, (chestnut_uint512_t*)out);
}

void chestnut_int1024_t_mul(
    chestnut_int1024_t *out,
    const chestnut_int1024_t *a,
    const chestnut_int1024_t *b
) {
    chestnut_uint64_t mask_a = a->limbs[15] >> 63;
    chestnut_uint64_t mask_b = b->limbs[15] >> 63;

    chestnut_uint1024_t neg_a, neg_b;
    chestnut_uint1024_t_negate(&neg_a, (chestnut_uint1024_t*)a);
    chestnut_uint1024_t_negate(&neg_b, (chestnut_uint1024_t*)b);

    chestnut_uint1024_t abs_a, abs_b;
    __chestnut_uint1024_t_select(mask_a, &abs_a, &neg_a, (chestnut_uint1024_t*)a);
    __chestnut_uint1024_t_select(mask_b, &abs_b, &neg_b, (chestnut_uint1024_t*)b);

    chestnut_uint1024_t_mul((chestnut_uint1024_t*)out, (chestnut_uint1024_t*)&abs_a, (chestnut_uint1024_t*)&abs_b);

    chestnut_uint64_t result_mask = mask_a ^ mask_b;

    chestnut_uint1024_t neg_out;
    chestnut_uint1024_t_negate(&neg_out, (chestnut_uint1024_t*)out);

    __chestnut_uint1024_t_select(result_mask, (chestnut_uint1024_t*)out, &neg_out, (chestnut_uint1024_t*)out);
}

// A helper method to do shift right on uint64 arms
static inline __attribute__((always_inline)) void _chestnut_uint_shr(
    chestnut_uint64_t *out,
    const chestnut_uint64_t *in,
    chestnut_uint32_t n,
    chestnut_uint32_t s
) {
    // Restrict the range of s from 0 to n * 64 -1.
    s &= (n * 64) - 1;

    // How many 64 bit blocks can be skipped.
    chestnut_uint32_t limb_jump = s >> 6;

    // Remainder of the shift.
    chestnut_uint32_t bit_off = s & 63;

    // Complement to catch overflowing bits.
    chestnut_uint32_t bit_rev = 64 - bit_off;

    // Safety bitmask to prevent undefined behavior
    chestnut_uint64_t rev_mask = -(chestnut_uint64_t)(bit_off != 0);

    for (chestnut_uint32_t i = 0; i < n; i++) {
        // Calculate the memory offset
        chestnut_uint32_t src_i = i + limb_jump;
        chestnut_uint64_t res = 0;
        if (src_i < n) {
            res = in[src_i] >> bit_off;
            if (src_i + 1 < n) {
                res |= (in[src_i + 1] << bit_rev) & rev_mask;
            }
        }
        out[i] = res;
    }
}

chestnut_uint128_t chestnut_uint128_t_shr(
    chestnut_uint128_t a,
    chestnut_uint32_t s
) {
    chestnut_uint128_t out;
    _chestnut_uint_shr(out.limbs, a.limbs, 2, s);
    return out;
}

chestnut_uint256_t chestnut_uint256_t_shr(
    chestnut_uint256_t a,
    chestnut_uint32_t s
) {
    chestnut_uint256_t out;
    _chestnut_uint_shr(out.limbs, a.limbs, 4, s);
    return out;
}

chestnut_uint512_t chestnut_uint512_t_shr(
    chestnut_uint512_t a,
    chestnut_uint32_t s
) {
    chestnut_uint512_t out;
    _chestnut_uint_shr(out.limbs, a.limbs, 8, s);
    return out;
}

chestnut_uint1024_t chestnut_uint1024_t_shr(
    chestnut_uint1024_t a,
    chestnut_uint32_t s
) {
    chestnut_uint1024_t out;
    _chestnut_uint_shr(out.limbs, a.limbs, 16, s);
    return out;
}

static inline __attribute__((always_inline)) void _chestnut_uint_shl(
    chestnut_uint64_t *out,
    const chestnut_uint64_t *in,
    chestnut_uint32_t n,
    chestnut_uint32_t s
) {
    chestnut_uint32_t limb_jump = s >> 6;
    chestnut_uint32_t bit_off = s & 63;
    chestnut_uint32_t bit_rev = 64 - bit_off;
    chestnut_uint64_t rev_mask = -(chestnut_uint64_t)(bit_off != 0);

    for (chestnut_uint32_t i = 0; i < n; i++) {
        chestnut_uint64_t res = 0;
        if (i >= limb_jump) {
            chestnut_uint32_t src_i = i - limb_jump;
            res = in[src_i] << bit_off;
            if (src_i > 0) {
                res |= (in[src_i - 1] >> bit_rev) & rev_mask;
            }
        }
        out[i] = res;
    }
}

chestnut_uint128_t chestnut_uint128_t_shl(
    chestnut_uint128_t a,
    chestnut_uint32_t s
) {
    chestnut_uint128_t out;
    _chestnut_uint_shl(out.limbs, a.limbs, 2, s);
    return out;
}

chestnut_uint256_t chestnut_uint256_t_shl(
    chestnut_uint256_t a,
    chestnut_uint32_t s
) {
    chestnut_uint256_t out;
    _chestnut_uint_shl(out.limbs, a.limbs, 4, s);
    return out;
}

chestnut_uint512_t chestnut_uint512_t_shl(
    chestnut_uint512_t a,
    chestnut_uint32_t s
) {
    chestnut_uint512_t out;
    _chestnut_uint_shl(out.limbs, a.limbs, 8, s);
    return out;
}

chestnut_uint1024_t chestnut_uint1024_t_shl(
    chestnut_uint1024_t a,
    chestnut_uint32_t s
) {
    chestnut_uint1024_t out;
    _chestnut_uint_shl(out.limbs, a.limbs, 16, s);
    return out;
}

chestnut_uint8_t chestnut_uint8_t_add(const chestnut_uint8_t a, const chestnut_uint8_t b) {
    return a + b;
}

chestnut_uint16_t chestnut_uint16_t_add(
    const chestnut_uint16_t a,
    const chestnut_uint16_t b
) {
    return a + b;
}

chestnut_uint32_t chestnut_uint32_t_add(
    const chestnut_uint32_t a,
    const chestnut_uint32_t b
) {
    return a + b;
}

chestnut_uint64_t chestnut_uint64_t_add(
    const chestnut_uint64_t a,
    const chestnut_uint64_t b
) {
    return a + b;
}

static inline __attribute__((always_inline)) chestnut_uint16_t pop(uint64_t x) {
    // Count the bits in every 2-bit pair.
    x -= (x >> 1) & 0x5555555555555555ULL;

    // Sum the results of the 2 bit pairs into 4-bit nibbles.
    x = (x & 0x3333333333333333ULL) + ((x >> 2) & 0x3333333333333333ULL);

    // Sum the result of the 4-bit nibbles into 8-bit bytes.
    x = (x + (x >> 4)) & 0x0f0f0f0f0f0f0f0fULL;


    return (chestnut_uint16_t)((x * 0x0101010101010101ULL) >> 56);
}

static inline __attribute__((always_inline)) chestnut_uint64_t __chestnut_uint64_t_clz_shift(
    chestnut_uint64_t limb
) {
    limb |= limb >> 1;
    limb |= limb >> 2;
    limb |= limb >> 4;
    limb |= limb >> 8;
    limb |= limb >> 16;
    limb |= limb >> 32;
    return limb;
}

static inline __attribute__((always_inline)) chestnut_uint64_t __chestnut_uint64_t_ctz_shift(
    chestnut_uint64_t limb
) {
    limb |= limb << 1;
    limb |= limb << 2;
    limb |= limb << 4;
    limb |= limb << 8;
    limb |= limb << 16;
    limb |= limb << 32;
    return limb;
}

chestnut_uint16_t chestnut_uint128_t_clz(
    const chestnut_uint128_t *a
) {
    chestnut_uint16_t r1, r2, count, m;
    r1 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[0]));
    r2 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[1]));

    count = r1;
    m = -(r1 >> 6);

    count += (r2 & m);

    return count;
}

chestnut_uint16_t chestnut_uint256_t_clz(
    const chestnut_uint256_t *a
) {
    chestnut_uint16_t r1, r2, r3, r4, count, m;
    r1 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[0]));
    r2 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[1]));
    r3 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[2]));
    r4 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[3]));

    count = r1;
    m = -(r1 >> 6);

    count += (r2 & m);
    m &= -(r2 >> 6);

    count += (r3 & m);
    m &= -(r3 >> 6);

    count += (r4 & m);

    return count;
}

chestnut_uint16_t chestnut_uint512_t_clz(
    const chestnut_uint512_t *a
) {
    chestnut_uint16_t r1, r2, r3, r4, r5, r6, r7, r8, count, m;
    r1 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[0]));
    r2 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[1]));
    r3 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[2]));
    r4 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[3]));
    r5 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[4]));
    r6 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[5]));
    r7 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[6]));
    r8 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[7]));

    count = r1;
    m = -(r1 >> 6);

    count += (r2 & m);
    m &= -(r2 >> 6);

    count += (r3 & m);
    m &= -(r3 >> 6);
    
    count += (r4 & m);
    m &= -(r4 >> 6);
    
    count += (r5 & m);
    m &= -(r5 >> 6);
    
    count += (r6 & m);
    m &= -(r6 >> 6);
    
    count += (r7 & m);
    m &= -(r7 >> 6);

    count += (r8 & m);

    return count;
}

chestnut_uint16_t chestnut_uint1024_t_clz(
    const chestnut_uint1024_t *a
) {
    chestnut_uint16_t r1, r2, r3, r4, r5, r6, r7, r8,
                      r9, r10, r11, r12, r13, r14, r15,
                      r16, count, m;

    r1 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[0]));
    r2 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[1]));
    r3 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[2]));
    r4 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[3]));
    r5 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[4]));
    r6 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[5]));
    r7 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[6]));
    r8 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[7]));
    r9 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[8]));
    r10 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[9]));
    r11 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[10]));
    r12 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[11]));
    r13 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[12]));
    r14 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[13]));
    r15 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[14]));
    r16 = pop(~__chestnut_uint64_t_clz_shift(a->limbs[15]));

    count = r1;
    m = -(r1 >> 6);

    count += (r2 & m);
    m &= -(r2 >> 6);

    count += (r3 & m);
    m &= -(r3 >> 6);

    count += (r4 & m);
    m &= -(r4 >> 6);

    count += (r5 & m);
    m &= -(r5 >> 6);

    count += (r6 & m);
    m &= -(r6 >> 6);

    count += (r7 & m);
    m &= -(r7 >> 6);

    count += (r8 & m);
    m &= -(r8 >> 6);

    count += (r9 & m);
    m &= -(r9 >> 6);

    count += (r10 & m);
    m &= -(r10 >> 6);

    count += (r11 & m);
    m &= -(r11 >> 6);

    count += (r12 & m);
    m &= -(r12 >> 6);

    count += (r13 & m);
    m &= -(r13 >> 6);

    count += (r14 & m);
    m &= -(r14 >> 6);

    count += (r15 & m);
    m &= -(r15 >> 6);

    count += (r16 & m);

    return count;
}

chestnut_uint16_t chestnut_uint128_t_ctz(
    const chestnut_uint128_t *a
) {
    chestnut_uint16_t r1, r2, count, m;
    r2 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[1]));
    r1 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[0]));

    count = r2;
    m = -(r2 >> 6);

    count += (r1 & m);

    return count;
}

chestnut_uint16_t chestnut_uint256_t_ctz(
    const chestnut_uint256_t *a
) {
    chestnut_uint16_t r1, r2, r3, r4, count, m;
    r4 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[3]));
    r3 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[2]));
    r2 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[1]));
    r1 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[0]));

    count = r4;
    m = -(r4 >> 6);

    count += (r3 & m);
    m &= -(r3 >> 6);

    count += (r2 & m);
    m &= -(r2 >> 6);

    count += (r1 & m);

    return count;
}

chestnut_uint16_t chestnut_uint512_t_ctz(
    const chestnut_uint512_t *a
) {
    chestnut_uint16_t r1, r2, r3, r4, r5, r6, r7, r8, count, m;
    r8 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[7]));
    r7 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[6]));
    r6 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[5]));
    r5 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[4]));
    r4 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[3]));
    r3 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[2]));
    r2 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[1]));
    r1 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[0]));

    count = r8;
    m = -(r8 >> 6);

    count += (r7 & m);
    m &= -(r7 >> 6);
    
    count += (r6 & m);
    m &= -(r6 >> 6);
    
    count += (r5 & m);
    m &= -(r5 >> 6);
    
    count += (r4 & m);
    m &= -(r4 >> 6);
    
    count += (r3 & m);
    m &= -(r3 >> 6);

    count += (r2 & m);
    m &= -(r2 >> 6);

    count += (r1 & m);

    return count;
}

chestnut_uint16_t chestnut_uint1024_t_ctz(
    const chestnut_uint1024_t *a
) {
    chestnut_uint16_t r0, r1, r2, r3, r4, r5, r6, r7,
                      r8, r9, r10, r11, r12, r13, r14,
                      r15, count, m;
    r0 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[0]));
    r1 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[1]));
    r2 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[2]));
    r3 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[3]));
    r4 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[4]));
    r5 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[5]));
    r6 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[6]));
    r7 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[7]));
    r8 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[8]));
    r9 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[9]));
    r10 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[10]));
    r11 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[11]));
    r12 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[12]));
    r13 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[13]));
    r14 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[14]));
    r15 = pop(~__chestnut_uint64_t_ctz_shift(a->limbs[15]));

    count = r0;
    m = -(r0 >> 6);

    count += (r1 & m);
    m &= -(r1 >> 6);

    count += (r2 & m);
    m &= -(r2 >> 6);

    count += (r3 & m);
    m &= -(r3 >> 6);

    count += (r4 & m);
    m &= -(r4 >> 6);

    count += (r5 & m);
    m &= -(r5 >> 6);

    count += (r6 & m);
    m &= -(r6 >> 6);

    count += (r7 & m);
    m &= -(r7 >> 6);

    count += (r8 & m);
    m &= -(r8 >> 6);

    count += (r9 & m);
    m &= -(r9 >> 6);
    
    count += (r10 & m);
    m &= -(r10 >> 6);
    
    count += (r11 & m);
    m &= -(r11 >> 6);
    
    count += (r12 & m);
    m &= -(r12 >> 6);
    
    count += (r13 & m);
    m &= -(r13 >> 6);

    count += (r14 & m);
    m &= -(r14 >> 6);

    count += (r15 & m);

    return count;
}
#endif
