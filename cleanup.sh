#!/bin/bash

if [ "${CODEGREPROOT}" == "" ]
then
    echo "Please specify the root of the searched directory tree in CODEGREPROOT"
    exit 1
fi

find ${CODEGREPROOT} -type d -name ".codegrep.index" -exec rm -rf {} \; 2> /dev/null
exit 0
