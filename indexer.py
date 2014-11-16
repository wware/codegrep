#!/usr/bin/env python

import os
import sys
import string
import re
import cPickle


# suffixes should maybe be passed in thru some config file?
def chooser(f):
    return (f.endswith(".cs") or
            f.endswith(".xaml") or
            f.endswith(".reg") or
            f.endswith(".proj") or
            f.endswith(".prj") or
            f.endswith(".txt") or
            f.endswith(".text") or
            f.endswith(".h") or
            f.endswith(".c") or
            f.endswith(".cpp") or
            f.endswith(".cxx") or
            f.endswith(".C") or
            f.endswith(".rb") or
            f.endswith(".pl") or
            f.endswith(".pm") or
            f.endswith(".xml") or
            f.endswith(".html") or
            f.endswith(".css") or
            f.endswith(".js") or
            f.endswith(".py") or
            f.endswith(".xml") or
            f.endswith(".pro") or
            f.endswith(".data") or
            f.endswith(".ref") or
            f.endswith(".qdoc") or
            f.endswith(".conf") or
            f.endswith(".qml") or
            f.endswith(".pri") or
            f.endswith(".prf") or
            f.endswith(".ent") or
            f.endswith(".ref") or
            f.endswith(".ent") or
            f.endswith(".qrc") or
            f.endswith(".ui") or
            f.endswith(".qmake") or
            f.endswith(".dtd") or
            ("." not in f))


files = []
d0 = {}

root = os.environ["CODEGREPROOT"]

for _dir, _, _files in os.walk(root):
    if "/.git" in _dir:
        continue
    if "/.svn" in _dir:
        continue
    if _dir.endswith(".codegrep.index"):
        continue
    _files = filter(chooser, _files)
    if not _files:
        continue

    print _dir
    ff = os.path.join(_dir, ".codegrep.index/files")
    if os.path.exists(ff):
        tf = os.path.getctime(ff)
        sources = map(lambda x: os.path.join(_dir, x), _files)
        ts = map(os.path.getctime, sources)
        ts.sort()
        if tf > ts[-1]:
            continue

    try:
        # directory names can include parens, spaces, other garbage
        cgdir = os.path.join(_dir, ".codegrep.index")
        os.system("mkdir -p " + cgdir)
        open(cgdir + "/files", "w").write("quick sanity check")
    except:
        continue

    d0 = {}
    fi = 0
    for filename in _files:
        if True:
            # C EXTENSION
            if False:
                # DEBUGGING MEMORY LEAKS
                import objgraph
                import sys
                print "===", sys.getrefcount(d0)
                print objgraph.show_most_common_types(limit=20)
            import cg
            cg.scan(d0, fi, os.path.join(_dir, filename))
        else:
            # REFERENCE IMPLEMENTATION
            R = open(os.path.join(_dir, filename)).read()
            if len(R) < 3:
                continue
            for i in range(len(R) - 2):
                # all this stuff should go into a swigged C function
                key0 = R[i]
                if not (32 <= ord(key0) <= 176):
                    continue
                if not (32 <= ord(R[i+1]) <= 176):
                    continue
                # assume N==3 here
                if not (32 <= ord(R[i+2]) <= 176):
                    continue
                key1 = R[i+1:i+3]
                try:
                    d = d0[key0]
                except KeyError:
                    d = d0[key0] = {}
                try:
                    d[key1][fi] = None
                except KeyError:
                    d[key1] = {fi: None}
        fi += 1

    try:
        cPickle.dump(_files, open(cgdir + "/files", "w"))
        for key0 in d0.keys():
            d = dict([(k, v.keys()) for k, v in d0[key0].items()])
            cPickle.dump(d, open(os.path.join(cgdir, str(ord(key0))), "w"))
    except KeyboardInterrupt:
        os.system('rm -rf ' + cgdir)
