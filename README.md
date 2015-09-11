# gRouter_flowtable
gRouter is the core of GINI(http://cgi.cs.mcgill.ca/~anrl/gini/)
gRouter is written from scratch with most of the functionalities and controls found in a general router. 
gRouter provides a simple but flexible implementation that can be easily extended by students.

------------ Threads ------------

grouter------...
		|--	threads
		|--	.
		|-- PacketProcessor -> checking workQ
		|-- DecisionProcessor -> checking DecisionQ and process in corresponding module.


------------ Threads ------------
packet -> router
			|
			v
		workQ : lable
			|
			v
		DecisionQ ---> check flowtable for module[3 default protocol: ARP IP ICMP]
			^					|
			|			 C		v
		lableNext <---	    processor
								|  -Python-
			
								v
						call wrapped function:   IP layer output interface provided.

TODO 	1. handle return from python.
		2. merge flowtable(into flow_match in openflow...)


------------ Developing Notes ------------
/* config struct for module importing */
typedef struct _module_config_t
{
    char *name;				/* name of the module */
    ushort protocol;		/* protocol number of the module */
    void *processor;		/* the function processing the packet */
    void *command;			/* the function registered for command line */
    char *command_str;		/* the command registered for [command function] */
    char *shelp;			/* short help message */
    char *usage;			/* instructions of using the module */
    char *lhelp;			/* help message in detail */
} module_config_t;

/* class for python */
/* config */

class module_config:
    def __init__(self, name="module", protocol=255, command_string="",
                 short_help="", usage="", long_help="")
    def to_tuple(self)

/* GPacket */
class GPacket:
	def __init__(self,ip_payload=None)
	def dissemble(self, msg)
	def assemble(self)
       
/* 
 * module prototype 
 */
/* Python module */
/* 0. import _GINIC as GINIC
/* 1. implement public function */
def Config():
    config = module_config(name="udp", protocol=17, command_string="nc", short_help="udp function",
                           usage="nc -l [port] nc [IP][port]",
                           long_help="sending and listening to udp packet")
    return config.to_tuple()
/* 2. implement public function Protocol_Processor
 *		a. argument is gPacket_t from C
 *		b. return value to be determined..
 */
def Protocol_Processor(pkt)
/* 3. implement public function Command_Line
 *		a. argument is the option from C
 */
def Command_Line(str)

/*
 * Helper functions
 * Calling by GINIC.IPPayload()
 */

 
/* returns the IP payload of a gpackeet */
PyObject * IPPayload(gpacket_t * gpacket);
/* helper function for gpacket */
gpacket_t * createGPacket(PyObject * pkt);
/* returns a new packet with only ip_payload changed */
gpacket_t * assembleWithIPPayload(PyObject * gpacket_py, PyObject * payload);
/* returns a gpacket with ip_payload as input */
gpacket_t * createGPacketWithIPPayload(PyObject * payload);
PyObject *getGPacketMetaheaderLen();
PyObject* getGPacketString(gpacket_t * gpacket);

/* Interface for C function in GINI */
/*1. IP Layer Out Put*/
GINIC.IPOutgoingPacket(gpacket_t *out_gpkt, uchar *dst_ip, int size, int newflag, int src_prot);
/* sample */
out_gpkt: gPacket_t.assemble()
dst_ip: ip address of destination in NETWORK ENDIAN. // TODO: Use typemap? so that could call us [192.168.1.2] or '192.168.1.2'
size: packet size
newflag:	0 use old packet. only ip_payload will be updated.
			1 create new packet. ip_payload is attached to an empty header.



/* C Module */
/* Similar implementation... */

/* Import module */
addmod [module name] [language]

sample: addmod udp python


