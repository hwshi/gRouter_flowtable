__author__ = 'Haowei Shi'

import _GINIC as GINIC

from ginilib import *

print("--    SIMPLE UDP IMPLEMENTATION FOR GINI    --")

class UDPPacket(Packet):
    name = "UDPPacket"
    fields_desc = [ ShortEnumField("sport", 53, {8888 : "test", 7 : "echo"}),
                    ShortEnumField("dport", 53, {8888 : "test", 7 : "echo"}),
                    ShortField("len", None),
                    XShortField("chksum", None), ]
    #methods for layer
    def extract_padding(self, s):
        l = self.len - 8
        return s[:l],s[l:]
    def post_build(self, p, pay):
        p += pay
        l = self.len
        if l is None:
            l = len(p)
            p = p[:4]+struct.pack("!H",l)+p[6:]
        if self.chksum is None:
            if isinstance(self.underlayer, IP):
                if self.underlayer.len is not None:
                    ln = self.underlayer.len-20
                else:
                    ln = len(p)
                psdhdr = struct.pack("!4s4sHH",
                                     inet_aton(self.underlayer.src),
                                     inet_aton(self.underlayer.dst),
                                     self.underlayer.proto,
                                     ln)
                ck=checksum(psdhdr+p)
                p = p[:6]+struct.pack("!H", ck)+p[8:]
            elif isinstance(self.underlayer, scapy.layers.inet6.IPv6) or isinstance(self.underlayer, scapy.layers.inet6._IPv6ExtHdr):
                ck = scapy.layers.inet6.in6_chksum(socket.IPPROTO_UDP, self.underlayer, p)
                p = p[:6]+struct.pack("!H", ck)+p[8:]
            else:
                warning("No IP underlayer to compute checksum. Leaving null.")
        return p

class UDPpcb(object):
    def __init__(self):
        self.port_set = set()
    def send(self, dip, sp, dp):
        print("[UDPPcb.send] input your msg")
        while True:
            str = raw_input()
            # payload = UDPPacket(sport = sp, dport = dp, len  = None, chksum = None)/str /IP() / Ether()
            payload = UDPPacket(sport = sp, dport = dp, len  = None, chksum = None)
            payload.add_payload(str)
            hexdump(payload)
            send_payload_to_ip(payload, dip, 17)
    def listen(self, port):
        self.port_set.add(port)

pcb = UDPpcb()
split_layers(IP, UDP, proto = 17)
bind_layers(IP, UDPPacket, proto = 17)
# bind_layers(UDPPacket, IP)

# #
# private functions for layer
#
def _echoReply(gpacket):
    udp = gpacket.ip_payload.payload
    out_udp = UDPPacket(sport = udp.dport, dport = udp.sport, len = None, chksum = None)
    dip = "192.168.1.2"
    send_payload_to_ip(out_udp, dip, 17)

# #
# public functions
# MUST IMPLEMENT
def Protocol_Processor(meta_pkt):
    global pcb
    gpacket = GPacket(meta_pkt)
    print("gpacket: ", gpacket)
    udp_field = gpacket.packet.payload.payload
    udp_field.show()
    if udp_field.dport == 7:
        print("Receiving an Echo packet..")
        _echoReply(gpacket)
    elif udp_field.dport in pcb.port_set:
        # udp_field.show()
        print(udp_field.payload)
    else:
        print("Port Unreachable!")

def Command_Line(str):
    global pcb
    if pcb == None:
        pcb = UDPpcb()
    command_string = str.split(" ")
    if len(command_string) != 3:
        print('Command Error! "nc -l [port]" "nc [IP][port]"')
    elif command_string[1] == "-l":
        port_listen = int(command_string[2])
        pcb.listen(port_listen)
        print("listen to port", command_string[2], "...")
    else:
        dip_hl = command_string[1]
        dport = int(command_string[2])
        sport = 7777
        pcb.send(dip_hl, sport, dport)

def Config():
    print("[Config]")
    config = module_config(name="udp_scapy", protocol=17, command_string="nc", short_help="udp function",
                           usage="nc -l [port] nc [IP][port]",
                           long_help="sending and listening to udp packet")
    return config



