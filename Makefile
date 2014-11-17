UNAME := $(shell uname)
# dotted python version (2.3, 2.4)
PYDVER := $(shell python -c "import sys; print sys.version[:3]")
# un-dotted python version (23, 24)
PYVER := $(shell python -c "import sys; print sys.version[0]+sys.version[2]")

ifeq ($(strip $(UNAME)),Darwin)
# Mac
PYBASE=/System/Library/Frameworks/Python.framework/Versions/$(PYDVER)
LFLAGS+=-L$(PYBASE)/lib/python$(PYDVER)/config -lpython
else
# Linux
PYBASE=/usr
LFLAGS+=-L/usr/lib/x86_64-linux-gnu -lpython$(PYDVER)
endif

CFLAGS+=-I$(PYBASE)/include/python$(PYDVER)

all: cgmodule.so

clean:
	rm -f *.o *.so

cgmodule.o: cgmodule.c
	gcc -O3 -c -fPIC $(CFLAGS) cgmodule.c

cgmodule.so: cgmodule.o
	gcc -shared -fPIC -o cgmodule.so $(LFLAGS) cgmodule.o -lpython$(PYDVER)
