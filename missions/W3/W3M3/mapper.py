#!/usr/bin/env python
import sys

for line in sys.stdin:
    for word in line.strip().split():
        print(f"{word}\t1")