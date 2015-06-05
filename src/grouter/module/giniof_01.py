# giniof_01.py (the openflow module for gRouter)
# import to gRouter: > addprot giniof_01 python
# Author: Haowei Shi
# DATE: May 2015

import socket
import threading

# TODO: import POX.openflow.libopenflow_01
import pox.openflow.libopenflow_01 as of

try:
    __import__('_GINIC')
except ImportError:
    print('Module _GINIC missing!')
# CONSTANT

class gini_of:
    NAME = "GINI RUNALBE"
    OFPT_HELLO = 0
    OFPT_ECHO_REQUEST = 2
    OFPT_ECHO_REPLY = 3
    OFPT_FEATURES_REQUEST = 5
    OFPT_FEATURES_REPLY = 6
    def __init__(self,
                 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM),
                 queue = None,
                 ):
        self.queue_map = {}
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("gini_of initiate")
    def connect_contoller(self, addr = "127.0.0.1", port = 6633):
        try:
            self.s.connect((addr, port))
        except Exception, e:
            print('Failed connection to %s : %d') % (addr, port)
            exit(1)
        # TODO: except? timeout?


    def process_hello(self, pkt):
        pkt_hello = of.ofp_hello()
        self.s.send(pkt_hello.pack())
        print("hello pkt sent...", pkt_hello.pack())
    def process_echo_request(self, pkt):
        pkt_echo_reply = of.ofp_echo_reply()
        self.s.send(pkt_echo_reply)
    def process_features_request(self, pkt):
        pkt_echo_reply = of.ofp_features_reply()
        # set fields
        self.s.send(pkt_echo_reply.pack())
    def test(self, a, b):
        print("this is a test!")
    def check_socket(self):
        while True:
            buff = self.s.recv(100)
            pkt = of.ofp_header()
            pkt.unpack(buff)
            print('recved: ', len(buff))
            print(pkt.show())
            if pkt.header_type == gini_of.OFPT_HELLO: # OFPT_HELLO
                print("OFPT_HELLO msg: ")
                self.process_hello(pkt)
            if pkt.header_type == gini_of.OFPT_ECHO_REQUEST:
                print("OFPT_ECHO_REPLY msg: ")
                self.process_echo_request(pkt)
            if pkt.header_type == gini_of.OFPT_FEATURES_REQUEST:
                print("OFPT_FEATURES_REQUEST msg: ")
                self.process_features_request(pkt)
            else:
                print("Unknown type!: ", pkt.header_type)
    """
    create threads:
        1.process packet from gRouter
        2.check socket which is communicating controller
    """
    def launch(self, addr = "127.0.0.1", port = 6633):
        self.connect_contoller(addr, port)
        routine_check_socket = threading.Thread(target = self.check_socket) # self.check_socket()  Wrong!!!
        try:
            routine_check_socket.start()
        except:
            print('Cannot start routine_check_socket!')

gini_of_runable = gini_of()
gini_of_runable.launch("127.0.0.1", 8899)
print("gini_of_runable lanched!")

def Protocol_Processor(packet):
    global gini_of_runable
    print("Process_OpenflowPkt", gini_of_runable.NAME)
    print("[Process_OpenflowPkt] packet: ", packet)
    gini_of_runable.launch("127.0.0.1", 8899)

def Command_Line(str):
    print("Command for giniof_01", str)

def Config():
    return "of"


# --read socket with count
# count = 1
# while True:
#     try:
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

