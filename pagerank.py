import numpy
from pandas import Series


def pagerank(df, maxerr=0.0001):
    n = df.count()
    rank = numpy.full(n, 1.0/n)
    err = 1.0
    while err > maxerr:
