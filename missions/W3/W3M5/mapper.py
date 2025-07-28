#!/usr/bin/env python
import sys

for line in sys.stdin:
    if line.startswith("userId,"):
        continue
    userId, movieId, rating, timestamp = line.strip().split(',')
    print(f"{movieId}\t{rating}")
    