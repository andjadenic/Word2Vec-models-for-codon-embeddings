from scipy.special import comb


def calculate_prob(tp: int, L: int, n: int=6):
    '''
    returns the probability that any model
    correctly predict tp or more (tp<L)
    codons out of L-1 from the same group by chance
    '''
    prob = 0
    for i in range(tp, L):
      prob += ((comb(L - 1, i) * comb(64 - L, n - i)) / comb(63, n))

    return prob * 100

