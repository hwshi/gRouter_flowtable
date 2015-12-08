# This file was automatically generated by SWIG (http://www.swig.org).
# Version 2.0.11
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info
if version_info >= (2,6,0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_GINIC', [dirname(__file__)])
        except ImportError:
            import _GINIC
            return _GINIC
        if fp is not None:
            try:
                _mod = imp.load_module('_GINIC', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _GINIC = swig_import_helper()
    del swig_import_helper
else:
    import _GINIC
del version_info
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError(name)

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0


MAX_IPREVLENGTH_ICMP = _GINIC.MAX_IPREVLENGTH_ICMP

def IPPayload(*args):
  return _GINIC.IPPayload(*args)
IPPayload = _GINIC.IPPayload

def createGPacket(*args):
  return _GINIC.createGPacket(*args)
createGPacket = _GINIC.createGPacket

def assembleWithIPPayload(*args):
  return _GINIC.assembleWithIPPayload(*args)
assembleWithIPPayload = _GINIC.assembleWithIPPayload

def createGPacketWithPacket(*args):
  return _GINIC.createGPacketWithPacket(*args)
createGPacketWithPacket = _GINIC.createGPacketWithPacket

def createGPacketWithIPPayload(*args):
  return _GINIC.createGPacketWithIPPayload(*args)
createGPacketWithIPPayload = _GINIC.createGPacketWithIPPayload

def getGPacketMetaheaderLen():
  return _GINIC.getGPacketMetaheaderLen()
getGPacketMetaheaderLen = _GINIC.getGPacketMetaheaderLen

def getGPacketString(*args):
  return _GINIC.getGPacketString(*args)
getGPacketString = _GINIC.getGPacketString

def getDeviceName():
  return _GINIC.getDeviceName()
getDeviceName = _GINIC.getDeviceName

def getPortNumber():
  return _GINIC.getPortNumber()
getPortNumber = _GINIC.getPortNumber

def getPortTuple():
  return _GINIC.getPortTuple()
getPortTuple = _GINIC.getPortTuple

def gini_ofp_flow_mod(*args):
  return _GINIC.gini_ofp_flow_mod(*args)
gini_ofp_flow_mod = _GINIC.gini_ofp_flow_mod

def gini_ofp_flow_mod_ADD(*args):
  return _GINIC.gini_ofp_flow_mod_ADD(*args)
gini_ofp_flow_mod_ADD = _GINIC.gini_ofp_flow_mod_ADD

def gini_ofp_flow_mod_MODIFY(*args):
  return _GINIC.gini_ofp_flow_mod_MODIFY(*args)
gini_ofp_flow_mod_MODIFY = _GINIC.gini_ofp_flow_mod_MODIFY

def gini_ofp_flow_mod_MODIFY_STRICT(*args):
  return _GINIC.gini_ofp_flow_mod_MODIFY_STRICT(*args)
gini_ofp_flow_mod_MODIFY_STRICT = _GINIC.gini_ofp_flow_mod_MODIFY_STRICT

def gini_ofp_flow_mod_DELETE(*args):
  return _GINIC.gini_ofp_flow_mod_DELETE(*args)
gini_ofp_flow_mod_DELETE = _GINIC.gini_ofp_flow_mod_DELETE

def gini_ofp_flow_mod_DELETE_STRICT(*args):
  return _GINIC.gini_ofp_flow_mod_DELETE_STRICT(*args)
gini_ofp_flow_mod_DELETE_STRICT = _GINIC.gini_ofp_flow_mod_DELETE_STRICT
class pkt_data_t(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, pkt_data_t, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, pkt_data_t, name)
    __repr__ = _swig_repr
    __swig_setmethods__["data"] = _GINIC.pkt_data_t_data_set
    __swig_getmethods__["data"] = _GINIC.pkt_data_t_data_get
    if _newclass:data = _swig_property(_GINIC.pkt_data_t_data_get, _GINIC.pkt_data_t_data_set)
    __swig_getmethods__["header"] = _GINIC.pkt_data_t_header_get
    if _newclass:header = _swig_property(_GINIC.pkt_data_t_header_get)
    def __init__(self): 
        this = _GINIC.new_pkt_data_t()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _GINIC.delete_pkt_data_t
    __del__ = lambda self : None;
pkt_data_t_swigregister = _GINIC.pkt_data_t_swigregister
pkt_data_t_swigregister(pkt_data_t)
cvar = _GINIC.cvar

class pkt_data_t_header(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, pkt_data_t_header, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, pkt_data_t_header, name)
    __repr__ = _swig_repr
    __swig_setmethods__["dst"] = _GINIC.pkt_data_t_header_dst_set
    __swig_getmethods__["dst"] = _GINIC.pkt_data_t_header_dst_get
    if _newclass:dst = _swig_property(_GINIC.pkt_data_t_header_dst_get, _GINIC.pkt_data_t_header_dst_set)
    __swig_setmethods__["src"] = _GINIC.pkt_data_t_header_src_set
    __swig_getmethods__["src"] = _GINIC.pkt_data_t_header_src_get
    if _newclass:src = _swig_property(_GINIC.pkt_data_t_header_src_get, _GINIC.pkt_data_t_header_src_set)
    __swig_setmethods__["prot"] = _GINIC.pkt_data_t_header_prot_set
    __swig_getmethods__["prot"] = _GINIC.pkt_data_t_header_prot_get
    if _newclass:prot = _swig_property(_GINIC.pkt_data_t_header_prot_get, _GINIC.pkt_data_t_header_prot_set)
    def __init__(self): 
        this = _GINIC.new_pkt_data_t_header()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _GINIC.delete_pkt_data_t_header
    __del__ = lambda self : None;
pkt_data_t_header_swigregister = _GINIC.pkt_data_t_header_swigregister
pkt_data_t_header_swigregister(pkt_data_t_header)

class label_t(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, label_t, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, label_t, name)
    __repr__ = _swig_repr
    __swig_setmethods__["prot"] = _GINIC.label_t_prot_set
    __swig_getmethods__["prot"] = _GINIC.label_t_prot_get
    if _newclass:prot = _swig_property(_GINIC.label_t_prot_get, _GINIC.label_t_prot_set)
    __swig_setmethods__["process"] = _GINIC.label_t_process_set
    __swig_getmethods__["process"] = _GINIC.label_t_process_get
    if _newclass:process = _swig_property(_GINIC.label_t_process_get, _GINIC.label_t_process_set)
    def __init__(self): 
        this = _GINIC.new_label_t()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _GINIC.delete_label_t
    __del__ = lambda self : None;
label_t_swigregister = _GINIC.label_t_swigregister
label_t_swigregister(label_t)

class pkt_frame_t(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, pkt_frame_t, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, pkt_frame_t, name)
    __repr__ = _swig_repr
    __swig_setmethods__["src_interface"] = _GINIC.pkt_frame_t_src_interface_set
    __swig_getmethods__["src_interface"] = _GINIC.pkt_frame_t_src_interface_get
    if _newclass:src_interface = _swig_property(_GINIC.pkt_frame_t_src_interface_get, _GINIC.pkt_frame_t_src_interface_set)
    __swig_setmethods__["src_ip_addr"] = _GINIC.pkt_frame_t_src_ip_addr_set
    __swig_getmethods__["src_ip_addr"] = _GINIC.pkt_frame_t_src_ip_addr_get
    if _newclass:src_ip_addr = _swig_property(_GINIC.pkt_frame_t_src_ip_addr_get, _GINIC.pkt_frame_t_src_ip_addr_set)
    __swig_setmethods__["src_hw_addr"] = _GINIC.pkt_frame_t_src_hw_addr_set
    __swig_getmethods__["src_hw_addr"] = _GINIC.pkt_frame_t_src_hw_addr_get
    if _newclass:src_hw_addr = _swig_property(_GINIC.pkt_frame_t_src_hw_addr_get, _GINIC.pkt_frame_t_src_hw_addr_set)
    __swig_setmethods__["dst_interface"] = _GINIC.pkt_frame_t_dst_interface_set
    __swig_getmethods__["dst_interface"] = _GINIC.pkt_frame_t_dst_interface_get
    if _newclass:dst_interface = _swig_property(_GINIC.pkt_frame_t_dst_interface_get, _GINIC.pkt_frame_t_dst_interface_set)
    __swig_setmethods__["nxth_ip_addr"] = _GINIC.pkt_frame_t_nxth_ip_addr_set
    __swig_getmethods__["nxth_ip_addr"] = _GINIC.pkt_frame_t_nxth_ip_addr_get
    if _newclass:nxth_ip_addr = _swig_property(_GINIC.pkt_frame_t_nxth_ip_addr_get, _GINIC.pkt_frame_t_nxth_ip_addr_set)
    __swig_setmethods__["arp_valid"] = _GINIC.pkt_frame_t_arp_valid_set
    __swig_getmethods__["arp_valid"] = _GINIC.pkt_frame_t_arp_valid_get
    if _newclass:arp_valid = _swig_property(_GINIC.pkt_frame_t_arp_valid_get, _GINIC.pkt_frame_t_arp_valid_set)
    __swig_setmethods__["arp_bcast"] = _GINIC.pkt_frame_t_arp_bcast_set
    __swig_getmethods__["arp_bcast"] = _GINIC.pkt_frame_t_arp_bcast_get
    if _newclass:arp_bcast = _swig_property(_GINIC.pkt_frame_t_arp_bcast_get, _GINIC.pkt_frame_t_arp_bcast_set)
    __swig_setmethods__["label"] = _GINIC.pkt_frame_t_label_set
    __swig_getmethods__["label"] = _GINIC.pkt_frame_t_label_get
    if _newclass:label = _swig_property(_GINIC.pkt_frame_t_label_get, _GINIC.pkt_frame_t_label_set)
    def __init__(self): 
        this = _GINIC.new_pkt_frame_t()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _GINIC.delete_pkt_frame_t
    __del__ = lambda self : None;
pkt_frame_t_swigregister = _GINIC.pkt_frame_t_swigregister
pkt_frame_t_swigregister(pkt_frame_t)

class gpacket_t(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, gpacket_t, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, gpacket_t, name)
    __repr__ = _swig_repr
    __swig_setmethods__["frame"] = _GINIC.gpacket_t_frame_set
    __swig_getmethods__["frame"] = _GINIC.gpacket_t_frame_get
    if _newclass:frame = _swig_property(_GINIC.gpacket_t_frame_get, _GINIC.gpacket_t_frame_set)
    __swig_setmethods__["data"] = _GINIC.gpacket_t_data_set
    __swig_getmethods__["data"] = _GINIC.gpacket_t_data_get
    if _newclass:data = _swig_property(_GINIC.gpacket_t_data_get, _GINIC.gpacket_t_data_set)
    def __init__(self): 
        this = _GINIC.new_gpacket_t()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _GINIC.delete_gpacket_t
    __del__ = lambda self : None;
gpacket_t_swigregister = _GINIC.gpacket_t_swigregister
gpacket_t_swigregister(gpacket_t)


def IPOutgoingPacket(*args):
  return _GINIC.IPOutgoingPacket(*args)
IPOutgoingPacket = _GINIC.IPOutgoingPacket

def addRouteEntry(*args):
  return _GINIC.addRouteEntry(*args)
addRouteEntry = _GINIC.addRouteEntry
# This file is compatible with both classic and new-style classes.


