CFLAGS = -c -Isrc/grouter -I../../include -I/usr/include/python2.7/ -DHAVE_GETOPT_LONG=1 -DHAVE_SNPRINTF=1 -DHAVE_VSSCANF=1 -DHAVE_PTHREAD_RWLOCK=1 -lpython2.7 -lreadline -ltermcap -lslack -lpthread -lutil -lm
#CFLAGS+= -Isrc/grouter/ -Iinclude/ -I/usr/include/python2.7/
#CFLAGS+= -g
LDFLAGS = -lpython2.7 -lreadline -ltermcap -lslack -lpthread -lutil -lm

SOURCES= arp.c classifier.c cli.c console.c ethernet.c filter.c flowtable.c fragment.c gnet.c grouter.c icmp.c info.c ip.c message.c mtu.c packetcore.c pythondebug.c qdisc.c roundrobin.c routetable.c simplequeue.c tap.c tapio.c utils.c vpl.c wfq.c

OBJECTS=$(SOURCES:.c=.o)
EXECUTABLE=grouter

all: $(SOURCES) $(EXECUTABLE) 

$(EXECUTABLE): swig $(OBJECTS)
	echo "E - O"
	gcc $(OBJECTS) $(LDFLAGS) -o $@

.c.o:
	echo ".c.o"
	gcc $(CFLAGS) $< -o $@

swig: wrap $(OBJECTS) 
	echo "swig..."
	gcc $(CFLAGS) ginic_wrap.c
	gcc -shared -Isrc/grouter/ -Iinclude/ -I/usr/include/python2.7/ ginic_wrap.o ip.o $(LDFLAGS) -o _GINIC.so
wrap: ginic.i
	echo "wrap..."
	swig -python ginic.i	
install:
	cp grouter /root/bin/grouter

clean:
	rm -rf *.o *~ 
