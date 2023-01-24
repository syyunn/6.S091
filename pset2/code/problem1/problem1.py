import pandas as pd

X = pd.read_csv('pset2/code/problem1/nongaussian_samples.csv',delimiter=' ', header=None, index_col=False)
X.columns = ['X1', 'X2']

from sklearn.linear_model import LinearRegression
reg1 = LinearRegression(fit_intercept=False).fit(X[['X1']], X[['X2']])
b_12 = reg1.coef_[0][0]
print("b12:", b_12)

reg2 = LinearRegression(fit_intercept=False).fit(X[['X2']], X[['X1']])
b_21 = reg2.coef_[0][0]
print("b21:", b_21)
import matplotlib.pyplot as plt

plt.scatter(X['X1'], X['X2'] - b_12 * X['X1'], label='(a)')
plt.scatter(X['X2'], X['X1'] - b_21 * X['X2'], label='(b)')
plt.legend()
plt.savefig('pset2/code/problem1/problem1.png')

# plt.show()

if __name__ == '__main__':
    pass

