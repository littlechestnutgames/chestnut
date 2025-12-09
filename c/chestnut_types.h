#ifndef CHESTNUT_TYPES

#define CHESTNUT_TYPES
#include <stdint.h>

#ifdef __SIZEOF_INT128__
    // If our compiler has int128s, use them instead.
    #define NUM_LIMBS_256 (256 / 128)
    #define NUM_LIMBS_512 (512 / 128)
    #define NUM_LIMBS_1024 (1024 / 128)

`    typedef __int128 chestnut_int128;
    typedef __uint128 chestnut_uint128;

    #define INT_LIMB_TYPE chestnut_int128
    #define UINT_LIMB_TYPE chestnut_uint128
#else
    // Our compiler didn't have int128s. Use int64 instead.
    #define NUM_LIMBS_128 (128 / 64)
    #define NUM_LIMBS_256 (256 / 64)
    #define NUM_LIMBS_512 (512 / 64)
    #define NUM_LIMBS_1024 (1024 / 64)

    #define INT_LIMB_TYPE int64_t
    #define UINT_LIMB_TYPE uint64_t

    typedef struct {
        int sign;
        INT_LIMB_TYPE limbs[NUM_LIMBS_128];
    } chestnut_int128;

    typedef struct {
        UINT_LIMB_TYPE limbs[NUM_LIMBS_128];
    } chestnut_uint128;
#endif

typedef struct {
    int sign;
    INT_LIMB_TYPE limbs[NUM_LIMBS_256];
} chestnut_int256;

typedef struct {
    int sign;
    INT_LIMB_TYPE limbs[NUM_LIMBS_512];
} chestnut_int512;

typedef struct {
    int sign;
    INT_LIMB_TYPE limbs[NUM_LIMBS_1024];
} chestnut_int1024;

typedef struct {
    UINT_LIMB_TYPE limbs[NUM_LIMBS_256];
} chestnut_uint256;

typedef struct {
    UINT_LIMB_TYPE limbs[NUM_LIMBS_512];
} chestnut_uint512;

typedef struct {
    UINT_LIMB_TYPE limbs[NUM_LIMBS_1024];
} chestnut_uint1024;

UINT_LIMB_TYPE add_with_carry(
    UINT_LIMB_TYPE a,
    UINT_LIMB_TYPE b,
    UINT_LIMB_TYPE* carry
) {
    UINT_LIMB_TYPE carry_in = *carry;
    UINT_LIMB_TYPE tmp_sum = a + b;
    UINT_LIMB_TYPE initial_carry_out = (temp_sum < a);
    UINT_LIMB_TYPE
    *carry = (result < a);
    return result;
}

int limb_add(
    UINT_LIMB_TYPE* dest,
    const UINT_LIMB_TYPE* a,
    const UINT_LIMB_TYPE* b,
    size_t limb_count
) {
    UINT_LIMB_TYPE carry = 0;
    for (size_t i = 0; i < limb_count; i++) {
        dest[i] = add_with_carry(a[i], b[i], &carry);
    }

    return carry;
}
#endif
