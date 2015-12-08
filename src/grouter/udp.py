# #
# udp.py
# module
# AUTHOR: Haowei Shi class "Packt" is from pyip http://sourceforge.net/projects/pyip/
# DATE: Jan 01, 2015
# #

from random import randint
import inspect
import array
import struct
#import GINIC
import _GINIC as GINIC

MAX_PCB_NUMBER = 5
MAX_BUFFER_SIZE = 5


class UDPPcbEntry:
    def __init__(self,
                 sport=-1,
                 dport=-1):
        self.sport = sport
        self.dport = dport
        self.buff = []


class UDPPcb:
    def __init__(self,
                 size=0):
        self.size = size
        self.entry = [UDPPcbEntry() for i in range(5)]
        self.port_dict = {}

    def bind(self, dport):
        sport = 8888
        if self.port_dict.has_key(sport):
            sport = randint(7000, 9000)
        for id in range(MAX_PCB_NUMBER):
            if self.entry[id].sport == -1:
                self.port_dict[sport] = id
                self.entry[id].sport = sport
                self.entry[id].dport = dport
                return id
        gprint("bind failed! Not enough space")
        return -1

    def check(self, dport):
        print("[check]dict: ", self.port_dict)
        if dport in self.port_dict:
            print("dport in self.port_dict")
        if self.port_dict.has_key(dport):
            print("[check]found port", dport, " in port_dict!")
            return self.port_dict[dport]
        else:
            print("[check]Didn't find port", dport, " in port_dict!")
            return -1

    def unbind(self, port):
        for check in range(MAX_PCB_NUMBER):
            if self.entry[check].port == port:
                self.entry[check].port = -1
                return True
        gprint("unbind failed! port invalid!")

    def send(self, diph_l, sport, dport):
        print("[UDPPcb.send] input your msg")
        dipn = struct.pack('BBBB', int(diph_l[3]), int(diph_l[2]), int(diph_l[1]), int(diph_l[0]))
        while True:
            str = raw_input()
            udp_pkt = Packet(sport, dport, len(str), 0, str)
            upkt_a = assemble(udp_pkt, 0)  # disable checksum
            gpacket = GPacket()
            gpacket.ip_payload = upkt_a
            print(upkt_a)
            GINIC.IPOutgoingPacket(gpacket._assemble(), dipn, len(upkt_a), 1, 17)
    def listen(self, port):
        if self.port_dict.has_key(port):
            print("listen failed! port in use!")
            return
        else:
            for id in range(MAX_PCB_NUMBER):
                if self.entry[id].sport == -1:
                    self.port_dict[port] = id
                    self.entry[id].sport = port
                    self.entry[id].dport = -1
                    return


print("--    SIMPLE UDP IMPLEMENTATION FOR GINI    --")
pcb = UDPPcb()


class module_config:
    def __init__(self, name="module", protocol=255, command_string="",
                 short_help="", usage="", long_help=""):
        self.name = name
        self.protocol = protocol
        self.command_string = command_string
        self.short_help = short_help
        self.usage = usage
        self.long_help = long_help

    def to_tuple(self):
        config_tuple = (self.name, self.protocol, self.command_string,
                        self.short_help, self.usage, self.long_help)
        return config_tuple


def Config():
    config = module_config(name="udp", protocol=17, command_string="nc", short_help="udp function",
                           usage="nc -l [port] nc [IP][port]",
                           long_help="sending and listening to udp packet")
    return config.to_tuple()


def Command_Line(str):
    global pcb
    if pcb == None:
        pcb = UDPPcb()
    command_string = str.split(" ")
    if len(command_string) != 3:
        print('Command Error! "nc -l [port]" "nc [IP][port]"')
    elif command_string[1] == "-l":
        port_listen = int(command_string[2])
        pcb.listen(port_listen)
        print("listen to port", command_string[2], "...")
    else:
        dip_hl = command_string[1].split(".")
        dport = int(command_string[2])
        if is_dip_hl(dip_hl) and is_port(dport):
            id = pcb.bind(dport)
            pcb.send(dip_hl, pcb.entry[id].sport, dport)
        else:
            print("invalid IP or PORT!")


def Protocol_Processor(meta_gpkt):
    global pcb
    print("[Protocol_Processor - UDP]...")
    print(pcb.port_dict)
    if pcb is None:
        pcb = UDPPcb()
    # ip_playload = GINIC.IPPayload(gpkt)  # g_header is lost here... need to save if somewhere?
    gpacket = GPacket()
    gpacket._dissemble(meta_gpkt)
    udp_packet = disassemble(gpacket.ip_payload, 1)
    print(udp_packet)
    if udp_packet.dport == 7:
        print("recieved an UDP ECHO packet")
        _udp_echo_reply(udp_packet)
        dest_ip = [8, 9, 168, 192]
        # dest_ip = __find_dest_ip(packet)  #TODO extract dest_ip from packet
        print("[_udp_echo_reply]dest ip: %d", dest_ip)
        newflag = 0
        prot = 17
        meta_udp_pkt = assemble(udp_packet)
        size = len(meta_udp_pkt)
        print("[_udp_echo_reply]sending to %s : %d", dest_ip, udp_packet.dport)
        gpacket.ip_payload = meta_udp_pkt
        GINIC.IPOutgoingPacket(gpacket._assemble(), dest_ip, size, newflag, prot)
    elif pcb.check(udp_packet.dport) != -1:
        print("Received Msg: ", udp_packet.data)
        pass
    else:
        print("Port Unreachable!")


def _udp_echo_reply(packet):
    port_tmp = packet.sport
    packet.sport = packet.dport
    packet.dport = port_tmp

class GPacket:
    def __init__(self,
                 ip_payload=None):
        # self.meta_msg = None
        self.ip_payload = ip_payload

    def _dissemble(self, msg):
        self.ip_payload = GINIC.IPPayload(msg)
        self.meta_msg = GINIC.getGPacketString(msg)
        repr(self.meta_msg)
    def _assemble(self):
        header_size = GINIC.getGPacketMetaheaderLen()
        self.__packed = ''
        if self.meta_msg == None:
            return GINIC.createGPacketWithIPPayload(self.ip_payload)
        else:
            return GINIC.assembleWithIPPayload(self.meta_msg, self.ip_payload);

class Packet:
    def __init__(self,
                 sport=0,
                 dport=0,
                 ulen=8,
                 sum=0,
                 data=''):
        self.sport = sport
        self.dport = dport
        self.ulen = ulen
        self.sum = sum
        self.data = data

    def __repr__(self):
        begin = "<UDP %d->%d len=%d " % (self.sport, self.dport, self.ulen)
        if self.ulen == 8:
            rep = begin + "\'\'>"
        elif self.ulen < 18:
            rep = begin + "%s>" % repr(self.data)
        else:
            rep = begin + "%s>" % repr(self.data[:10] + '...')
        return rep

    def __eq__(self, other):
        if not isinstance(other, Packet):
            return 0
        return self.sport == other.sport and \
               self.dport == other.dport and \
               self.ulen == other.ulen and \
               self.sum == other.sum and \
               self.data == other.data

    def _assemble(self, cksum=1):
        self.ulen = 8 + len(self.data)
        src_ip = ip_ltostr([128, 1, 168, 192])
        dest_ip = ip_ltostr([2, 1, 168, 192])
        begin = struct.pack('HHH', self.sport, self.dport, self.ulen)
        pseudo_header = src_ip + dest_ip + '\000\000' + struct.pack('H', self.ulen)
        pseudo_packet = pseudo_header + begin + '\000\000' + self.data
        if cksum:
            self.sum = udpcksum(pseudo_packet)
            #self.sum = udpchecksum(packet)
            packet = begin + struct.pack('H', self.sum) + self.data
        else:
            self.sum = 0
            packet = begin + struct.pack('H', self.sum) + self.data
        self.__packet = udph2net(packet)
        return self.__packet

    def _disassemble(self, raw_packet, cksum=1):
        packet = net2updh(raw_packet)
        if cksum and packet[6:8] != '\000\000':
            our_cksum = udpcksum(packet)
            # no check sum
            # if our_cksum != 0:
            #      print("[_disassemble]Check sum invalid!!")
            #      raise ValueError, packet
        elts = map(lambda x: x & 0xffff, struct.unpack('HHHH', packet[:8]))
        [self.sport, self.dport, self.ulen, self.sum] = elts
        #tail = self.ulen# Haowei
        self.data = packet[8:self.ulen]


def assemble(packet, cksum=1):
    return packet._assemble(cksum)


def disassemble(buffer, cksum=1):
    packet = Packet()
    packet._disassemble(buffer, cksum)
    return packet


def gprint(str):
    print(inspect.stack()[0][3] + "::" + str)


def is_port(data):
    return data >= 0


def is_dip_hl(data):
    return len(data) == 4 and \
           is_uchar(int(data[0])) and \
           is_uchar(int(data[1])) and \
           is_uchar(int(data[2])) and \
           is_uchar(int(data[3]))


def is_uchar(num):
    return num >= 0 and num <= 255


def ip_ltostr(iplist):
    return struct.pack('BBBB', iplist[0], iplist[1], iplist[2], iplist[3])


def __find_dest_ip(pkt):
    ip = [2, 1, 168, 192]
    ipstr = ip_ltostr(ip)
    # print("[__find_dest_ip]len(ipstr) = %d") % len(ipstr)
    # print("[__find_dest_ip]lip after ltostr:", ipstr)
    return ipstr


def __ntohs(s):
    return struct.pack('H', struct.unpack('!H', s)[0])


def __htons(s):
    return struct.pack('!H', struct.unpack('H', s)[0])


def iph2net(s):
    return s[:2] + __htons(s[2:4]) + __htons(s[4:6]) + __htons(s[6:8]) + s[8:]


def net2iph(s):
    return s[:2] + __ntohs(s[2:4]) + __ntohs(s[4:6]) + __ntohs(s[6:8]) + s[8:]


def udph2net(s):
    return __htons(s[0:2]) + __htons(s[2:4]) + __htons(s[4:6]) + s[6:]


def net2updh(s):
    return __ntohs(s[0:2]) + __ntohs(s[2:4]) + __ntohs(s[4:6]) + s[6:]


def udpcksum(s):
    if len(s) & 1:
        s = s + '\0'
    words = array.array('h', s)
    sum = 0
    for word in words:
        sum = sum + (word & 0xffff)
    hi = sum >> 16
    lo = sum & 0xffff
    sum = hi + lo
    sum = sum + (sum >> 16)
    print("checksum is : %s") % ((~sum) & 0xffff)
    return (~sum) & 0xffff


HDR_SIZE_IN_BYTES = 8