B_wa = [5, 0.5, 0.05]

# for b_wa in B_wa:

b_wa = 5

import pandas as pd

samples = pd.read_csv(f"pset1/samples_{b_wa}.csv", delimiter=' ', header=None, index_col=0)
print(samples.head())