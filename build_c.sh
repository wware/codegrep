#!/bin/bash

OS=$(uname -a | sed "s/ .*//")

if [ "$OS" == "Linux" ]; then
    PYBASE=/usr
    LFLAGS="-L/usr/lib/x86_64-linux-gnu -lpython2.7"
fi

if [ "$OS" == "Darwin" ]; then
    # Homebrew install of Python on the Mac
    PYBASE=/usr/local/Cellar/python/2.7.8_1/Frameworks/Python.framework/Versions/2.7
    LFLAGS="-L${PYBASE}/lib/python2.7 -lpython"
fi

gcc -O3 -c -fPIC -I${PYBASE}/include/python2.7 cgmodule.c
gcc -shared -fPIC -o cgmodule.so ${LFLAGS} cgmodule.o -lpython2.7
