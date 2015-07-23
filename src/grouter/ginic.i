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
        char name[200];
        interface_t *ifptr;
        int i;
        for(i = 0; i < 20; i ++)
            if(netarray.elem[i] != NULL)
                break;
        verbose(3, "[SWIG - getDeviceName]Index: %d\n", i);
        ifptr = netarray.elem[i];
        printf("[getDevicename]---number: %d", netarray.count);
        sprintf(name, "%02x%02x%02x%02x%02x%02x", ifptr->mac_addr[0], ifptr->mac_addr[1], ifptr->mac_addr[2], 
               ifptr->mac_addr[3], ifptr->mac_addr[4],ifptr->mac_addr[5]);
        printf("[getDeviceName] name is: %s\n", name);
        //return PyString_FromStringAndSize("aaaaaaaaaaaa", 12);
        return PyString_FromStringAndSize(name, 12);
    }
    
    int getPortNumber()
    {
        return netarray.count;
    }
    
    PyObject* getPortTuple()
    {
        PyObject *port_list = PyTuple_New(netarray.count);
        int i, tuple_index = 0;
//        for(i = 0; i < MAX_INTERFACES; i ++)
//        {
//            if(netarray.elem[i] != NULL)
//            {
//                //int PyTuple_SetItem(PyObject *p, Py_ssize_t pos, PyObject *o) 
//                // this function steal a reference to "o"
//                // TODO - DONE: need to convert netarray.elem[] to PyObject.....using PyTupple_Pack()
//                
//                if(PyTuple_SetItem(port_list, tuple_index ++, PyTuple_Pack(2, i, netarray.elem[i])) != 0)
//                    printf("Failed to build port tuple");
//            }
//        }
        //DEBUG:
        //PyObject* tuple = PyTuple_Pack(1, i);
        //PyObject* tuple = PyTuple_Pack(2, i, netarray.elem[1]);
        PyObject* tuple = Py_BuildValue("o", netarray.elem[1]);
        PyTuple_SetItem(port_list, 0, tuple);
        return port_list;
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
