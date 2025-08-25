// Code modifié basé sur Jon Erickson, pages 147-148, Hacking: The Art of Exploitation, 2nd Edition

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

int main(int argc, char *argv[]) {
    char *ptr;

    if(argc < 3) {
        printf("Usage: %s <environment variable> <target program name>\n", argv[0]);
        exit(0);
    }

    ptr = getenv(argv[1]);
    if(!ptr) {
        printf("Environment variable %s not found.\n", argv[1]);
        exit(1);
    }

    ptr += (strlen(argv[0]) - strlen(argv[2])) * 2;

    uintptr_t addr = (uintptr_t)ptr;
    printf("%s will be at %p\n", argv[1], (void*)addr);
    printf("Canonical 64-bit form: 0x%016lx\n", addr);
    printf("Little endian form : ");
    unsigned char *p = (unsigned char *)&addr;
    for (size_t i = 0; i < sizeof(addr); i++) {
        printf("\\x%02x", p[i]);
    }
    printf("\n");

    return 0;
}
