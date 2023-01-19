B_wa = [5, 0.5, 0.05]

# for b_wa in B_wa:

ratios = []
for b_wa in B_wa:
    import pandas as pd
    samples = pd.read_csv(f"pset1/samples_{b_wa}.csv", delimiter=' ', header=None, index_col=False)
    samples.columns = ['W', 'A', 'Y']

    from sklearn.linear_model import LinearRegression
    # Regress A onto W to get the parameters of the linear model
    reg = LinearRegression().fit(samples[['W']], samples[['A']])
    b_wa_hat = reg.coef_[0][0]
    # Regress Y onto W to get the parameters of the linear model
    reg = LinearRegression().fit(samples[['W']], samples[['Y']])
    b_wy_hat = reg.coef_[0][0]
    # get ratio of b_wy/b_wa
    r = b_wy_hat/b_wa_hat
    print(f"b_wa: {b_wa}, b_wa_hat: {b_wa_hat}, b_wy_hat: {b_wy_hat}, ratio: {r},  b_ay: {7.5}, error:{abs(r-7.5)}")
    ratios.append(r)





pass