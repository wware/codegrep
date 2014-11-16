#!/bin/sh

PYBASE=/usr/local/Cellar/python/2.7.8_1/Frameworks/Python.framework/Versions/2.7

gcc -O3 -c -I${PYBASE}/include/python2.7 cgmodule.c
gcc -shared -fPIC -o cgmodule.so -I${PYBASE}/lib/python2.7 cgmodule.o -lpython
