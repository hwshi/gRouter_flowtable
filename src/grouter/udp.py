#module_name, package_name, ClassName, method_name, 
#ExceptionName, function_name, GLOBAL_VAR_NAME, 
#instance_var_name, function_parameter_name, local_var_name.


import _GINIC#,Cmessage,Csimplequeue
import inspect
import struct
import string
import array
from socket import htons, ntohs
import time
from threading import Thread
import thread
import os
#,Cmessage
# PCB set2q1
# class PCBCore:
# 	print("PCBCore is initilizing...")
# 	NAME = 'PCB CORE'
# 	MAX_PCB_NUMBER = 20
# 	MAX_PORT_NUMBER = 65536
# 	MAX_BUFFER_SIZE = 1000
# 	socket_count = 0
# 	PCB_dict = {} #{port: (pkt1, pkt2, ...)}
# 	#lock = thread.allocate_lock()
# 	#print(lock)
# 	print("PCBCore is initilaized")
# 	@staticmethod
# 	def pcb_bind_socket(port):
# 		if PCBCore.socket_count == PCBCore.MAX_PCB_NUMBER:
# 			print("Fail! Cannot have more sockets!")
# 			return
# 		if PCBCore.socket_count ==  PCBCore.MAX_PORT_NUMBER:
# 			print("Fail! Port number invalid")
# 			return
# 		if PCBCore.PCB_dict.has_key(port):
# 			print("Fail! Port already binded!")
# 			return
# 		PCBCore.PCB_dict.update({port : []})
# 		print("Socket binded!")

# 	@staticmethod
# 	def pcb_close_socket(port):
# 		#PCBCore.lock.acquire()
# 		if PCBCore.PCB_dict.has_key(port):
# 			##PCBCore.lock.acquire()
# 			del PCBCore.PCB_dict[port]
# 			PCBCore.socket_count = PCBCore.socket_count - 1
# 			#PCBCore.lock.release()
# 		else:
# 			#PCBCore.lock.release()
# 			print("Socket doesn't exist!")

# 	@staticmethod
# 	def recv_packet(pkt):
# 		print("[recv_packet] 1")
# 		port = pkt.dport
# 		print("[recv_packet] testing PCB_dict")
# 		#PCBCore.lock.acquire()
# 		if PCBCore.PCB_dict.has_key(port):
# 			print("[recv_packet] 2")
# 			new_value = PCBCore.PCB_dict[port].append(pkt)
# 			PCBCore.PCB_dict.update({port: new_value})
# 		print("[recv_packet] Done")
# 		#PCBCore.lock.release()

# 	@staticmethod
# 	def pcb_get_packet(port):
# 		print("[pcb_get_packet] 1")
# 		#PCBCore.lock.acquire()
# 		print("[pcb_get_packet] locked")
# 		if len(PCBCore.PCB_dict[port]) > 0:
# 			print("Found pkt")
# 			pkt = PCBCore.PCB_dict[port].pop(0)
# 			print("[pcb_get_packet] Done")
# 			#PCBCore.lock.release()
# 			return pkt
# 		else:
# 			print ""
# 			#PCBCore.lock.release()
# 	@staticmethod
# 	def get_name():
# 		print("[get_name]: %s") % PCBCore.NAME
		
# PCB
# class PCB:

# 	def __init__(self, gpacket):
# 		self.sport = gpacket.sport
# 		self.dport = gpacket.dport
# 		self.data = gpacket.data
class Ncer:

	def __init__(self):
		print("Init: NC")
		self.port = 777

	def ncCmdPy():	
		# Cip.cvar.PCB = [1, 2]
		print("[ncCmdPy] UDPPCB: %d, %d") % (UDPPCB.a, UDPPCB.b)

	def _recv_from(self):
		print("Ncer:[_recv_from] 1")
		pkt = PCBCore.pcb_get_packet(self.port)
		print(">>>")
		print(pkt)
	def thread_recv_from(self):
		#PCBCore.pcb_close_socket(self.port)
		PCBCore.pcb_bind_socket(self.port)
		print("creating thread")
		while True:
			Thread(target = self._recv_from).start()
			time.sleep(3)
		print("[thread_recv_from] closing socket")
		PCBCore.pcb_close_socket(self.port)
			

def ncCmdPy():
	print("[ncCmdPy]:: UDP sever/client::")
	print("call with 'nc -u -l port/nc -u ip port'")
	#print("???")
	nc = Ncer()
	print("listening...")
	#print(PCBCore.MAX_BUFFER_SIZE)
	PCBCore.get_name()
	#print(nc)
	PCBCore.NAME = "ncCmdPyed!"
	#nc.thread_recv_from()
def Protocol_Processor(gpkt):
	print("=====Py#[Packet_Processor]::=====")
	print("[UDPPacketProcess]Process ID: %d") % os.getpid();
	print("ready")
	print(gpkt)
	print("dir:")
	print(dir(gpkt))
	udpPacketFromC = GINIC.getUDPPacketString(gpkt)
	packet = disassemble(udpPacketFromC, 1)
	print(packet)
	if packet.dport == 7:
		print("recieved an UDP ECHO packet")
		_udp_echo_reply(packet)
	print("Done")

def UDPPacketProcess(gpkt):
	print("[UDPPacketProcess]Process ID: %d") % os.getpid();
	print("[UDPPacketProcess]::")
	PCBCore.get_name() 
	PCBCore.NAME = "Processed!"
	msg = Cip.getUDPPacketString(gpkt)
	packet = disassemble(msg,1)
	print("packet::")
	print(packet)
	#echo msg
	if packet.dport == 7:
		print("recieved an echo packet from %d")
		_udp_echo_reply(packet)
		# thread_reply_echo = Thread(target = _udp_echo_reply, args = (packet, ))
		# thread_reply_echo.start()
		
	else:
		#Thread(target = _UDPPacketProcess, args = (packet, )).start()
		print("[UDPPacketProcess] Recieved")
def _udp_echo_reply(packet):
	#TODO: should use route table
	print("in _udp_echo")
	print(packet.__class__)
	port_tmp = packet.sport
	packet.sport = packet.dport
	packet.dport = port_tmp
	print("get source ip")
	dest_ip = __find_dest_ip(packet)
	print(dest_ip)
	newflag = 1
	prot = 17
	print("prepare for assembling")
	pkt = assemble(packet)
	size = len(pkt)
	print("sending to %s : %d") % (dest_ip, packet.dport)
	print("udppkt size: %d") % (len(pkt))
	udp2gpkt = pkt #process udp2gpkt in typemap
	print("Start to send back to C")
	#Cip.IPOutgoingPacket(udp2gpkt, dest_ip, size, newflag, prot)


def _UDPPacketProcess(packet):
	print("[_UDPPacketProcess] Thread")
	PCBCore.recv_packet(packet)	
def ip_ltostr(iplist):
	return struct.pack('BBBB', iplist[0], iplist[1], iplist[2], iplist[3])

def __find_dest_ip(pkt):
	ip = [2, 1, 168, 192]
	#return " ".join(str(x) for x in ip)
	ipstr = ip_ltostr(ip)
	print("len(ipstr) = %d") % len(ipstr)
	return ipstr




def __ntohs(s):
	print("in ntohs")
	return struct.pack('H', struct.unpack('!H', s)[0])
def __htons(s):
	return struct.pack('!H', struct.unpack('H', s)[0])
# def iph2net(s):
# 	return s[:2] + __htons(s[2:4]) + __htons(s[4:6]) + __htons(s[6:8]) + s[8:]

# def net2iph(s):
# 	return s[:2] + __ntohs(s[2:4]) + __ntohs(s[4:6]) + __ntohs(s[6:8]) + s[8:]

def udph2net(s):
	print("[udp2net]")
	return __htons(s[0:2]) + __htons(s[2:4]) + __htons(s[4:6]) + s[6:]

def net2updh(s):
	print("in net2udph")
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
	#print("chsum>>end")
	return (~sum) & 0xffff

HDR_SIZE_IN_BYTES = 8

class Packet:

	def __init__(self,
				 sport = 0,
				 dport = 0,
				 ulen = 8,
				 sum = 0,
				 data = ''):
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
		begin = struct.pack('HHH', self.sport, self.dport, self.ulen)
		packet = begin + '\000\000' + self.data
		print("[_assemble]")
		if cksum:
			print("[_assemble] 1")
			self.sum = udpcksum(packet)
			print("[_assemble] 2")
			packet = begin + struct.pack('H', self.sum) + self.data
		self.__packet = udph2net(packet)
		print("[_assemble Done]")
		return self.__packet

	def _disassemble(self, raw_packet, cksum=1):
		print("dis: 1")
		packet = net2updh(raw_packet)
		print("net2updh>> Done")
		#print(packet)
		if cksum and packet[6:8] != '\000\000':
			print("disa>> if 1")
			our_cksum = udpcksum(packet)
			# no check sum
			# if our_cksum != 0:
			# 	print("disa>> if 2")
			# 	raise ValueError, packet
		print("disa>> upacking")
		elts = map(lambda x:x & 0xffff, struct.unpack('HHHH', packet[:8]))
		[self.sport, self.dport, self.ulen, self.sum] = elts
		print("set>> Done")
		#tail = self.ulen# Haowei

		self.data = packet[8:self.ulen]


def assemble(packet, cksum=1):
	return packet._assemble(cksum)
	
def disassemble(buffer, cksum=1):
	print("DIS")
	print("DISing")
	packet = Packet()
	print("DISing2")
	packet._disassemble(buffer, cksum)
	print("DISing done?")
	return packet