#ifndef __MEMDEBUG_H__
#define __MEMDEBUG_H__

#include <stdio.h>
#include <stdlib.h>
void *
mymtom_malloc(size_t size);
 
//#define malloc(s) mymtom_malloc(s)
#define free(p)  do {                                                   \
                printf("%s:%d:%s:free(0x%lx)\n", __FILE__, __LINE__,    \
                    __func__, (unsigned long)p);                        \
                free(p);                                                \
        } while (0)
#endif