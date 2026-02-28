#ifndef CHESTNUT_LIB_FLOAT_H
#define CHESTNUT_LIB_FLOAT_H

#include <stdint.h>
#include <stddef.h>
#include <stdalign.h>
#if !defined(chestnut_uint64_t)
    typedef uint8_t chestnut_uint8_t;
    typedef uint16_t chestnut_uint16_t;
    typedef uint64_t chestnut_uint64_t;
#endif
typedef chestnut_uint8_t chestnut_float8_5e2m_t;
typedef chestnut_uint8_t chestnut_float8_4e3m_t;
typedef chestnut_float8_4e3m_t chestnut_float8_t;
typedef chestnut_uint8_t chestnut_float8_3e4m_t;
typedef chestnut_uint8_t chestnut_float8_2e5m_t;

typedef chestnut_uint16_t chestnut_float16_5e10m_t;
typedef chestnut_float16_5e10m_t chestnut_float16_t;
typedef chestnut_uint16_t chestnut_float16_8e7m_t;
typedef chestnut_float16_8e7m_t chestnut_bfloat16_t;


#if defined(__STDC_VERSION__) && __STDC_VERSION__ >= 202311L
    typedef _Float32 chestnut_float32_t;
    typedef _Float64 chestnut_float64_t;
#else
    typedef float chestnut_float32_t;
    typedef double chestnut_float64_t;
#endif

typedef struct {
    chestnut_uint64_t limbs[2] __attribute__((aligned(16)));
} chestnut_float128_t;
typedef struct {
    chestnut_uint64_t limbs[4] __attribute__((aligned(16)));
} chestnut_float256_t;
typedef struct {
    chestnut_uint64_t limbs[8] __attribute__((aligned(16)));
} chestnut_float512_t;
typedef struct {
    chestnut_uint64_t limbs[16]__attribute__((aligned(16)));
} chestnut_float1024_t;

#endif
