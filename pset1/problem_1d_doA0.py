class Bernoulli:
    def __init__(self, p):
        self.p = p
    def __call__(self, x=1):
        if x == 1:
            return self.p
        elif x == 0:
            return 1-self.p
    
U = {0: 0.5, 1: 0.5}

def get_point_cond_prob(a:int, b:int, bern: lambda b: b/4):
    # P(A=a|B=b)
    return Bernoulli(bern(b))(a)

def get_entire_cond_prob(A_keys, B:dict, bern: lambda b: b/4):
    dist = {}
    for a in A_keys:
        for b in B.keys():
            dist[(a,b)] = get_point_cond_prob(a, b, bern)
    return dist

M_bar_A0 = {0: Bernoulli(0.5)(0), 1: Bernoulli(0.5)(1)}
print("M_bar_A0", M_bar_A0, sum(M_bar_A0.values()))

M = M_bar_A0

def get_point_cond_prob_2var(a:int, b:int, c:int, bern: lambda b,c: b/2 + c/4):
    return Bernoulli(bern(b, c))(a)

def get_entire_cond_prob_2var(A_keys, B:dict, C:dict, bern: lambda b,c : b/2 + c/4):
    dist = {}
    for a in A_keys:
        for b in B.keys():
            for c in C.keys():
                dist[(a,b,c)] = get_point_cond_prob_2var(a, b, c, bern)
    return dist

Y_bar_M_U = get_entire_cond_prob_2var([0,1], M, U, lambda b,c: b/2 + c/4)
print(Y_bar_M_U, sum(Y_bar_M_U.values()))

def get_YdoA0MU(U, M_bar_A0, Y_bar_M_U):
    YdoA0MU = {}
    for u in [0,1]:
        for m in [0,1]:
            for y in [0,1]:
                YdoA0MU[(y,m,u)] = U[u] *  M_bar_A0[m] * Y_bar_M_U[(y,m,u)]
    return YdoA0MU

YdoA0MU = get_YdoA0MU(U, M_bar_A0, Y_bar_M_U)
print("YdoA0MU", YdoA0MU, sum(YdoA0MU.values()))
assert sum(YdoA0MU.values()) == 1

def get_Y1_bar_doA0(YdoA0MU):
    Y1_bar_doA0 = sum([YdoA0MU[(1,m,u)] for m in [0,1] for u in [0,1]])
    return Y1_bar_doA0

def get_Y0_bar_doA0(YdoA0MU):
    Y0_bar_doA0 = sum([YdoA0MU[(0,m,u)] for m in [0,1] for u in [0,1]])
    return Y0_bar_doA0

print("Y1_bar_doA0: ", get_Y1_bar_doA0(YdoA0MU))
print("Y0_bar_doA0: ", get_Y0_bar_doA0(YdoA0MU))


# def get_Y1_bar_M0A0(YAMU):
#     Y1_bar_M0A0 = sum([YAMU[(1,0,0,u)] for u in [0,1]])/sum([YAMU[(y,0,0,u)] for y in [0,1] for u in [0,1]])
#     return Y1_bar_M0A0
# print(get_Y1_bar_M0A0(YAMU))

# def get_Y1_bar_M0A1(YAMU):
#     Y1_bar_M0A1 = sum([YAMU[(1,1,0,u)] for u in [0,1]])/sum([YAMU[(y,1,0,u)] for y in [0,1] for u in [0,1]])
#     return Y1_bar_M0A1
# print(get_Y1_bar_M0A1(YAMU))

