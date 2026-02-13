from cffi import FFI
import os

ffibuilder = FFI()

# 1. Define ONLY what we are testing right now
ffibuilder.cdef("""
    typedef uint8_t chestnut_uint8_t;
    typedef uint16_t chestnut_uint16_t;
    typedef uint32_t chestnut_uint32_t;
    typedef uint64_t chestnut_uint64_t;

    typedef struct {
        chestnut_uint64_t limbs[2];
    } chestnut_uint128_t;

    typedef struct {
        chestnut_uint64_t limbs[4];
    } chestnut_uint256_t;

    typedef struct {
        chestnut_uint64_t limbs[8];
    } chestnut_uint512_t;

    typedef struct {
        chestnut_uint64_t limbs[16];
    } chestnut_uint1024_t;

    chestnut_uint8_t chestnut_uint128_t_add(chestnut_uint128_t *c, const chestnut_uint128_t *a, const chestnut_uint128_t *b);
    chestnut_uint8_t chestnut_uint128_t_sub(chestnut_uint128_t *c, const chestnut_uint128_t *a, const chestnut_uint128_t *b);
    chestnut_uint8_t chestnut_uint128_t_mul(chestnut_uint128_t *c, const chestnut_uint128_t *a, const chestnut_uint128_t *b);

    chestnut_uint8_t chestnut_uint256_t_add(chestnut_uint256_t *c, const chestnut_uint256_t *a, const chestnut_uint256_t *b);
    chestnut_uint8_t chestnut_uint256_t_sub(chestnut_uint256_t *c, const chestnut_uint256_t *a, const chestnut_uint256_t *b);
    chestnut_uint8_t chestnut_uint256_t_mul(chestnut_uint256_t *c, const chestnut_uint256_t *a, const chestnut_uint256_t *b);

    chestnut_uint8_t chestnut_uint512_t_add(chestnut_uint512_t *c, const chestnut_uint512_t *a, const chestnut_uint512_t *b);
    chestnut_uint8_t chestnut_uint512_t_sub(chestnut_uint512_t *c, const chestnut_uint512_t *a, const chestnut_uint512_t *b);
    chestnut_uint8_t chestnut_uint512_t_mul(chestnut_uint512_t *c, const chestnut_uint512_t *a, const chestnut_uint512_t *b);

    chestnut_uint8_t chestnut_uint1024_t_add(chestnut_uint1024_t *c, const chestnut_uint1024_t *a, const chestnut_uint1024_t *b);
    chestnut_uint8_t chestnut_uint1024_t_sub(chestnut_uint1024_t *c, const chestnut_uint1024_t *a, const chestnut_uint1024_t *b);
    chestnut_uint8_t chestnut_uint1024_t_mul(chestnut_uint1024_t *c, const chestnut_uint1024_t *a, const chestnut_uint1024_t *b);
""")

ffibuilder.set_source("chestnut_c_binding", 
    """
    #include <stdint.h>
    #include <stddef.h>
    
    typedef uint8_t chestnut_uint8_t;
    typedef uint16_t chestnut_uint16_t;
    typedef uint32_t chestnut_uint32_t;
    typedef uint64_t chestnut_uint64_t;

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

    chestnut_uint8_t chestnut_uint128_t_add(chestnut_uint128_t *c, const chestnut_uint128_t *a, const chestnut_uint128_t *b);
    chestnut_uint8_t chestnut_uint128_t_sub(chestnut_uint128_t *c, const chestnut_uint128_t *a, const chestnut_uint128_t *b);
    chestnut_uint8_t chestnut_uint128_t_mul(chestnut_uint128_t *c, const chestnut_uint128_t *a, const chestnut_uint128_t *b);

    chestnut_uint8_t chestnut_uint256_t_add(chestnut_uint256_t *c, const chestnut_uint256_t *a, const chestnut_uint256_t *b);
    chestnut_uint8_t chestnut_uint256_t_sub(chestnut_uint256_t *c, const chestnut_uint256_t *a, const chestnut_uint256_t *b);
    chestnut_uint8_t chestnut_uint256_t_mul(chestnut_uint256_t *c, const chestnut_uint256_t *a, const chestnut_uint256_t *b);

    chestnut_uint8_t chestnut_uint512_t_add(chestnut_uint512_t *c, const chestnut_uint512_t *a, const chestnut_uint512_t *b);
    chestnut_uint8_t chestnut_uint512_t_sub(chestnut_uint512_t *c, const chestnut_uint512_t *a, const chestnut_uint512_t *b);
    chestnut_uint8_t chestnut_uint512_t_mul(chestnut_uint512_t *c, const chestnut_uint512_t *a, const chestnut_uint512_t *b);

    chestnut_uint8_t chestnut_uint1024_t_add(chestnut_uint1024_t *c, const chestnut_uint1024_t *a, const chestnut_uint1024_t *b);
    chestnut_uint8_t chestnut_uint1024_t_sub(chestnut_uint1024_t *c, const chestnut_uint1024_t *a, const chestnut_uint1024_t *b);
    chestnut_uint8_t chestnut_uint1024_t_mul(chestnut_uint1024_t *c, const chestnut_uint1024_t *a, const chestnut_uint1024_t *b);
    """,
    extra_objects=[os.path.abspath("/home/lumpywizard/Projects/Python/chestnut/c/lib/int.o")]
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
    print("\n✨ The tiny bridge is built! ✨")
