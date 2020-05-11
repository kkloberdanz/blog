#include <stdio.h>
#include <stdbool.h>
#include <math.h>

bool is_prime(unsigned long n) {
    if (n < 2) {
        return false;
    } else {
        unsigned long max = sqrt(n) + 1;
        unsigned long i;
        for (i = 2; i < max; i++) {
            if (n % i == 0) {
                return false;
            }
        }
        return true;
    }
}

int main(void) {
    unsigned long start = 9223372036854775808UL;
    unsigned long end = start + 1000;
    unsigned long i;

    #pragma omp parallel for schedule(dynamic)
    for (i = start; i < end; i++) {
        if (is_prime(i)) {
            #pragma omp critical
            {
                printf("%lu is prime\n", i);
            }
        }
    }
    return 0;
}
