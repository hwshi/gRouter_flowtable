/*
 * flowtable.h (include file for the flow table)
 * AUTHOR: Haowei Shi
 * DATE: October 01, 2014
 *
 */

#ifndef __FLOW_TABLE_H__
#define __FLOW_TABLE_H__
#define MAX_ENTRY_NUMBER 50
#define MAX_ENTRY_SIZE 4
#include <slack/std.h>
#include <slack/map.h>
#include <slack/list.h>
#include <pthread.h>
#include <sys/types.h>
#include <dlfcn.h>
#include <string.h>

#include "message.h"
#include "grouter.h"
#include "simplequeue.h"
#include "qdisc.h"
#include "protocols.h"
#include "ip.h"
#include "arp.h"
#include "icmp.h"
//#include "packetcore.h"

#define OFP_ETH_ALEN 6

//tpye of entry
#define CLASSICAL 1
#define OPENFLOW 2

//type of language
#define C_FUNCTION 0
#define PYTHON_FUNCTION 1

//config infor

typedef struct _module_config_t
{
    char name[20];
    ushort protocol;
    void *processor;
    void *command;
    char command_str[20];
} module_config_t;

/* Fields to match against flows */
typedef struct _ofp_match_t
{
    uint32_t wildcards;                 /* Wildcard fields. */
    uint16_t in_port;                   /* Input switch port. */
    uint8_t dl_src[OFP_ETH_ALEN];       /* Ethernet source address. */
    uint8_t dl_dst[OFP_ETH_ALEN];       /* Ethernet destination address. */
    uint16_t dl_vlan;                   /* Input VLAN id. */
    uint8_t dl_vlan_pcp;                /* Input VLAN priority. */
    uint8_t pad1[1];                    /* Align to 64-bits */
    uint16_t dl_type;                   /* Ethernet frame type. */
    uint8_t nw_tos;                     /* IP ToS (actually DSCP field, 6 bits). */
    uint8_t nw_proto;                   /* IP protocol or lower 8 bits of
                                         * ARP opcode. */
    uint8_t pad2[2];                    /* Align to 64-bits */
    uint32_t nw_src;                    /* IP source address. */
    uint32_t nw_dst;                    /* IP destination address. */
    uint16_t tp_src;                    /* TCP/UDP source port. */
    uint16_t tp_dst;                    /* TCP/UDP destination port. */
} ofp_match_t;
//OFP_ASSERT(sizeof (struct ofp_match) == 40);

/* Flow wildcards. */
typedef enum _ofp_flow_wildcards
{
    OFPFW_IN_PORT = 1 << 0,             /* Switch input port. */
    OFPFW_DL_VLAN = 1 << 1,             /* VLAN id. */
    OFPFW_DL_SRC = 1 << 2,              /* Ethernet source address. */
    OFPFW_DL_DST = 1 << 3,              /* Ethernet destination address. */
    OFPFW_DL_TYPE = 1 << 4,             /* Ethernet frame type. */
    OFPFW_NW_PROTO = 1 << 5,            /* IP protocol. */
    OFPFW_TP_SRC = 1 << 6,              /* TCP/UDP source port. */
    OFPFW_TP_DST = 1 << 7,              /* TCP/UDP destination port. */
    
    /* IP source address wildcard bit count. 0 is exact match, 1 ignores the
     * LSB, 2 ignores the 2 least-significant bits, ..., 32 and higher wildcard
     * the entire field. This is the *opposite* of the usual convention where
     * e.g. /24 indicates that 8 bits (not 24 bits) are wildcarded. */
    OFPFW_NW_SRC_SHIFT = 8,
    OFPFW_NW_SRC_BITS = 6,
    OFPFW_NW_SRC_MASK = ((1 << OFPFW_NW_SRC_BITS) - 1) << OFPFW_NW_SRC_SHIFT,
    OFPFW_NW_SRC_ALL = 32 << OFPFW_NW_SRC_SHIFT,
    /* IP destination address wildcard bit count. Same format as source. */
    OFPFW_NW_DST_SHIFT = 14,
    OFPFW_NW_DST_BITS = 6,
    OFPFW_NW_DST_MASK = ((1 << OFPFW_NW_DST_BITS) - 1) << OFPFW_NW_DST_SHIFT,
    OFPFW_NW_DST_ALL = 32 << OFPFW_NW_DST_SHIFT,
    OFPFW_DL_VLAN_PCP = 1 << 20, /* VLAN priority. */
    OFPFW_NW_TOS = 1 << 21, /* IP ToS (DSCP field, 6 bits). */
    /* Wildcard all fields. */
    OFPFW_ALL = ((1 << 22) - 1)
} ofp_flow_wildcards;

typedef enum _ofp_action_type
{
    OFPAT_OUTPUT,                       /*Output to switch port. */
    OFPAT_SET_VLAN_VID,                 /*Set the 802.1q VLAN id. */
    OFPAT_SET_VLAN_PCP,                 /*Set the 802.1q priority. */
    OFPAT_STRIP_VLAN,                   /*Strip the 802.1q header. */
    OFPAT_SET_DL_SRC,                   /*Ethernet source address. */
    OFPAT_SET_DL_DST,                   /*Ethernet destination address. */
    OFPAT_SET_NW_SRC,                   /*IP source address. */
    OFPAT_SET_NW_DST,                   /*IP destination address. */
    OFPAT_SET_NW_TOS,                   /*IP ToS (DSCP field, 6 bits). */
    OFPAT_SET_TP_SRC,                   /*TCP/UDP source port. */
    OFPAT_SET_TP_DST,                   /*TCP/UDP destination port. */
    OFPAT_ENQUEUE,                      /*Output to queue. */
    OFPAT_VENDOR = 0xffff
} ofp_action_type;
//flow table
// TODO: an new flow table entry need to be designed.

//TODO: change it into struct of unions? (classical and openflow...)
typedef struct _ftentry_t
{
    // for gini_classic
    ushort is_empty;
    ushort language;
    ushort ip_protocol_type;
    // for of
    ofp_match_t match;
    int count;
    ofp_action_type action;
    //for gini_classic
    void *action_c;
} ftentry_t;

//typedef struct _ftentry_t
//{
//    ushort is_empty; // 1 empty 0 occupied
//    ushort language; // 0 C 1 PYTHON
//    ushort protocol;
//    void *action;
//} ftentry_t;

typedef struct _flowtable_t
{
    int num;
    //ftentry_t entry[MAX_ENTRY_NUMBER];
    ftentry_t entry[MAX_ENTRY_NUMBER];
} flowtable_t;

typedef struct _ofp_header_t
{
    uint8_t version;
    uint8_t type;
    uint16_t length;
    uint32_t xid;
} ofp_header_t;
typedef struct _ofp_action_header_t
{
    uint16_t type;                      /* One of OFPAT_*. */
    uint16_t len;                       /* Length of action, including this
                                        header. This is the length of action,
                                        including any padding to make it
                                        64-bit aligned. */
    uint8_t pad[4];
} ofp_action_header_t;
typedef struct _ofp_flow_mod_pkt_t
{
    ofp_header_t header;
    ofp_match_t match;                  /* Fields to match */
   
    uint64_t cookie;                    /* Opaque controller-issued identifier. */

    /* Flow actions. */
    uint16_t command;                   /*One of OFPFC_*. */
    uint16_t idle_timeout;              /*Idle time before discarding (seconds). */
    uint16_t hard_timeout;              /*Max time before discarding (seconds). */
    uint16_t priority;                  /*Priority level of flow entry. */
    uint32_t buffer_id;                 /*Buffered packet to apply to (or -1).
                                        Not meaningful for OFPFC_DELETE*. */
    uint16_t out_port;                  /* For OFPFC_DELETE* commands, require
                                        matching entries to include this as an
                                        output port. A value of OFPP_NONE
                                        indicates no restriction. */

    uint16_t flags;                     /* One of OFPFF_*. */
// TODO: define....
    ofp_action_header_t actions[0];/* The action length is inferred
                                        from the length field in the
                                        header. */
} ofp_flow_mod_pkt_t;

void *judgeProcessor(void *pc);
int addEntry(flowtable_t *flowtable, int type, ushort language, void *content);
int deleteEntry();
flowtable_t *initFlowTable();
int defaultProtocol(flowtable_t *flowtable, ushort prot, void *function);
int addProtocol(flowtable_t *flowtable, ushort language, char *protname);
int addModule(flowtable_t *flowtable, ushort language, char *mod_name);
int addPyModule(flowtable_t *flowtable, char *mod_name);
int addCModule(flowtable_t *flowtable, char *mod_name);

ftentry_t *checkFlowTable(flowtable_t *flowtable, gpacket_t *pkt);
void printFlowTable(flowtable_t *flowtable);

char *Name2ConfigName(char *tmpbuff, char *mod_name);
void printConfigInfo(module_config_t *config);


// function prototyp for openflow protocol
ftentry_t *checkOFFlowTable(flowtable_t *flowtable, gpacket_t *pkt);
int ofpFlowModAdd();
int ofpFlowModModify();
int ofpFLowModModifyStrict();
int ofpFlowModDelete();
int ofpFlowModDleteStrict();
#endif