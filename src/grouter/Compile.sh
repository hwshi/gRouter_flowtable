swig -python ginic.i 
echo "Building _GINIC.so ..."
gcc -g -DHAVE_PTHREAD_RWLOCK=1 -DHAVE_GETOPT_LONG -Wno-write-strings -I/usr/include/python2.7/ -I../../include -c ginic_wrap.c -lpython2.7 -lreadline -ltermcap -lslack -lpthread -lutil -lm
gcc -shared -I/usr/include/python2.7/ -I../../include ginic_wrap.o -lpython2.7 -lreadline -ltermcap -lslack -lpthread -lutil -lm -o _GINIC.so
rm *.o
echo "Building grouter..."
scons
#echo "Linking..."
#gcc -I/usr/include/python2.7/ -I../../include *.o -lpython2.7 -lreadline -ltermcap -lslack -lpthread -lutil -lm -o grouter

rm *.o
