__author__ = 'chi'

from scapy.all import *
from scapy.layers.inet import *
import _GINIC as GINIC

class GPacket(object):
    name = "Gini Packet"
    def __init__(self, meta_packet=None):
        # self.gheader = gheader
        # self.packet = Ether(GINIC.getGPacketString(meta_packet))
        if meta_packet == None:
            self.ip_payload = None
        else:
            self.ip_payload = GINIC.IPPayload(meta_packet)

    #
    # def _dissemble(self, msg):
    #     self.ip_payload = GINIC.IPPayload(msg)
    #     self.meta_msg = GINIC.getGPacketString(msg)
    #     repr(self.meta_msg)
    # def _assemble(self):
    #     header_size = GINIC.getGPacketMetaheaderLen()
    #     self.__packed = ''
    #     if self.meta_msg == None:
    #         return GINIC.createGPacketWithIPPayload(self.ip_payload)
    #     else:
    #         return GINIC.assembleWithIPPayload(self.meta_msg, self.ip_payload);
    def build(self):
        raw_packet = GINIC.createGPacketWithIPPayload(self.ip_payload)
        return raw_packet
def send2IP(ip_payload, dip_h_str, protocol):
    dip_n = htonStringToIP(dip_h_str)
    print("[send2IP]sending to dest ip:", dip_n)
    out_gpacket = GPacket()
    out_gpacket.ip_payload = ip_payload.build()

    print("ready to send...ip_payload: ", out_gpacket.ip_payload)
    GINIC.IPOutgoingPacket(out_gpacket.build(), dip_n, len(ip_payload) + 8, 1, protocol) # 0 for old packet, 1 for new packet
def htonStringToIP(str):
    list = str.split(".")
    ipn = struct.pack('BBBB', int(list[3]), int(list[2]), int(list[1]), int(list[0]))
    print("[stringToIP]ip is:", ipn)
    return ipn

    #
    # meta_udp_pkt = assemble(udp_packet)
    # size = len(meta_udp_pkt)
    # print("[_udp_echo_reply]sending to %s : %d", dest_ip, udp_packet.dport)
    # gpacket.ip_payload = meta_udp_pkt
    # GINIC.IPOutgoingPacket(gpacket._assemble(), dest_ip, size, newflag, prot)
# class module_config:
#     def __init__(self, name="module", protocol=255, command_string="",
#                  short_help="", usage="", long_help=""):
#         self.name = name
#         self.protocol = protocol
#         self.command_string = command_string
#         self.short_help = short_help
#         self.usage = usage
#         self.long_help = long_help
#
#     def to_tuple(self):
#         config_tuple = (self.name, self.protocol, self.command_string,
#                         self.short_help, self.usage, self.long_help);
#         return config_tuple
def module_config(name="module", protocol=255, command_string="",
                 short_help="", usage="", long_help=""):
    return (name, protocol, command_string,
                        short_help, usage, long_help)