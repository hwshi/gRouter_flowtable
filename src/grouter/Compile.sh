swig -python ip.i 
#swig -python cli.i
#swig -python simplequeue.i
scons
gcc -shared -I/usr/include/python2.7/ -I../../include *.o -lpython2.7 -lreadline -ltermcap -lslack -lpthread -lutil -lm -o _Cip.so

#gcc -shared -I/usr/include/python2.7/ -I../../include *.o -lpython2.7 -lreadline -ltermcap -lslack -lpthread -lutil -lm -o _Cip.so
#gcc -shared -I/usr/include/python2.7/ -I../../include *.o -lpython2.7 -lreadline -ltermcap -lslack -lpthread -lutil -lm -o _Ccli.so
#gcc -shared -I/usr/include/python2.7/ -I../../include *.o -lpython2.7 -lreadline -ltermcap -lslack -lpthread -lutil -lm -o _Csimplequeue.so
#rm cli_wrap.o
#gcc -fPIC -I/usr/include/python2.7/ -I../../include *.o -lpython2.7 -lreadline -ltermcap -lslack -lpthread -lutil -lm -o grouter
gcc -I/usr/include/python2.7/ -I../../include *.o -lpython2.7 -lreadline -ltermcap -lslack -lpthread -lutil -lm -o grouter

rm *.o
