__author__ = 'Haowei Shi'
# using scapy: http://www.secdev.org/projects/scapy/
from scapy.all import *
from scapy.layers.inet import *
# gini C interfaces
import _GINIC as GINIC
class GFrame(object):
    name = "gHeader"
    def __init__(self, raw_frame):
        if raw_frame != None:
            #TODO parse gframe
            pass

class GPacket(object):
    name = "Gini Packet"
    def __init__(self, raw_packet=None): # TODO more methods
        if raw_packet == None:
            self.ip_payload = None
        else:
            self.ip_payload = GINIC.IPPayload(raw_packet)
            #test for bind
            # self.gframe = GFrame(GINIC.getGFrame(raw_packet)) #TODO implement GINIC.getGFrame(raw_packet)
            self.packet = Ether(GINIC.getGPacketString(raw_packet))
    def get_ip_layer(self):
        return self.packet.payload
    def get_ip_payload(self):
        return self.packet.payload.payload
    def build(self):
        raw_packet = GINIC.createGPacketWithIPPayload(self.ip_payload)
        return raw_packet
def module_config(name="module", protocol=255, command_string="",
                 short_help="", usage="", long_help=""):
    return (name, protocol, command_string,
                        short_help, usage, long_help)
# layers API
def send_payload_to_ip(ip_payload, dip_h_str, protocol):
    dip_n = IP_hton_str_to_list(dip_h_str)
    out_gpacket = GPacket()
    ip_payload.show2()
    out_gpacket.ip_payload = ip_payload.build()
    print("ready to send...ip_payload: ", out_gpacket.ip_payload)
    GINIC.IPOutgoingPacket(out_gpacket.build(), dip_n, len(ip_payload), 1, protocol) # 0 for old packet, 1 for new packet
def send_packet_to_ip():
    pass

# routing table API
def find_route(dip):
    res = GINIC.findRoute(dip)
    if res != None:
        return res[0], res[1]
    else:
        return None, None

def show_route_talbe():
    GINIC.showRouteTable()
# utilities
def IP_hton_str_to_list(str):
    list = str.split(".")
    ipn = struct.pack('BBBB', int(list[3]), int(list[2]), int(list[1]), int(list[0]))
    print("[stringToIP]ip is:", ipn)
    return ipn