__author__ = 'mohamed'

import math
from Counter import Counter

class CosineSimilarity(object):

    def buildVector(masterWords, otherWords):
        masterCounter = Counter(masterWords)
        otherCounter = Counter(otherWords)
        all_items = set(masterCounter.keys()).union( set(otherCounter.keys()))
        vector1 = [masterCounter[k] for k in all_items]
        vector2 = [otherCounter[k] for k in all_items]
        return vector1, vector2

    def cosine(masterVector, otherVector):
        dot_product = sum(n1 * n2 for n1,n2 in zip(masterVector, otherVector))
        magnitude1 = math.sqrt (sum(n ** 2 for n in masterVector))
        magnitude2 = math.sqrt (sum(n ** 2 for n in otherVector))
        return dot_product / (magnitude1 * magnitude2)

