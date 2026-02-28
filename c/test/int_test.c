#include "../lib/int.c"

void do_test_uint128(int argc) {
    chestnut_uint128_t a, b, res;
    chestnut_uint128_t_clear(&a);
    chestnut_uint128_t_clear(&b);
    chestnut_uint128_t_clear(&res);

    for(int i = 0; i < 2; i++) {
        a.limbs[i] = 0xAAAAAAAAAAAAAAAAULL + argc;
        b.limbs[i] = 0xDEADBEEFULL + i;
    }

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for(int i = 0; i < 1000000; i++) {
        chestnut_uint128_t_mul(&res, &a, &b);
        a.limbs[0] += a.limbs[0];
        __asm__ __volatile__("" : "+g"(a.limbs[0]), "+g"(res.limbs[0]) : : "memory");
    }

    clock_gettime(CLOCK_MONOTONIC, &end);

    double time_spent = (end.tv_sec - start.tv_sec) + 
                       (end.tv_nsec - start.tv_nsec) / 1000000000.0;
    printf("Total time for 1M 128 bit truncated product multiplications: %f seconds\n", time_spent);
    printf("Checksum %u\n\n", res.limbs[0] ^ res.limbs[1]);
}

void do_test_uint128_full(int argc) {
    chestnut_uint128_t a, b, res;
    chestnut_uint128_t_clear(&a);
    chestnut_uint128_t_clear(&b);
    chestnut_uint128_t_clear(&res);

    for(int i = 0; i < 2; i++) {
        a.limbs[i] = 0xAAAAAAAAAAAAAAAAULL + argc;
        b.limbs[i] = 0xDEADBEEFULL + i;
    }

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for(int i = 0; i < 1000000; i++) {
        chestnut_uint128_t_mul_full(&res, &a, &b);
        a.limbs[0] += a.limbs[0];
        __asm__ __volatile__("" : "+g"(a.limbs[0]), "+g"(res.limbs[0]) : : "memory");
    }

    clock_gettime(CLOCK_MONOTONIC, &end);

    double time_spent = (end.tv_sec - start.tv_sec) + 
                       (end.tv_nsec - start.tv_nsec) / 1000000000.0;
    printf("Total time for 1M 128 bit full product multiplications: %f seconds\n", time_spent);
    printf("Checksum %u\n\n", res.limbs[0] ^ res.limbs[1]);
}

void do_test_uint256(int argc) {
    chestnut_uint256_t a, b, res;
    chestnut_uint256_t_clear(&a);
    chestnut_uint256_t_clear(&b);
    chestnut_uint256_t_clear(&res);

    for(int i = 0; i < 4; i++) {
        a.limbs[i] = 0xAAAAAAAAAAAAAAAAULL + argc;
        b.limbs[i] = 0xDEADBEEFULL + i;
    }

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for(int i = 0; i < 1000000; i++) {
        chestnut_uint256_t_mul(&res, &a, &b);
        a.limbs[0] += a.limbs[0];
        __asm__ __volatile__("" : "+g"(a.limbs[0]), "+g"(res.limbs[0]) : : "memory");
    }

    clock_gettime(CLOCK_MONOTONIC, &end);

    double time_spent = (end.tv_sec - start.tv_sec) + 
                       (end.tv_nsec - start.tv_nsec) / 1000000000.0;
    printf("Total time for 1M 256 bit truncated product multiplications: %f seconds\n", time_spent);
    printf("Checksum: %u\n\n", res.limbs[0] ^ res.limbs[1] ^ res.limbs[2] ^ res.limbs[3]);
}

void do_test_uint256_full(int argc) {
    chestnut_uint256_t a, b, res;
    chestnut_uint256_t_clear(&a);
    chestnut_uint256_t_clear(&b);
    chestnut_uint256_t_clear(&res);

    for(int i = 0; i < 4; i++) {
        a.limbs[i] = 0xAAAAAAAAAAAAAAAAULL + argc;
        b.limbs[i] = 0xDEADBEEFULL + i;
    }

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for(int i = 0; i < 1000000; i++) {
        chestnut_uint256_t_mul_full(&res, &a, &b);
        a.limbs[0] += a.limbs[0];
        __asm__ __volatile__("" : "+g"(a.limbs[0]), "+g"(res.limbs[0]) : : "memory");
    }

    clock_gettime(CLOCK_MONOTONIC, &end);

    double time_spent = (end.tv_sec - start.tv_sec) + 
                       (end.tv_nsec - start.tv_nsec) / 1000000000.0;
    printf("Total time for 1M 256 bit full product multiplications: %f seconds\n", time_spent);
    printf("Checksum: %u\n\n", res.limbs[0] ^ res.limbs[1] ^ res.limbs[2] ^ res.limbs[3]);
}

void do_test_uint512(int argc) {
    chestnut_uint512_t a, b, res;
    chestnut_uint512_t_clear(&a);
    chestnut_uint512_t_clear(&b);
    chestnut_uint512_t_clear(&res);

    for(int i = 0; i < 8; i++) {
        a.limbs[i] = 0xAAAAAAAAAAAAAAAAULL + argc;
        b.limbs[i] = 0xDEADBEEFULL + i;
    }

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for(int i = 0; i < 1000000; i++) {
        chestnut_uint512_t_mul(&res, &a, &b);
        a.limbs[0] += a.limbs[0];
        __asm__ __volatile__("" : "+g"(a.limbs[0]), "+g"(res.limbs[0]) : : "memory");
    }

    clock_gettime(CLOCK_MONOTONIC, &end);

    double time_spent = (end.tv_sec - start.tv_sec) + 
                       (end.tv_nsec - start.tv_nsec) / 1000000000.0;
    printf("Total time for 1M 512 bit truncated product multiplications: %f seconds\n", time_spent);
    printf("Checksum: %u\n\n", res.limbs[0] ^ res.limbs[1] ^ res.limbs[2] ^ res.limbs[3] ^ res.limbs[4] ^ res.limbs[5] ^ res.limbs[6] ^ res.limbs[7]);
}

void do_test_uint512_full(int argc) {
    chestnut_uint512_t a, b, res;
    chestnut_uint512_t_clear(&a);
    chestnut_uint512_t_clear(&b);
    chestnut_uint512_t_clear(&res);

    for(int i = 0; i < 8; i++) {
        a.limbs[i] = 0xAAAAAAAAAAAAAAAAULL + argc;
        b.limbs[i] = 0xDEADBEEFULL + i;
    }

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for(int i = 0; i < 1000000; i++) {
        chestnut_uint512_t_mul_full(&res, &a, &b);
        a.limbs[0] += a.limbs[0];
        __asm__ __volatile__("" : "+g"(a.limbs[0]), "+g"(res.limbs[0]) : : "memory");
    }

    clock_gettime(CLOCK_MONOTONIC, &end);

    double time_spent = (end.tv_sec - start.tv_sec) + 
                       (end.tv_nsec - start.tv_nsec) / 1000000000.0;
    printf("Total time for 1M 512 bit full product multiplications: %f seconds\n", time_spent);
    printf("Checksum: %u\n\n", res.limbs[0] ^ res.limbs[1] ^ res.limbs[2] ^ res.limbs[3] ^ res.limbs[4] ^ res.limbs[5] ^ res.limbs[6] ^ res.limbs[7]);
}

void do_test_uint1024(int argc) {
    chestnut_uint1024_t a, b, res;
    chestnut_uint1024_t_clear(&a);
    chestnut_uint1024_t_clear(&b);
    chestnut_uint1024_t_clear(&res);

    for(int i = 0; i < 16; i++) {
        a.limbs[i] = 0xAAAAAAAAAAAAAAAAULL + argc;
        b.limbs[i] = 0xDEADBEEFULL + i;
    }

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for(int i = 0; i < 1000000; i++) {
        chestnut_uint1024_t_mul(&res, &a, &b);
        a.limbs[0] += a.limbs[0];
        __asm__ __volatile__("" : "+g"(a.limbs[0]), "+g"(res.limbs[0]) : : "memory");
    }

    clock_gettime(CLOCK_MONOTONIC, &end);

    double time_spent = (end.tv_sec - start.tv_sec) + 
                       (end.tv_nsec - start.tv_nsec) / 1000000000.0;
    printf("Total time for 1M 1024 bit truncate product multiplications: %f seconds\n", time_spent);
    printf("Checksum: %u\n\n", res.limbs[0] ^ res.limbs[1] ^ res.limbs[2] ^ res.limbs[3] ^ res.limbs[4] ^ res.limbs[5] ^ res.limbs[6] ^ res.limbs[7] ^ res.limbs[8] ^ res.limbs[9] ^ res.limbs[10] ^ res.limbs[11] ^ res.limbs[12] ^ res.limbs[13] ^ res.limbs[14] ^ res.limbs[15]);
}

void do_test_uint1024_full(int argc) {
    chestnut_uint1024_t a, b, res;
    chestnut_uint1024_t_clear(&a);
    chestnut_uint1024_t_clear(&b);
    chestnut_uint1024_t_clear(&res);

    for(int i = 0; i < 16; i++) {
        a.limbs[i] = 0xAAAAAAAAAAAAAAAAULL + argc;
        b.limbs[i] = 0xDEADBEEFULL + i;
    }

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for(int i = 0; i < 1000000; i++) {
        chestnut_uint1024_t_mul_full(&res, &a, &b);
        a.limbs[0] += a.limbs[0];
        __asm__ __volatile__("" : "+g"(a.limbs[0]), "+g"(res.limbs[0]) : : "memory");
    }

    clock_gettime(CLOCK_MONOTONIC, &end);

    double time_spent = (end.tv_sec - start.tv_sec) + 
                       (end.tv_nsec - start.tv_nsec) / 1000000000.0;
    printf("Total time for 1M 1024 bit full product multiplications: %f seconds\n", time_spent);
    printf("Checksum: %u\n\n", res.limbs[0] ^ res.limbs[1] ^ res.limbs[2] ^ res.limbs[3] ^ res.limbs[4] ^ res.limbs[5] ^ res.limbs[6] ^ res.limbs[7] ^ res.limbs[8] ^ res.limbs[9] ^ res.limbs[10] ^ res.limbs[11] ^ res.limbs[12] ^ res.limbs[13] ^ res.limbs[14] ^ res.limbs[15]);
}

void do_test_ctz1024() {
    chestnut_uint1024_t a;
    chestnut_uint1024_t_clear(&a);
    chestnut_uint16_t b = chestnut_uint1024_t_ctz(&a);
    printf("1024 CTZ: %d\n", b);
}

void do_test_clz1024() {
    chestnut_uint1024_t a;
    chestnut_uint1024_t_clear(&a);
    chestnut_uint16_t b = chestnut_uint1024_t_clz(&a);
    printf("1024 CLZ: %d\n", b);
}

int main() {
    do_test_uint128(15);
    do_test_uint128_full(16);
    do_test_uint256(26);
    do_test_uint256_full(27);
    do_test_uint512(1);
    do_test_uint512_full(2);
    do_test_uint1024(11);
    do_test_uint1024_full(12);
    // do_test_ctz1024();
    // do_test_clz1024();
    return 0;
}
