
import sys
import os.path
# sys.path.append('.')
# TODO: import POX.openflow.libopenflow_01
import pox.openflow.libopenflow_01 as of
from pox.core import core
import socket
import struct
import threading
import thread

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
        self.s.connect((addr, port))
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
            # print('2nd echo reply: ', struct.unpack('>bbhl',buff), 'len: ', len(buff))
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
        2.check socket communicating controller
    """
    def launch(self, addr = "127.0.0.1", port = 6633):
        self.connect_contoller(addr, port)
        #routine = threading(self.check_socket())
        #routine.start()
#        routine_print = threading(test())
        #routine_print.start()
        thread.start_new_thread(self.check_socket())
        # thread.start_new_thread(self.test,(1,2))
        print("routine thread created!")
        print("routine thread created!")
        print("routine thread created!")
        print("routine thread created!")
        print("routine thread created!")
        print("routine thread created!")
        print("routine thread created!")


gini_of_runable = gini_of()
#gini_of_runable.launch("127.0.0.1", 8899)
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
#build socket
# controller_ip_addr = "127.0.0.1"
# controller_port = 8899
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((controller_ip_addr, controller_port))
#
# # send a hello msg
# pkt_hello = of.ofp_hello()
# print(pkt_hello)
# s.send(pkt_hello.pack())
# print(struct.unpack('>bbhl', (pkt_hello.pack())), "pkt sent...1")
# print(pkt_hello.pack(), "pkt sent...2")
# buff = s.recv(8)
# print('recved: ', len(buff))
# print(buff, "rev hello pkt 1: len: ", len(buff))
# buff = s.recv(32)
# print('recved: ', len(buff))
# print(buff, "rev hello pkt 2: len: ", len(buff))
# buff = s.recv(32)
# print('recved: ', len(buff))
# print(buff, "rev hello pkt 3: len: ", len(buff))
# buff = s.recv(32)
# print('recved: ', len(buff))
# print(buff, "rev hello pkt 4: len: ", len(buff))
# buff = s.recv(32)
# print('recved: ', len(buff))
# print(buff, "rev hello pkt 5: len: ", len(buff))

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

# #send echo request
# pkt_echo_request = of.ofp_echo_request()
# s.send(pkt_echo_request.pack())
# buff = s.recv(32)
# print('recved: ', len(buff))
# print('1st echo reply: ', struct.unpack('>bbhl',buff), 'len: ', len(buff))
# #will recieve feature request
#
# #send feature_reply
# pkt_feature_reply = of.ofp_features_reply()
# pkt_feature_reply.datapath_id = 10
# # pkt_feature_reply.actions=
# s.send(pkt_feature_reply.pack())
# buff = s.recv(32)
# print('recved: ', len(buff))
# print('feature reply: ', struct.unpack('>bbhlbbbb',buff), 'len: ', len(buff))
#
# #send 2nd echo request
# pkt_echo_request = of.ofp_echo_request()
# s.send(pkt_echo_request.pack())
# buff = s.recv(32)
# print('recved: ', len(buff))
# print('2nd echo reply: ', struct.unpack('>bbhlddd',buff), 'len: ', len(buff))


#read
