#!/usr/bin/env python
import sys

current_asin = None
sum_rating = 0.0
count = 0

for line in sys.stdin:
    asin,rating = line.strip().split('\t', 1)
    if asin is None:
        current_asin = asin
        sum_rating = rating
        count = 1
    elif asin == current_asin:
        sum_rating += rating
        count += 1
    else:
        avg = sum_rating / count
        print(f"{current_asin}\t{count}\t{avg:.1f}")
        current_asin = asin
        sum_rating = rating
        count = 1

if current_asin is not None:
    avg = sum_rating / count
    print(f"{current_asin}\t{count}\t{avg:.1f}")