import numpy
from pandas import Series


def pagerank(df, maxerr=0.0001, d=0.85, max_iterations=100):
    n = float(len(df.count()))
    keys = df.keys()

    # dp = Fraction(1, n)
    dp = 1.0 / n
    rank = Series(data=[dp for _ in range(0, int(n))], index=keys, dtype=float)
    l = dict((key, len(df[key].dropna())) for key in keys)
    for i in range(0, max_iterations):
        print("Iteration %d..." % i)
        ro = rank.copy()
        for key in keys:
            val = 0.0
            for t_id in df.loc[:, key].dropna().keys():
                val += float(ro[t_id]) / float(l[key])

            rank[key] = (d * val) + ((1.0 - d) / n)
        err = numpy.sum(numpy.abs(rank - ro))
        print("Error: %f" % err)
        if err < maxerr: break
        print("Iteration %d...done" % i)
    return rank
