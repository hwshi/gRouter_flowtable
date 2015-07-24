# giniof_01.py (the openflow module for gRouter)
# import to gRouter: > addprot giniof_01 python
# Author: Haowei Shi
# DATE: May 2015

import socket
import threading

# utils
import copy

# TODO: import POX.openflow.libopenflow_01
import pox.openflow.libopenflow_01 as of
import _GINIC
# try:
#     __import__('_GINIC')
# except ImportError:
#     print('Module _GINIC missing!')
# CONSTANT
def gini_get_device_name():
    print("[gini_get_device_name]")
    name = "aaaaaaaaaaaa"
    print("got name before: ", name)
    name =_GINIC.getDeviceName()
    print("got name done: ", name)
    return name

def gini_get_device_ports():
    port_list = []
    port_num = _GINIC.getPortNumber()
    print("[gini_get_device_ports]This device has %d ports", port_num)
    port_tuple_list = _GINIC.getPortTuple()
    print("[gini_get_device_ports]Done!!")
    for tp in port_tuple_list:
        print("tuple: ", tp)
        port = of.ofp_phy_port()
        port.port_no = tp[0]
        port.hw_addr = tp[1]
        port.name = tp[2]
        port_list.append(copy.deepcopy(port)) # stupid way??
    print("port list is: ", port_list)
    return port_list

class gini_of:
    NAME = "GINI RUNALBE"
    OFPT_HELLO = 0
    OFPT_ECHO_REQUEST = 2
    OFPT_ECHO_REPLY = 3
    OFPT_FEATURES_REQUEST = 5
    OFPT_FEATURES_REPLY = 6
    OFPT_SET_CONFIG = 9
    OFPT_SET_MOD = 14
    OFPT_BARRIER_REQUEST = 18

    def __init__(self,
                 s=socket.socket(socket.AF_INET, socket.SOCK_STREAM),
                 queue=None,
                 ):
        self.queue_map = {}
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("gini_of initiate")

    def connect_contoller(self, addr="127.0.0.1", port=6633):
        try:
            self.s.connect((addr, port))
        except Exception, e:
            print('Failed connection to %s : %d') % (addr, port)
            exit(1)
            # TODO: except? timeout?


    def process_hello(self, pkt):
        print("This is a [Hello packet]")
        pkt_hello = of.ofp_hello()
        pkt_hello.xid = 9999
        self.s.send(pkt_hello.pack())
        print("hello pkt sent...", pkt_hello.pack())

    def process_echo_request(self, pkt):
        print("This is a [Echo request packet]")
        pkt_echo_reply = of.ofp_echo_reply()
        self.s.send(pkt_echo_reply.pack())
    # TODO: 1.get MAC ADDR from gini_c 2.set pkt.ports
    def process_features_request(self, pkt):
        print("This is a [Features reuqest packet]")
        pkt_features_reply = of.ofp_features_reply()  # set fields
        pkt_features_reply.xid = pkt.xid  # same xid
        device_name = gini_get_device_name() #TODO(DONE): returns a string for name eg. "003de70fc98a"
        ports = gini_get_device_ports()
        pkt_features_reply.datapath_id = int(device_name, 16) # [16bit: USER DEFIN |48bit: MAC ADDRESS]
        pkt_features_reply.n_buffers = 0
        pkt_features_reply.n_tables = 0
        pkt_features_reply.capabilities = 0
        pkt_features_reply.actions = 0
        pkt_features_reply.ports = []  # set the list of ports
        self.s.send(pkt_features_reply.pack())

    def process_set_config(self, pkt):
        print("This is a [set config packet]")
        pkt_echo_reply = of.ofp_echo_reply()
        self.s.send(pkt_echo_reply.pack())


    def process_set_mod(self, pkt):
        print("This is a [set mod packet]")
        pkt_echo_reply = of.ofp_echo_reply()
        self.s.send(pkt_echo_reply.pack())

    def process_barrier_request(self, pkt):
        print("This is a [barrier request packet]")
        pkt_barrier_reply = of.ofp_barrier_reply()
        pkt_barrier_reply.xid = pkt.xid
        self.s.send(pkt_barrier_reply.pack())
    def test(self, a, b):
        print("this is a test!")


    def check_socket(self):
        while True:
            buff = self.s.recv(100)
            pkt = of.ofp_header()
            pkt.unpack(buff)
            print('[check_socket]recved: ', len(buff))
            print(pkt.show())
            if pkt.header_type == gini_of.OFPT_HELLO:  # OFPT_HELLO
                print("OFPT_HELLO msg: ")
                self.process_hello(pkt)
            elif pkt.header_type == gini_of.OFPT_ECHO_REQUEST:
                print("OFPT_ECHO_REPLY msg: ")
                self.process_echo_request(pkt)
            elif pkt.header_type == gini_of.OFPT_FEATURES_REQUEST:
                print("OFPT_FEATURES_REQUEST msg: ")
                self.process_features_request(pkt)
            elif pkt.header_type == gini_of.OFPT_SET_CONFIG:
                print("OFPT_SET_CONFIG msg: ")
                self.process_set_config(pkt)
            elif pkt.header_type == gini_of.OFPT_SET_MOD:
                print("OFPT_SET_MOD msg: ")
                self.process_set_mod(pkt)
            elif pkt.header_type == gini_of.OFPT_BARRIER_REQUEST:
                print("OFPT_BARRIER_REQUEST msg: ")
                self.process_barrier_request(pkt)
            else:
                print("Unknown type!: ", pkt.header_type, "details: ")
                print(pkt.show())

    """
    create threads:
        1.process packet from gRouter
        2.check socket which is communicating controller
    """


    def launch(self, addr="127.0.0.1", port=6633):
        self.connect_contoller(addr, port)
        # routine_check_socket = threading.Thread(target=self.check_socket)  # self.check_socket()  Wrong!!!
        # try:
        #     routine_check_socket.start()
        # except:
        #     print('Cannot start routine_check_socket!')
        self.check_socket()


gini_of_runable = gini_of()
gini_of_runable.launch("127.0.0.1", 8899)
print("gini_of_runable lanched!")



# Interface functions
def Protocol_Processor(packet):
    print("receive an Openflow packet from Ginic...")
    global gini_of_runable
    print("Process_OpenflowPkt", gini_of_runable.NAME)
    print("[Process_OpenflowPkt] packet: ", packet)
    # gini_of_runable.launch("127.0.0.1", 8899)
    #   gini_of_runable.process_packet(packet)
    # process_packet not done


def Command_Line(str):
    print("Command for giniof_01", str)


def Config():
    return "of"


# --read socket with count
# count = 1
# while True:
# try:
#         buff = s.recv(32)
#     except socket.errno, e:
#         print("exception")
#         err = e.args[0]
#         if err == socket.errno.EAGAIN or err == socket.errno.EWOULDBLOCK:
#             print("No data")
#             break
#     print('recved: ', len(buff))
#     print(buff, "rev hello pkt", count, ": len: ", len(buff))
#     count += 1
#         break
#
# if buff:
#     print('recved: ', len(buff))
#     print(buff, "rev hello pkt", count, ": len: ", len(buff))
#     count += 1
# else:
#     print("socket is empty")
#     break

