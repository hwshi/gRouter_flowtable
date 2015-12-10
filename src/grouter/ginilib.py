__author__ = 'Haowei Shi'
import socket
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
    dip_n = ip_hton_str_to_list(dip_h_str)
    if dip_n != None:
        out_gpacket = GPacket()
        out_gpacket.ip_payload = ip_payload.build()
        # print("ready to send...ip_payload: ", out_gpacket.ip_payload)
        GINIC.IPOutgoingPacket(out_gpacket.build(), dip_n, len(ip_payload), 1, protocol) # 0 for old packet, 1 for new packet
def send_packet_to_ip():
    pass

# routing table API
def find_route(dip):
    if not validate_ip(dip):
        print("Not a valid IP")
    else:
        res = GINIC.findRoute(dip)
        if res != None:
            return res[0], res[1]
        else:
            return None, None
def add_route(network, netmask, next_hop, interface):
    if not validate_ip(network):
        print("Not a valid network  IP")
        return None
    if not validate_ip(netmask):
        print("Not a valid netmask IP")
        return None
    if not validate_ip(next_hop):
        print("Not a valid next_hop IP")
        return None
    # TODO validate interface
    GINIC.addRoute(network, netmask, next_hop, interface)
def show_route_talbe():
    GINIC.showRouteTable()

# utilities
def ip_hton_str_to_list(str):
    if not validate_ip(str):
        print("Not a valid IP.")
        return None
    else:
        list = str.split(".")
        ipn = struct.pack('BBBB', int(list[3]), int(list[2]), int(list[1]), int(list[0]))
        print("[stringToIP]ip is:", ipn)
        return ipn
def validate_ip(ip):
    nums = ip.split('.')
    if len(nums) != 4:
        return False
    for x in nums:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True