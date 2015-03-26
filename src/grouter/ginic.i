//file: message.i
%module GINIC

%inline%{
	#include <sys/types.h>
	#include "grouter.h"
	#include "message.h"
	#include "ip.h"
	#define MAX_IPREVLENGTH_ICMP            50       // maximum previous header sent back
	#define MAX_MESSAGE_SIZE                sizeof(gpacket_t)
	#define uchar unsigned char
	#define ushort unsigned short

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
	#endif

%}

	typedef struct _pkt_data_t
	{
		struct
		{
			uchar dst[6];                // destination host's MAC address (filled by gnet)
			uchar src[6];                // source host's MAC address (filled by gnet)
			ushort prot;                // protocol field
		} header;
		uchar data[DEFAULT_MTU];             // payload (limited to maximum MTU)
	} pkt_data_t;

	typedef struct _label_t
	{
	    ushort prot;
	    ushort process;//0 un process  1 processed 2 invalid
	} label_t;
	// frame wrapping every packet... GINI specific (GINI metadata)
	typedef struct _pkt_frame_t
	{
		int src_interface;               // incoming interface number; filled in by gnet?
		uchar src_ip_addr[4];            // source IP address; required for ARP, IP, gnet
		uchar src_hw_addr[6];            // source MAC address; required for ARP, filled by gnet
		int dst_interface;               // outgoing interface, required by gnet; filled in by IP, ARP
		uchar nxth_ip_addr[4];           // destination interface IP address; required by ARP, filled IP
		int arp_valid;
		int arp_bcast;
		label_t label[8];				 // label for flow table; required by packet core, filled by each protoco process
	} pkt_frame_t;


	typedef struct _gpacket_t 
	{
		pkt_frame_t frame;
		pkt_data_t data;
	} gpacket_t;