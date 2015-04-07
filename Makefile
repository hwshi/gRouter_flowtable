CFLAGS = -c -Isrc/grouter -Iinclude -I/usr/include/python2.7/ -DHAVE_GETOPT_LONG=1 -DHAVE_SNPRINTF=1 -DHAVE_VSSCANF=1 -DHAVE_PTHREAD_RWLOCK=1 -lpython2.7 -lreadline -ltermcap -lslack -lpthread -lutil -lm
#CFLAGS+= -Isrc/grouter/ -Iinclude/ -I/usr/include/python2.7/
#CFLAGS+= -g
LDFLAGS = -lpython2.7 -lreadline -ltermcap -lslack -lpthread -lutil -lm

SOURCES= arp.c classifier.c cli.c console.c ethernet.c filter.c fragment.c tun.c gnet.c grouter.c icmp.c info.c ip.c message.c mtu.c packetcore.c qdisc.c roundrobin.c routetable.c simplequeue.c tap.c tapio.c utils.c vpl.c wfq.c

OBJECTS=$(SOURCES:.c=.o)
EXECUTABLE=grouter

all: $(SOURCES) $(EXECUTABLE) swig

$(EXECUTABLE): $(OBJECTS)
	gcc $(OBJECTS) $(LDFLAGS) -o $@

.c.o:
	gcc $(CFLAGS) $< -o $@

swig:
	swig -python ginic.i
	gcc $(CFLAGS) ip.c ginic_wrap.c
	gcc -shared -Isrc/grouter/ -Iinclude/ -I/usr/include/python2.7/ ginic_wrap.o ip.o $(LDFLAGS) -o _GINIC.so

install:
	cp grouter /root/bin/grouter

clean:
	rm -rf *.o *~ 
