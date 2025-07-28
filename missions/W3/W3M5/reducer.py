#!/usr/bin/env python
import sys

result = {}
resultCnt = {}

for line in sys.stdin:
    movieId,rating = line.strip().split('\t',1)
    if movieId not in result:
        result[movieId] = float(rating)
        resultCnt[movieId] = 1
    else:
        result[movieId] += float(rating)
        resultCnt[movieId] += 1
for movieId in sorted(result, key=int):
    avg = result[movieId] / resultCnt[movieId]
    print(f"{movieId}\t{avg:.1f}")