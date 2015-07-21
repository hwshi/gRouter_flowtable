#include <stdlib.h>
#include <stdio.h>
#include <string.h>
typedef struct _module_config_t
{
    char name[20];
    ushort protocol;
    void *processor;
    void *command;
    char command_str[20];    
} module_config_t;

module_config_t *udpConfig();

int udp2Process();

void udp2Command();
void printConfigInfo(module_config_t *config);
