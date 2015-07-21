//file: ip.i
%module Cip

%inline%{

	#include "message.h"
	#include "grouter.h"
	#include "routetable.h"
	#include "mtu.h"
	#include "protocols.h"
	#include "ip.h"
	#include "fragment.h"
	#include "packetcore.h"
	#include <stdlib.h>
	#include <slack/err.h>
	#include <netinet/in.h>
	#include <string.h>
	//**Swig Haowei
	#include <stdint.h>
	#include <endian.h>
	#define TEST_DF_BITS(X)                 ( (X & IP_DF) >> 14)
	#define TEST_MF_BITS(X)                 ( (X & IP_MF) >> 13)
	#define SET_DF_BITS(X)                  X = ( X | (0x00001 << 14) )
	#define SET_MF_BITS(X)                  X = ( X | (0x00001 << 13) )
	#define RESET_DF_BITS(X)                X = ( X & (~(0x00001 << 14)) )
	#define RESET_MF_BITS(X)                X = ( X & (~(0x00001 << 13)) )


	//global
	extern pktcore_t *pcore;


	//helper function for ippacket
	#ifndef __IP__HELPER__
	#define __IP__HELPER__
	PyObject* getUDPPacketString(gpacket_t *gpacket){
		printf("[UDPPacketString]:: 1\n");
		//int gpayload = sizeof(gpacket->data.data);
		int payload = sizeof(gpacket->data.data);
		int gheader = sizeof(gpacket_t) - payload;
		int udplen = sizeof(*gpacket) - gheader - sizeof(ip_packet_t);
		printf("[UDPPacketString]:: 2\n");
		ip_packet_t *ip_pkt = (ip_packet_t *)gpacket->data.data;
		printf("[UDPPacketString]:: 3\n");
		printf("gpayload: %d size of ip_t %d", payload, sizeof(ip_packet_t));
		return PyString_FromStringAndSize((char *) (ip_pkt + 1), udplen);
	}
	//helper function for gpacket
	PyObject* getGPacketString(gpacket_t *gpacket){
		return PyString_FromStringAndSize((char *)(&gpacket->data.data), sizeof(*gpacket));
	}
	extern int PythonError(PyObject *pObj);
	#endif
	//int IPSend2Output(gpacket_t *pkt);
%}
//get wrapped gpacket structure
%include "message.i"


//%ignore pcore

//typemap:
%typemap(in) gpacket_t *pyUDPpkt {
	printf("[TypeMap:] gpacket_t *pyUDPpkt\n");
	gpacket_t* gpkt = (gpacket_t *)malloc(sizeof(gpacket_t));
	ip_packet_t *ippkt = (ip_packet_t *)gpkt->data.data;
	char * udpkpt = (char *) (ippkt + 1);
	char * tmpstr = PyString_AsString($input);
	int udplen = PyString_Size($input);
	printf("[TypeMap:]udp size: %d\n", udplen);

	memcpy(udpkpt, tmpstr, udplen);

	$1 = gpkt;
	//free(gpkt);
}

%typemap(in) uchar *dst_ip {
	printf("[TypeMap:] uchar *dst_ip\n");
	$1 = PyString_AsString($input);
}

//TODO: free for typemap
//%typemap(freearg) gpacket_t *pyUDPpkt {
//   free($1);
//}

typedef struct _ip_packet_t
{
#if __BYTE_ORDER == __LITTLE_ENDIAN
	uint8_t ip_hdr_len:4;                   // header length 
	uint8_t ip_version:4;                   // version 
#endif
#if __BYTE_ORDER == __BIG_ENDIAN
	uint8_t ip_version:4;                   // version 
	uint8_t ip_hdr_len:4;                   // header length 
#endif
	uint8_t ip_tos;                         // type of service 
	uint16_t ip_pkt_len;                    // total length 
	uint16_t ip_identifier;                 // identification 
	uint16_t ip_frag_off;                   // fragment offset field 
#define IP_RF 0x8000                            // reserved fragment flag 
#define IP_DF 0x4000                            // dont fragment flag 
#define IP_MF 0x2000                            // more fragments flag 
#define IP_OFFMASK 0x1fff                       // mask for fragmenting bits 
	uint8_t ip_ttl;                         // time to live 
	uint8_t ip_prot;                        // protocol 
	uint16_t ip_cksum;                      // checksum 
	uchar ip_src[4], ip_dst[4];             // source and dest address 
} ip_packet_t;

//wrapped functions
int IPOutgoingPacket(gpacket_t *pyUDPpkt, uchar *dst_ip, int size, int newflag, int src_prot);
