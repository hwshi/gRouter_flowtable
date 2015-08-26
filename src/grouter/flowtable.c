/*
 * flowtable.c (the flowtable for packet core)
 * AUTHOR: Haowei Shi
 * DATE: October 01, 2014
 *
 */

//Haowei
//#include "flowtable_wrap.c"
#include "ginic_wrap.c"
#include "flowtable.h"
#include "Python.h"
//#include "utils.h"
//

void *judgeProcessor(void *pc)
{
    pktcore_t *pcore = (pktcore_t *) pc;
    gpacket_t *in_pkt;
    //flowtable
    SWIG_init(); // Haowei: should be init here or in packetcore.c???
    int pktsize;
    pthread_setcanceltype(PTHREAD_CANCEL_ASYNCHRONOUS, NULL);
    while (1)
    {

        verbose(2, "[judgeProcessor]:: Waiting for a packet...");
        //TODO: Redefine data format in Queue from pkt to frame
        readQueue(pcore->decisionQ, (void **) &in_pkt, &pktsize);
        pthread_testcancel();
        verbose(2, "[judgeProcessor]:: Got a packet for further processing...");
        ftentry_t *entry_res = NULL;
        ushort prot;
        //        printf("[judgeProcessor]:: flowtable size: %d\n", pcore->flowtable->num);
        /*
         * check flow table:    1. classical router
         *                      2. openflow switch
         */

        /*
         * 1. classical router
         */
        /////////// 
        //        entry_res = checkFlowTable(pcore->flowtable, in_pkt);
        //        if (entry_res == NULL)
        //            //if (!checkFlowTable(pcore->flowtable, in_pkt, action_c, &prot))
        //        {
        //            printf("[judgeProcessor]:: Cannot find action to given packet...Drop!\n");
        //            return;
        //        }
        //        //TODO: call function using action(char *):  PyObject_CallFunction(String)
        //        verbose(2, "[judgeProcessor]:: Entry found protocol: %#06x\n", entry_res->ip_protocol_type);
        //        if (entry_res->language == C_FUNCTION)
        //        {
        //
        //            verbose(2, "[judgeProcessor]:: C Function: Action: (0x%lx)\n", (unsigned long) entry_res->action_c);
        //            int (*processor)(gpacket_t *);
        //            processor = entry_res->action_c;
        //            int nextlabel = (*processor)(in_pkt);
        //            if (entry_res->ip_protocol_type == ARP_PROTOCOL || nextlabel == EXIT_SUCCESS)
        //            {
        //                verbose(2, "[judgeProcessor] SUCCESS!  : %d\n", EXIT_SUCCESS);
        //                continue;
        //            }
        //            if (nextlabel == UDP_PROTOCOL) verbose(2, "UDP!!!!!!!!");
        //            verbose(2, "[judgeProcessor][Ft]New style round");
        //            labelNext(in_pkt, entry_res->ip_protocol_type, nextlabel);
        //            verbose(2, "[judgeProcessor]Writing back to decision Q...");
        //            writeQueue(pcore->decisionQ, in_pkt, sizeof (gpacket_t));
        //            verbose(2, "[judgeProcessor]Wrote back to decision Q...");
        //            //            printSimpleQueue(pcore->decisionQ);
        //
        //        }
        //        else if (entry_res->language == PYTHON_FUNCTION)
        //        {
        //            verbose(2, "[judgeProcessor]:: Python Function: Action: (0x%lx)\n", (unsigned long) entry_res->action_c);
        //            //TODO: Python embedding
        //            //TODO: ?? Where to declaire!?
        //            PyObject * Py_pFun, *Py_pPkt, *Py_pResult;
        //            Py_pFun = entry_res->action_c;
        //            Py_pPkt = SWIG_NewPointerObj((void *) in_pkt, SWIGTYPE_p__gpacket_t, 1);
        //            //Py_pResult = PyObject_CallFunction(Py_pFun, NULL);
        //            if (Py_pPkt)
        //            {
        //                verbose(2, "Got Pyton obj\n");
        //                Py_pResult = PyObject_CallFunction(Py_pFun, "O", Py_pPkt);
        //                CheckPythonError();
        //              /* TODO: check whether further process is needed. */
        //                //                printf("pResult: %p", Py_pResult);
        //            }
        //        }
        ///////////
        /*
         * 2. openflow switch
         * tmp: let flowtable[3] have openflow.py (hardcoded)         
         */
        entry_res = checkOFFlowTable(pcore->flowtable, in_pkt);
        if (entry_res == NULL) // No action in flowtable, send to openflow.py
        {
            PyObject * Py_pFun, *Py_pPkt, *Py_pResult;
            Py_pFun = pcore->flowtable->entry[3].action_c; // 3 is now for giniof_01
            Py_pPkt = SWIG_NewPointerObj((void *) in_pkt, SWIGTYPE_p__gpacket_t, 1);
            if (Py_pPkt)
            {
                verbose(2, "Got Pyton obj\n");
                Py_pResult = PyObject_CallFunction(Py_pFun, "O", Py_pPkt);
                CheckPythonError();
            }
        }
        else
            /* found an match, apply action. Only [Output to switch port] is supported */
        {
            /*Other fields..*/
            ofp_action_output_t *action = (ofp_action_output_t *) entry_res->action;
            printAction(action);
            in_pkt->frame.dst_interface = action->port;
            writeQueue(pcore->outputQ, (void *) in_pkt, sizeof (gpacket_t));
        }

    }
}

int addEntry(flowtable_t *flowtable, int type, ushort language, void *content)
{
    verbose(2, "[addEntry]:: \n");
    if (type == CLASSICAL)
    {
        verbose(2, "[addEntry]:: Adding a classical entry\n");
        //TODO: how to add?: append? insert? : Haowei
        //append: reason: less time when check pkt/add entry, more time delete entry;
        if (flowtable->num < MAX_ENTRY_NUMBER)
        {
            flowtable->entry[flowtable->num].is_empty = 0;
            flowtable->entry[flowtable->num].language = language;
            flowtable->entry[flowtable->num].ip_protocol_type = UDP_PROTOCOL; // TODO: temporary soluction
            flowtable->entry[flowtable->num].action_c = content;
            flowtable->num++;
            return EXIT_SUCCESS;
        }
        else
        {
            verbose(2, "[addEntry]:: flowtable is full...Exit with failure\n");
            return EXIT_FAILURE;
        }


    }
    else if (type == OPENFLOW)
    {
        verbose(2, "[addEntry]:: Adding a openflow entry\n");
        return EXIT_SUCCESS;
    }

    return EXIT_FAILURE;
}

int deleteEntry()
{
    verbose(2, "[deleteEntry]:: \n");
    return EXIT_SUCCESS;
}

flowtable_t *initFlowTable()
{
    verbose(2, "[initFlowTable]:: \n");
    flowtable_t *flowtable = (flowtable_t *) malloc(sizeof (flowtable_t));
    flowtable->num = 0;
    //int (*function_ptr)(gpacket_t);
    defaultProtocol(flowtable, ARP_PROTOCOL, (void *) ARPProcess);
    defaultProtocol(flowtable, IP_PROTOCOL, (void *) IPIncomingPacket);
    defaultProtocol(flowtable, ICMP_PROTOCOL, (void *) ICMPProcessPacket);
    verbose(2, "[initFlowTable]:: finished size: %d\n", flowtable->num);
    return flowtable;
}

int defaultProtocol(flowtable_t *flowtable, ushort prot, void *function)
{
    verbose(2, "[defaultProtocol]:: Adding default protocol: %hu\n", prot);
    if (flowtable->num < MAX_ENTRY_NUMBER)
    {
        flowtable->entry[flowtable->num].is_empty = 0;
        flowtable->entry[flowtable->num].language = C_FUNCTION;
        flowtable->entry[flowtable->num].ip_protocol_type = prot;
        flowtable->entry[flowtable->num].action_c = function;
        flowtable->num++;
    }
    else
    {
        verbose(2, "[defaultProtocol]:: Exceed MAX_ENTRY_NUMBER\n");
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}

int addModule(flowtable_t *flowtable, ushort language, char *mod_name)
{
    //TODO: 1. import module 2. find getEntry function 3.addEntry with \
    //given entry
    //======
    //SWIG_init();
    //init_CFT();//TODO: build CFT
    //==
    verbose(2, "[addModule]Start to add protocol");
    switch (language)
    {
    case PYTHON_FUNCTION:
        if (addPyModule(flowtable, mod_name))
            verbose(2, "[addModule]Python module: %s added", mod_name);
        break;
    case C_FUNCTION:
        if (addCModule(flowtable, mod_name))
            verbose(2, "[addModule]C Module: %s added", mod_name);
        break;
    }

    return EXIT_FAILURE;
}
// only check the protocol for now

int addPyModule(flowtable_t *flowtable, char *mod_name)
{
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('./')");

    PyObject *pProtMod, *pProtGlobalDict, *pFuncProcess, *pFuncCommand;
    pProtMod = PyImport_ImportModule(mod_name); //load protocol.py
    if (pProtMod)
    {
        verbose(2, "[addPyModule]-%s- Module loaded\n", mod_name);
        //verbose(2, "[addPyModule]module [udp] imported\n");
        pProtGlobalDict = PyModule_GetDict(pProtMod); // Get main dictionary
        //CheckPythonError();
        if (pProtGlobalDict)
        {
            verbose(2, "[addPyModule]main dictionary got\n");
            pFuncProcess = PyDict_GetItemString(pProtGlobalDict, "Protocol_Processor"); //TODO: find function of getEntry
            verbose(2, "[addPyModule]Protocol_Processor got\n");
            pFuncCommand = PyDict_GetItemString(pProtGlobalDict, "Command_Line");
            if (pFuncCommand == NULL) verbose(2, "[addPyModule]pFuncCommand is NULL!!\n", pFuncCommand);
            verbose(2, "[addPyModule]Command_Line got\n");

            //return a tuple of config info 
            PyObject *PyConfigFunc = PyDict_GetItemString(pProtGlobalDict, "Config");
            verbose(2, "[addPyModule]Config got\n");
            module_config_t *config = (module_config_t *) calloc(1, sizeof (module_config_t));
            PyObject *PyConfigTuple = PyObject_CallFunction(PyConfigFunc, NULL);
            PyArg_ParseTuple(PyConfigTuple, "sHssss", config->name, &(config->protocol), config->command_str, config->shelp, config->usage, config->lhelp);
            //            PyObject *Py_String = 
            //            if (Py_String == NULL)
            //            {
            //                verbose(2, "[addPyModule]Py_String is NULL !\n");
            //            }
            //            char *command = PyString_AsString(Py_String);
            printConfigInfo(config);
            registerCLI(config->command_str, pFuncCommand, PYTHON_FUNCTION, "command", "command", "command");

            verbose(2, "[addPyModule]Command < %p >registered\n", pFuncCommand);
            //CheckPythonError();
            if (pFuncProcess == NULL)
            {
                verbose(2, "[addPyModule]pFunc is NULL !!");
                return EXIT_FAILURE;
            }
            addEntry(flowtable, CLASSICAL, PYTHON_FUNCTION, (void *) pFuncProcess); //add protocol into flow table
            //registerCLI("giniudp", addprotCmd, NULL, NULL, NULL);
            verbose(2, "[addPyModule]!!!!Python Processor added into flowtable!!!");
            return EXIT_SUCCESS;
        }
        verbose(2, "[addPyModule]loading protocol module failed!\n");
        return EXIT_FAILURE;
    }
}

int addCModule(flowtable_t *flowtable, char *mod_name)
{
    //read config info from mod_nameConfig()
    //module_config_t *config = (module_config_t)calloc(1, sizeof(module_config_t));
    module_config_t *config_info;
    void *library = NULL;
    module_config_t * (*config_fun)();
    library = dlopen(mod_name, RTLD_LAZY); //RTLD_LAZY  RTLD_NOW
    if (!library)
    {
        printf("%s \n", dlerror());
    }
    dlerror();
    char tmpbuff[20];
    //config_fun = dlsym(library, Name2ConfigName(tmpbuff, mod_name));
    config_fun = dlsym(library, Name2ConfigName(tmpbuff, "udp2"));
    if (config_fun)
        config_info = config_fun();
    printConfigInfo(config_info);
    registerCLI(config_info->command_str, config_info->command, C_FUNCTION, "command_C", "command_C", "command_C");
    addEntry(flowtable, CLASSICAL, C_FUNCTION, (void *) config_info->processor); //TODO: protocol is not passed..
    return EXIT_SUCCESS;
}

char *Name2ConfigName(char *tmpbuff, char *mod_name)
{
    strcpy(tmpbuff, mod_name);
    strcat(tmpbuff, "Config");
    return tmpbuff;
}

void printConfigInfo(module_config_t *config)
{
    printf("----    Config Information  ----\n");
    printf("module name :       %s\n", config->name);
    printf("protocol    :       %#06x\n", config->protocol);
    printf("processor   :       %p\n", config->processor);
    printf("command     :       %p\n", config->command);
    printf("----       End of Config    ----\n");
}
// use short for result count?

short *ofpFindMatch(flowtable_t *flowtable, ofp_match_t *match, short result[MAX_ENTRY_NUMBER], short *res_num)
{
    printf("[ofpFindMatch]finding the match..\n");
    // TODO: matching algorithm needed....
    ofp_flow_wildcards wc = match->wildcards;
    int i, j, index = 0;
    // all wildcards
    if (wc == OFPFW_ALL)
        for (i = 0; i < MAX_ENTRY_NUMBER; i++)
            if (flowtable->entry[i].is_empty != 1)
            {
                result[index++] = i;
                res_num++;
            }
    // TODO: match
    for (i = 0; i < MAX_ENTRY_NUMBER; i++)
    {
        for (j = 0; j < 12; j++)
        {

        }
    }
    return result;
}

ftentry_t *checkFlowTable(flowtable_t *flowtable, gpacket_t *pkt)
{
    //find the protocol label
    int i, j, fromUpper = 0, prot = NULL_PROTOCOL;
    verbose(2, "[checkFlowTable]:: Search protocol(EtherType): %#06x\n", ntohs(pkt->data.header.prot));
    for (i = 0; i < 8; i++)
    {
        if (pkt->frame.label[i].prot != NULL_PROTOCOL && pkt->frame.label[i].process == 0)
        {
            prot = pkt->frame.label[i].prot;
            verbose(2, "[checkFlowTable]:: Found Next protocol: %hu in pkt: %hu\n", prot, ntohs(pkt->data.header.prot));
            if (pkt->frame.label[i + 1].prot == 1)
            {
                verbose(2, "[checkFlowTable]:: From Upper Layer of %hu", prot);
                fromUpper = 1;
            }
            break;
        }

    }
    if (prot == NULL_PROTOCOL)
    {
        verbose(2, "[checkFlowTable]::Didn't find any protocol in FT!");
        return NULL;
    }
    for (j = 0; j < flowtable->num; j++)
    {
        //verbose(2  , "[checkFlowTable]::Checking for entry");
        if (flowtable->entry[j].ip_protocol_type == prot)
        {
            verbose(2, "[checkFlowTable]:: Entry found protocol(entry): %#06x\n", flowtable->entry[j].ip_protocol_type);
            return &(flowtable->entry[j]);
        }
    }
    verbose(2, "Failed finding a entry!\n");
    return NULL;
}

/* match packet with openflow flowtable.
 * algorithm: naive match
 * return corresponding entry if found, NULL if not.
 */
ftentry_t *checkOFFlowTable(flowtable_t *flowtable, gpacket_t *pkt)
{
    verbose(2, "[checkOFFlowTable]:: Search protocol(EtherType): %#06x\n", ntohs(pkt->data.header.prot));
    int i;
    ushort cur_priority = 0;
    ftentry_t *result = NULL;
    for (i = 0; i < MAX_ENTRY_NUMBER; i++)
    {
        if (flowtable->entry[i].is_empty != 1)
        {
            printf("checking entry[%d]..\n", i);
            if (flowtable->entry[i].priority >= cur_priority && compareFlowAndPkt(&(flowtable->entry[i]), pkt) == FLOW_MATCH)
            {
                result = &(flowtable->entry[i]);
                cur_priority = result->priority;
            }
        }
    }
    return result;
}

/* ntoh() needed for 5 items in packet_in
 * ntol() needed for 2 IP address in packet in.
 * change before match? 'cus match occurs several times for one packet....
 */
int compareFlowAndPkt(ftentry_t *entry, gpacket_t *pkt)
{
    char tmpbuff[MAX_TMPBUF_LEN];

    ofp_match_t *match = &(entry->match);
    uint32_t wildcards = match->wildcards;
    if (wildcards == OFPFW_ALL) return FLOW_MATCH;
    /* which port should be used?..*/
    if (!(wildcards >> 0 & 1) && match->in_port != pkt->frame.src_interface)
    {
        printf("port not matched..\n");
        return FLOW_NOT_MATCH;
    }
    /* vlan tagging not supported..*/
    if (!(wildcards >> 1 & 1))
    {

    }
    /* Ethernet source address. */
    if (!(wildcards >> 2 & 1) && COMPARE_MAC(match->dl_src, pkt->data.header.src) != 0)
    {
        printf("Ethernet source address not matched..\n");
        return FLOW_NOT_MATCH;
    }
    /* Ethernet destination address. */
    if (!(wildcards >> 3 & 1) && COMPARE_MAC(match->dl_dst, pkt->data.header.dst) != 0)
    {
        printf("Ethernet destination address not matched..\n");
        return FLOW_NOT_MATCH;
    }
    /* Ethernet frame type. */
    if (!(wildcards >> 4 & 1) && (match->dl_type != ntohs(pkt->data.header.prot)))
    {
        printf("Ethernet frame type not matched..match: %d, pkt: %d\n", match->dl_type, ntohs(pkt->data.header.prot));
        return FLOW_NOT_MATCH;
    }
    ip_packet_t *ip_pkt = (ip_packet_t *) & pkt->data.data;
    /* IP protocol. */
    if (pkt->data.header.prot == IP_PROTOCOL)
    {
        if (!(wildcards >> 5 & 1) && (match->nw_proto != ip_pkt->ip_prot))
        {
            printf("IP protocol not matched..\n");
            return FLOW_NOT_MATCH;
        }
        /* Match IP*/

        if (compareIPUsingWildcards(gNtohl(tmpbuff, ip_pkt->ip_src), gNtohl(tmpbuff, ip_pkt->ip_dst),
                                    (uchar*) match->nw_src, (uchar*) match->nw_dst, wildcards))
        {
            printf("IP not matched..\n");
            return FLOW_NOT_MATCH;
        }
        tcp_udp_header_t * tcp_udp = (tcp_udp_header_t *) (ip_pkt + 1);
        /* TCP/UDP source port. */
        if (!(wildcards >> 6 & 1) && (match->tp_src != tcp_udp->src_port))
        {
            printf("TCP/UDP source port not matched..\n");
            return FLOW_NOT_MATCH;
        }
        /* TCP/UDP destination port. */
        if (!(wildcards >> 7 & 1) && (match->tp_dst != tcp_udp->dst_port))
        {
            printf("TCP/UDP destination port not matched..\n");
            return FLOW_NOT_MATCH;
        }
        /* VLAN priority. */
        if (wildcards >> 20 & 1)
        {
            /* vlan tagging not supported..*/
        }
        /* IP ToS (DSCP field, 6 bits). */
        if (!(wildcards >> 21 & 1) && (match->nw_tos != ip_pkt->ip_tos))
        {
            printf("IP ToS not matched..\n");
            return FLOW_NOT_MATCH;
        }
    }
    return FLOW_MATCH;
}

int compareFlowAndFlow(ftentry_t *entry, ofp_flow_mod_pkt_t pkt)
{
    //TODO: sufficient implementation needed...
}

void printFlowTable(flowtable_t *flowtable)
{
    printf("--  Flow Table Status  --\n");
    printf("Size: %d\n", flowtable->num);
    printf("Details: \n");
    int i;
    for (i = 0; i < flowtable->num; i++)
    {
        printf("\t[%d]protocol: %d language: %d :: action %p\n",
               i,
               flowtable->entry[i].ip_protocol_type,
               flowtable->entry[i].language,
               flowtable->entry[i].action_c);
    }
    printf("-- End of Flow Table --\n");
}

void DEBUG_ADD_TEST_FLOW_AllWildcards(flowtable_t *flowtable)
{
    ftentry_t *entry = &flowtable->entry[1];
    entry->priority = 1;
    entry->match.wildcards = OFPFW_ALL;
    ofp_action_output_t *action = (ofp_action_output_t *) entry->action;
    action->port = 2;
    action->type = OFPAT_OUTPUT;
    return;
}

void DEBUG_ADD_TEST_FLOW_ARPFlow(flowtable_t *flowtable)
{
    ftentry_t *entry = &flowtable->entry[0];
    entry->priority = 1;
    /* for ARP*/
    entry->match.wildcards = OFPFW_IN_PORT | OFPFW_DL_VLAN | OFPFW_DL_SRC | OFPFW_DL_DST
            | OFPFW_NW_PROTO | OFPFW_TP_SRC | OFPFW_TP_DST | OFPFW_DL_VLAN_PCP | OFPFW_NW_TOS
            | 0x1F << 8 | 0x1F << 14;
    entry->match.dl_type = ARP_PROTOCOL;
    ofp_action_output_t *action = (ofp_action_output_t *) entry->action;
    action->port = 1;
    action->type = OFPAT_OUTPUT;
    return;
}

int ofpFlowMod(flowtable_t *flowtable, ofp_flow_mod_pkt_t *flow_mod_pkt)
{
    printf("[ofpFlowMod] Receive FLOW MOD pkt!\n");
    printOFPFlowModPkt(flow_mod_pkt);
    DEBUG_ADD_TEST_FLOW_AllWildcards(flowtable);
    DEBUG_ADD_TEST_FLOW_ARPFlow(flowtable);
    printAction(flowtable->entry[0].action);
    switch (flow_mod_pkt->command)
    {
    case 0:
        ofpFlowModAdd(flowtable, flow_mod_pkt);
        break;
    case 1:
        ofpFlowModModify(flowtable, flow_mod_pkt);
        break;
    case 2:
        ofpFlowModModifyStrict(flowtable, flow_mod_pkt);
        break;
    case 3:
        ofpFlowModDelete(flowtable, flow_mod_pkt);
        break;
    case 4:
        ofpFlowModDeleteStrict(flowtable, flow_mod_pkt);
        break;
    default:
        printf("Flow Mod Command invalid...\n");
        break;
    }
    return EXIT_SUCCESS;
}

//int ofpFlowMod2(flowtable_t *flowtable, void *msg)
//{
//    printf("[ofpFlowMod2] Receive FLOW MOD pkt!\n");
//    ofp_flow_mod_pkt_t *flow_mod_pkt = msg;
//    printOFPFlowModPkt(flow_mod_pkt);
//    return EXIT_SUCCESS;
//}

int ofpFlowModAdd(flowtable_t *flowtable, ofp_flow_mod_pkt_t *flow_mod_pkt)
{
    verbose(2, "[ofpFlowModAdd]Adding a Match to flow table...\n");
    int i;
    ftentry_t *entry;
    for (i = 0; i < MAX_ENTRY_NUMBER; i++)
    {
        if (flowtable->entry[i].is_empty)
        {
            entry = &(flowtable->entry[i]);
            break;
        }
        if (i == MAX_ENTRY_NUMBER - 1) verbose(1, "[ofpFlowModAdd] Flow table is full, adding failed!\n");
    }
    // TODO: ADD......be ware of action[0]..variable length..
    entry->is_empty = 0;
    memcpy(& entry->match, & flow_mod_pkt->match, sizeof(ofp_match_t));
    entry->count = 0;
    /*size ? is memory alloced properly?*/
    memcpy(& entry->action, & flow_mod_pkt->actions, flow_mod_pkt->actions->len);
    
    return EXIT_SUCCESS;
}

int ofpFlowModModify(flowtable_t *flowtable, ofp_flow_mod_pkt_t *flow_mod_pkt)
{
    verbose(2, "[ofpFlowModAdd]Modifying a Match in flow table...\n");

    return EXIT_SUCCESS;
}

int ofpFlowModModifyStrict(flowtable_t *flowtable, ofp_flow_mod_pkt_t *flow_mod_pkt)
{
    verbose(2, "[ofpFlowModModifyStrict]Modifying a Match in flow table...\n");
    return EXIT_SUCCESS;
}

int ofpFlowModDelete(flowtable_t *flowtable, ofp_flow_mod_pkt_t *flow_mod_pkt)
{
    verbose(2, "[ofpFlowModDelete]Deleting a Match from flow table...\n");
    //findMatch();
    short result[MAX_ENTRY_NUMBER] = {0};
    short res_num = 0;
    //ofpFindMatch(flowtable, &(flow_mod_pkt->match), result, &res_num);
    verbose(2, "[ofpFlowModDelete]Deleted..\n");
    return EXIT_SUCCESS;
}

int ofpFlowModDeleteStrict(flowtable_t *flowtable, ofp_flow_mod_pkt_t *flow_mod_pkt)
{
    verbose(2, "[ofpFlowModDeleteStrict]Deleting a Match from flow table...\n");
    return EXIT_SUCCESS;
}

void printOFPFlowModPkt(ofp_flow_mod_pkt_t *flow_mod_pkt)
{
    uchar tmpbuff[MAX_TMPBUF_LEN];
    printf("--  Flow_Mod packet --\n");
    printf("Version: %" PRIu8 "\n", flow_mod_pkt->header.version);
    printf("Type: %" PRIu8 "\n", flow_mod_pkt->header.type);
    printf("Length: %" PRIu16 "\n", flow_mod_pkt->header.length);
    printf("before convert: %x", flow_mod_pkt->header.xid);
    printf("Xid: %" PRIu32 "\n", flow_mod_pkt->header.xid);
    printf("Cookie: %" PRIu64 "\n", flow_mod_pkt->cookie);
    printf("Command: %" PRIu16 "\n", flow_mod_pkt->command);
    printf("Priority: %" PRIu16 "\n", flow_mod_pkt->priority);
    printf("before convert: %x", flow_mod_pkt->buffer_id);
    printf("BufferId: %" PRIu32 "\n", flow_mod_pkt->buffer_id);
    printf("Out port: %" PRIu16 "\n", flow_mod_pkt->out_port);
    printf("--  End of packet  --\n");
}

printAction(ofp_action_output_t *action)
{
    printf("--  action  --\n");
    printf("type: %" PRIu16 "\n", action->type);
    printf("port: %" PRIu16 "\n", action->port);
    printf("--    end   --\n");
}

int compareIPUsingWildcards(uchar *ip_src_p, uchar * ip_dst_p,
                            uchar *ip_src_f, uchar *ip_dst_f, ofp_flow_wildcards wc)
{
    int mask_src = wc >> 8 & 0x1F;
    int mast_dst = wc >> 14 & 0x1F;
    return memcmp(ip_src_p, ip_src_f, mask_src) | memcmp(ip_dst_p, ip_dst_f, mast_dst);
}