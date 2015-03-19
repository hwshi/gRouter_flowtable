#include "memdebug.h"
void *
mymtom_malloc(size_t size)
{
        void *p;
        p = malloc(size);
        printf("malloc() size=0x%lu, p=0x%lx\n", (unsigned long)size, (unsigned long)p);
        return p;
}