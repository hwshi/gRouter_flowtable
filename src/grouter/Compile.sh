swig -python ginic.i 
scons
gcc -shared -I/usr/include/python2.7/ -I../../include *.o -lpython2.7 -lreadline -ltermcap -lslack -lpthread -lutil -lm -o _GINIC.so
gcc -I/usr/include/python2.7/ -I../../include *.o -lpython2.7 -lreadline -ltermcap -lslack -lpthread -lutil -lm -o grouter

rm *.o
