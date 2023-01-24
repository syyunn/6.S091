import pandas as pd
import numpy as np

X = pd.read_csv('pset2/code/problem2/pcalg_samples.csv',delimiter=' ', header=None, index_col=False)
X.columns = ['X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7']

from sklearn.linear_model import LinearRegression

def regress_linear(X, y):
    reg = LinearRegression().fit(X, y)
    return reg.coef_

def compute_partial_correlation(samples, i, j, S):
    Xi = samples[[f'X{i}']]
    Xj = samples[[f'X{j}']]

    if len(S) == 0:
        corr = np.corrcoef(np.squeeze(Xi), np.squeeze(Xj))[0, 1]        
        return corr

    S = samples[[f'X{s}' for s in S]]

    bi = regress_linear(S, Xi)
    bj = regress_linear(S, Xj)

    Ri = Xi - np.dot(S, bi.T)
    Rj = Xj - np.dot(S, bj.T)

    corr = np.corrcoef(np.squeeze(Ri), np.squeeze(Rj))[0, 1]

    return corr

r1 = compute_partial_correlation(X, 1, 7, [3, 4])
r2 = compute_partial_correlation(X, 1, 7, [])

ra = compute_partial_correlation(X, 1, 4, [])
rb = compute_partial_correlation(X, 1, 4, [2, 3])

def fisherz(r):
    return 0.5 * np.log((1 + r) / (1 - r))

def ztransf(samples, i, j, S):
    r = compute_partial_correlation(samples, i, j, S)
    return np.sqrt(samples.shape[0]- len(S)-3) * fisherz(r)

z1 = ztransf(X, 1, 7, [3, 4])
z2 = ztransf(X, 1, 7, [])

zc = ztransf(X, 1, 4, [2, 3])


if __name__ == '__main__':
    pass

