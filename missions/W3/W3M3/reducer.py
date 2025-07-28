#!/usr/bin/env python
import sys

result = {}

for line in sys.stdin:
    word,count = line.strip().split('\t',1)
    if word not in result:
        result[word] = 1
    else:
        result[word] += 1
for key, value in result.items():
    print(f"{key}: {value}")