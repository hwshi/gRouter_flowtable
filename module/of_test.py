# giniof_01.py (the openflow module for gRouter)
# import to gRouter: > addprot giniof_01 python
# Author: Haowei Shi
# DATE: May 2015

import socket
import threading
import struct

#utilities
import copy

# pox libraries
import pox.openflow.libopenflow_01 as of
try:
    __import__('_GINIC')
    _gini_error = 0
except ImportError:
    _gini_error = 1
    print('Module _GINIC missing!')


def gini_get_device_name():
    print("[gini_get_device_name]")
    name = ""
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

def gini_ofp_flow_mod(pkt):
    #TODO: parse the pkt and send modification command to flow table(in GINI)

    return True



class gini_of:
    NAME = "GINI RUNALBE"
    OFPT_HELLO = 0
    OFPT_ECHO_REQUEST = 2
    OFPT_ECHO_REPLY = 3
    OFPT_FEATURES_REQUEST = 5
    OFPT_FEATURES_REPLY = 6
    OFPT_SET_CONFIG = 9
    OFPT_FLOW_MOD = 14
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
        if _gini_error == 1:
            device_name = "cccccccccccc"
            ports = []
        else:
            device_name = gini_get_device_name() # returns a string for name eg. "003de70fc98a"
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
        print(pkt.show())
        #TODO: miss_send_len is received
        pkt_echo_rep = of.ofp_echo_reply()
        self.s.send(pkt_echo_rep.pack()) # TODO: not need. But cant connect when missing....
        print("[process_set_config] done")

    # TODO: huge work here ...
    def process_flow_mod(self, pkt):
        print("This is a [flow mod packet]")
        print(pkt.show())
        pkt_echo_reply = of.ofp_echo_reply() #???
        self.s.send(pkt_echo_reply.pack())  #???

        if gini_ofp_flow_mod(pkt) == True:
            print('flow mod succesful!')
        print("[process_set_mod] sent")

    def process_barrier_request(self, pkt):
        print("This is a [barrier request packet]")
        pkt_barrier_reply = of.ofp_barrier_reply()
        pkt_barrier_reply.xid = pkt.xid
        self.s.send(pkt_barrier_reply.pack())
        print("[process_barrier_request] sent")

    def test(self, a, b):
        print("this is a test!")


    def check_socket(self):
        pkt_count = 0
        while True:
            pkt_count += 1
            buff = self.s.recv(100)
            pkt = of.ofp_header()
            pkt.unpack(buff)
            #print('[{}][check_socket]recved: ', len(buff))
            print('\n[{0}] received [{1}]byte data.'.format(pkt_count, len(buff)))
            print(pkt.show())
            if pkt.header_type == gini_of.OFPT_HELLO:  # OFPT_HELLO
                print("OFPT_HELLO msg: ")
                pkt = of.ofp_hello()
                pkt.unpack(buff)
                self.process_hello(pkt)
            elif pkt.header_type == gini_of.OFPT_ECHO_REQUEST:
                print("OFPT_ECHO_REPLY msg: ")
                pkt = of.ofp_echo_request()
                pkt.unpack(buff)
                self.process_echo_request(pkt)
            elif pkt.header_type == gini_of.OFPT_FEATURES_REQUEST:
                print("OFPT_FEATURES_REQUEST msg: ")
                pkt = of.ofp_features_request()
                pkt.unpack(buff)
                self.process_features_request(pkt)
            elif pkt.header_type == gini_of.OFPT_SET_CONFIG:
                print("OFPT_SET_CONFIG msg: ")
                pkt = of.ofp_set_config()
                pkt.unpack(buff)
                self.process_set_config(pkt)
            elif pkt.header_type == gini_of.OFPT_FLOW_MOD:
                print("OFPT_FLOW_MOD msg: ")
                pkt = of.ofp_flow_mod()
                pkt.unpack(buff)
                self.process_flow_mod(pkt)
            elif pkt.header_type == gini_of.OFPT_BARRIER_REQUEST:
                print("OFPT_BARRIER_REQUEST msg: ")
                pkt = of.ofp_barrier_request()
                pkt.unpack(buff)
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

# test area:
#
# gini_of_runable.process_features_request(of.ofp_features_request())

