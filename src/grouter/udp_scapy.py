__author__ = 'chi'

# import _GINIC as GINIC

from ginilib import *

print("--    SIMPLE UDP IMPLEMENTATION FOR GINI    --")
UDP_SERVICES=load_services("/etc/services")
class UDPPacket(Packet):
    name = "UDPPacket"
    fields_desc = [ ShortEnumField("sport", 53, {8888 : "test", 7 : "echo"}),
                    ShortEnumField("dport", 53, {8888 : "test", 7 : "echo"}),
                    ShortField("len", None),
                    XShortField("chksum", None), ]
# class UDPPacket(UDP):
#     pass

class UDPpcb(object):
    def __init__(self):
        self.port_set = set()
    def send(self, dip, sp, dp):
        print("[UDPPcb.send] input your msg")
        # dipn = struct.pack('BBBB', int(diph_l[3]), int(diph_l[2]), int(diph_l[1]), int(diph_l[0]))
        while True:
            str = raw_input()
            # udp_pkt = Packet(sport, dport, len(str), 0, str)
            packet = UDPPacket(sport = sp, dport = dp, len  = len(str))
            packet.payload = str
            hexdump(packet)
            send2IP(packet, dip, 17)
            # upkt_a = assemble(udp_pkt, 0)  # disable checksum
            # gpacket = GPacket()
            # gpacket.ip_payload = upkt_a
            # print(upkt_a)
            # GINIC.IPOutgoingPacket(gpacket._assemble(), dipn, len(upkt_a), 1, 17)
    def listen(self, port):
        self.port_set.add(port)

pcb = UDPpcb()


# #
# private functions
#
def _echoReply(gpacket):
    udp = gpacket.ip_payload.payload
    out_udp = UDPPacket(sport = udp.dport, dport = udp.sport, len = 0, chksum = None)
    # dip_n = [8, 9, 168, 192]
    dip = "192.168.1.2"
    send2IP(out_udp, dip, 17)

    # dest_ip = __find_dest_ip(packet)  #TODO extract dest_ip from packet
    # print("[_udp_echo_reply]dest ip: %d", dest_ip)
    # newflag = 0
    # prot = 17
    # meta_udp_pkt = assemble(udp_packet)
    # size = len(meta_udp_pkt)
    # print("[_udp_echo_reply]sending to %s : %d", dest_ip, udp_packet.dport)
    # gpacket.ip_payload = meta_udp_pkt
    # GINIC.IPOutgoingPacket(gpacket._assemble(), dest_ip, size, newflag, prot)

# #
# public functions
#
def Protocol_Processor(meta_pkt):
    global pcb
    gpacket = GPacket(meta_pkt)
    print("gpacket: ", gpacket)
    # print("packet.payload", gpacket.packet.payload.payload)
    udp_field = UDPPacket(gpacket.ip_payload)
    print("gpacket.ip_payload: ", gpacket.ip_payload)
    if udp_field.dport == 7:
        print("Receiving an Echo packet..")
        _echoReply(gpacket)
    elif udp_field.dport in pcb.port_set:
        hexdump(udp_field)
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



