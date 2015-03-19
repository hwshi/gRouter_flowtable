//file: message.i
%module Cmessage

%inline%{
	#include <sys/types.h>
	#include "grouter.h"
	#include "message.h"
	#include "ip.h"
	#define MAX_IPREVLENGTH_ICMP            50       // maximum previous header sent back
	#define MAX_MESSAGE_SIZE                sizeof(gpacket_t)
	#define uchar unsigned char
	#define ushort unsigned short
%}

#define uchar unsigned char
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
} pkt_frame_t;


typedef struct _gpacket_t 
{
	pkt_frame_t frame;
	pkt_data_t data;
} gpacket_t;