//file: message.i
%module GINIC
%inline %{
#include <sys/types.h>
#include "grouter.h"
#include "message.h"
#include "arp.h"
#include "gnet.h"
#include "ip.h"
#include "packetcore.h"
#include "routetable.h"
#include "mtu.h"
#define MAX_IPREVLENGTH_ICMP            50       // maximum previous header sent back
#define MAX_MESSAGE_SIZE                sizeof(gpacket_t)
#define uchar unsigned char
#define ushort unsigned short

    
    extern interface_array_t netarray;  // interface table from gnet.h
    extern pktcore_t *pcore;
    extern route_entry_t route_tbl[MAX_ROUTES]; // routing table
    extern mtu_entry_t MTU_tbl[MAX_MTU]; // MTU table
    
    extern interface_array_t netarray;
    extern devicearray_t devarray;
    extern arp_entry_t arp_cache[ARP_CACHE_SIZE];
    extern arp_entry_t ARPtable[MAX_ARP];		                // ARP table
    extern arp_buffer_entry_t ARPbuffer[MAX_ARP_BUFFERS];   	// ARP buffer for unresolved packets
    extern int tbl_replace_indx;            // overwrite this element if no free space in ARP table
    extern int buf_replace_indx;            // overwrite this element if no free space in ARP buffer
    
    PyObject * getUDPPacketString(gpacket_t * gpacket) {
//        printf("[UDPPacketString]:: 1\n");
        //int gpayload = sizeof(gpacket->data.data);
        int payload = sizeof (gpacket->data.data);
        int gheader = sizeof (gpacket_t) - payload;
        int udplen = sizeof (*gpacket) - gheader - sizeof (ip_packet_t);
//        printf("[UDPPacketString]:: 2\n");
        ip_packet_t *ip_pkt = (ip_packet_t *) gpacket->data.data;
//        printf("[UDPPacketString]:: 3\n");
//        printf("gpayload: %d size of ip_t %d", payload, sizeof (ip_packet_t));
        return PyString_FromStringAndSize((char *) (ip_pkt + 1), udplen);
    }
    //helper function for gpacket

    gpacket_t * createGPacket(PyObject * pkt) {
        void * pktString = PyString_AsString(pkt);
//        printf("[helpr - createGPacket]\n");
        gpacket_t *gpkt = (gpacket_t *) malloc(sizeof (gpacket_t));
        memcpy(gpkt->data.data, pktString, sizeof (pktString));
        //gpkt->data.data = (uchar*)pkt;
//        printf("[createGPacket] coppied %d byte\n", sizeof (pktString));
        return gpkt;

    }

    PyObject* getGPacketString(gpacket_t * gpacket) {
        return PyString_FromStringAndSize((char *) (&gpacket->data.data), sizeof (*gpacket));
    }
    
    PyObject* getDeviceName()
    {
        char name[100];
        printf("[getDevicename]-------------");
        //printRouteTable(route_tbl);
        //printInterfaces(11);
//        int i;
//        for(i = 0; i < 200; i ++)
        printf("1");
        printf("2");
        MAC2Colon(name, netarray.elem[0]->mac_addr);
        printf("3");
        printf("name is : %s", name);
        printf("[getDeviceName]2");
        //sprintf(name, "%02x%02x%02x%02x%02x%02x", netarray.elem[0]->mac_addr[0], netarray.elem[0]->mac_addr[1], netarray.elem[0]->mac_addr[2], 
        //netarray.elem[0]->mac_addr[3], netarray.elem[0]->mac_addr[4], netarray.elem[0]->mac_addr[5]);
        //printf("[getDeviceName] name is: %s", name);
        return PyString_FromStringAndSize("aaaaaaaaaaaa", 12);
    }

%}

typedef struct _pkt_data_t {

    struct {
        uchar dst[6]; // destination host's MAC address (filled by gnet)
        uchar src[6]; // source host's MAC address (filled by gnet)
        ushort prot; // protocol field
    } header;
    uchar data[DEFAULT_MTU]; //payloadPyObject_CallFunction     // PyObject_CallFunction (limited to maximum MTU)
} pkt_data_t;

typedef struct _label_t {
    ushort prot;
    ushort process; //0 un process  1 processed 2 invalid
} label_t;
// frame wrapping every packet... GINI specific (GINI metadata)

typedef struct _pkt_frame_t {
    int src_interface; // incoming interface number; filled in by gnet?
    uchar src_ip_addr[4]; // source IP address; required for ARP, IP, gnet
    uchar src_hw_addr[6]; // source MAC address; required for ARP, filled by gnet
    int dst_interface; // outgoing interface, required by gnet; filled in by IP, ARP
    uchar nxth_ip_addr[4]; // destination interface IP address; required by ARP, filled IP
    int arp_valid;
    int arp_bcast;
    label_t label[8]; // label for flow table; required by packet core, filled by each protoco process
} pkt_frame_t;

typedef struct _gpacket_t {
    pkt_frame_t frame;
    pkt_data_t data;
} gpacket_t;

%typemap(in) uchar * {
//    printf("[typemap-uchar*]\n");
    $1 = PyString_AsString($input);
}

%typemap(in) gpacket_t* out_gpkt {
//    printf("[typemap-gpacket_t *out_gpkt]\n");
    int size  = PyString_Size($input);
    gpacket_t* gpkt = (gpacket_t *)calloc(1, sizeof(gpacket_t));
    memcpy((gpkt->data.data)+sizeof (ip_packet_t), PyString_AsString($input), size);
    $1 = gpkt;
}


int IPOutgoingPacket(gpacket_t *out_gpkt, uchar *dst_ip, int size, int newflag, int src_prot);
