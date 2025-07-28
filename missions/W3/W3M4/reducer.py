#!/usr/bin/env python
import sys

result = {}

for line in sys.stdin:
    sent,count = line.strip().split('\t',1)
    if sent not in result:
        result[sent] = 1
    else:
        result[sent] += 1
for sent, count in result.items():
    print(f"{sent}: {count}")