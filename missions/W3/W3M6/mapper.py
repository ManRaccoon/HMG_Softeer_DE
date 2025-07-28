#!/usr/bin/env python
import json
import sys

for line in sys.stdin:
    try:
        review = json.loads(line)
    except json.JSONDecodeError:
        continue
    asin = review.get("asin")
    rating = review.get("rating")
    if not asin or rating is None:
        continue
    print(f"{asin}\t{rating}")