#!/usr/bin/env python

"""
Example usage:
  find . -type f | head -3000 | ./suffixes.py
Lists the file suffixes it finds, in order of decreasing frequency.
"""

import sys

d = {}

while True:
        L = sys.stdin.readline()
        if L.startswith("./"):
                L = L[2:]
        if not L:
                break
        L = L.rstrip()
        try:
                n = L.rindex(".")
        except ValueError:
                continue
        L = L[n+1:]
        if L not in d:
                d[L] = 1
        else:
                d[L] += 1

lst = [(-pop, suf) for suf, pop in d.items()]
lst.sort()
for pop, suf in lst:
        print suf, -pop
