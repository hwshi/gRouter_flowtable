/*
 * flowtable.h (include file for the flow table)
 * AUTHOR: Haowei Shi
 * DATE: October 01, 2014
 *
 */

#ifndef __FLOW_TABLE_H__
#define __FLOW_TABLE_H__
#define MAX_ENTRY_NUMBER 50
#include <slack/std.h>
#include <slack/map.h>
#include <slack/list.h>
#include <pthread.h>
#include <sys/types.h>

#include "message.h"
#include "grouter.h"
#include "simplequeue.h"
#include "qdisc.h"
#include "protocols.h"
 #include "ip.h"
 #include "arp.h"
 #include "icmp.h"
//#include "packetcore.h"
//tpye of entry
#define CLASSICAL 1
#define OPENFLOW 2

 //type of language
 #define C_FUNCTION 0
 #define PYTHON_FUNCTION 1


//flow table
typedef struct _ftentry_t
{
	ushort is_empty; // 1 empty 0 occupied
	ushort language; // 0 C 1 PYTHON
    ushort protocol;
    void *action;
} ftentry_t;

typedef struct _flowtable_t
{
    int num;
    ftentry_t entry[MAX_ENTRY_NUMBER];
} flowtable_t;

int addEntry(flowtable_t *flowtable, int type, ushort language, void *content);
int deleteEntry();
flowtable_t *initFlowTable();
int defaultProtocol(flowtable_t *flowtable, ushort prot, void *function);
int addProtocol(flowtable_t *flowtable,ushort language, char *protname);
ftentry_t *checkFlowTable(flowtable_t *flowtable, gpacket_t *pkt);
void printFlowTable(flowtable_t *flowtable);
#endif