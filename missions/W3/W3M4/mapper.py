#!/usr/bin/env python
import sys

pos_words = {
    "good", "great", "happy", "love", "awesome",
    "fantastic", "joyful", "wonderful", "excellent",
    "delightful", "amazing", "pleasant",
}

neg_words = {
    "bad", "sad", "worst", "poor", "angry",
    "horrible", "disappointing",  "hate",
     "terrible", "awful", "miserable", "dreadful"
}

for line in sys.stdin:
    input = line.strip().lower().split()
    if any(word in pos_words for word in input):
        print("positive\t1")
    elif any(word in neg_words for word in input):
        print("negative\t1")
    else:
        print("neutral\t1")
    