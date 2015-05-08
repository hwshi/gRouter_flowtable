#include "udp2.h"

module_config_t *udp2Config()
{
    printf("creating config..\n");
    module_config_t *config = (module_config_t*)malloc(sizeof(module_config_t));
    
    strcpy(config->name, "udp2");
    config->protocol = 17;
    config->processor = &udp2Process;
    config->command = &udp2Command;
    strcpy(config->command_str, "udp2");
    printConfigInfo(config);
    return config;
}
void printConfigInfo(module_config_t *config)
{
    printf("----    Config Information [so]  ----\n");
    printf("module name :       %s\n", config->name);
    printf("protocol    :       %#06x\n", config->protocol);
    printf("processor   :       %p\n", config->processor);
    printf("command     :       %p\n", config->command);
    printf("----       End of Config    ----\n");
}
void udp2Process()
{
    printf("[udp2Process] start!\n");
    
}

void udp2Command()
{
    printf("[udp2Command] start!\n");
}
