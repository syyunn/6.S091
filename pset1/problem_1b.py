class Bernoulli:
    def __init__(self, p):
        self.p = p
    def __call__(self, x=1):
        if x == 1:
            return self.p
        elif x == 0:
            return 1-self.p
    

U = {0: 0.5, 1: 0.5}
def get_point_cond_prob(a:int, b:int, bern= lambda b: b/4):
    # P(A=a|B=b)
    return Bernoulli(bern(b))(a)

A1_bar_U1 = get_point_cond_prob(1, 1, lambda b: b/4)
print("A1_bar_U1", A1_bar_U1)

def get_entire_cond_prob(A_keys, B:dict, bern= lambda b: b/4):
    dist = {}
    for a in A_keys:
        for b in B.keys():
            dist[(a,b)] = get_point_cond_prob(a, b, bern)
    return dist

A_bar_U = get_entire_cond_prob([0,1], U, lambda b: b/4)
print("A_bar_U", A_bar_U, sum(A_bar_U.values()))

def integrate_cond(A_bar_B: dict, B:dict):
    A = {}
    for a in [0,1]:
        A[a] = sum([A_bar_B[(a,b)]*B[b] for b in B.keys()])
    return A

A = integrate_cond(A_bar_U, U)
print(A)

M_bar_A = get_entire_cond_prob([0,1], A, lambda b: 1/2 + 0.1*b)
print("M_bar_A", M_bar_A, sum(M_bar_A.values()))

M = integrate_cond(M_bar_A, A)

def get_point_cond_prob_2var(a:int, b:int, c:int, bern= lambda b,c: b/2 + c/4):
    return Bernoulli(bern(b, c))(a)

def get_entire_cond_prob_2var(A_keys, B:dict, C:dict, bern= lambda b,c : b/2 + c/4):
    dist = {}
    for a in A_keys:
        for b in B.keys():
            for c in C.keys():
                dist[(a,b,c)] = get_point_cond_prob_2var(a, b, c, bern)
    return dist

Y_bar_M_U = get_entire_cond_prob_2var([0,1], M, U, lambda b,c: b/2 + c/4)
print("Y_bar_M_U", Y_bar_M_U, sum(Y_bar_M_U.values()))

def get_YAMU(U, A_bar_U, M_bar_A, Y_bar_M_U):
    YAMU = {}
    for u in [0,1]:
        for a in [0,1]:
            for m in [0,1]:
                for y in [0,1]:
                    YAMU[(y,a,m,u)] = U[u] * A_bar_U[(a,u)] * M_bar_A[(m,a)] * Y_bar_M_U[(y,m,u)]
    return YAMU

YAMU = get_YAMU(U, A_bar_U, M_bar_A, Y_bar_M_U)
print("YAMU: ", YAMU, sum(YAMU.values()))
assert sum(YAMU.values()) == 1

def get_Y1(YAMU):
    Y1 = sum([YAMU[(1,a,m,u)] for a in [0,1] for m in [0,1] for u in [0,1]])
    return Y1
print("Y1: ", get_Y1(YAMU))

def get_Y1_bar_M0A0(YAMU):
    Y1_bar_M0A0 = sum([YAMU[(1,0,0,u)] for u in [0,1]])/sum([YAMU[(y,0,0,u)] for y in [0,1] for u in [0,1]])
    return Y1_bar_M0A0
print(get_Y1_bar_M0A0(YAMU))

def get_Y1_bar_M0A1(YAMU):
    Y1_bar_M0A1 = sum([YAMU[(1,1,0,u)] for u in [0,1]])/sum([YAMU[(y,1,0,u)] for y in [0,1] for u in [0,1]])
    return Y1_bar_M0A1
print(get_Y1_bar_M0A1(YAMU))

def get_Y1_bar_A0U0(YAMU):
    Y1_bar_A0U0 = sum([YAMU[(1,0,m,0)] for m in [0,1]])/sum([YAMU[(y,0,m,0)] for y in [0,1] for m in [0,1]])
    return Y1_bar_A0U0
print("Y1_bar_A0U0: ", get_Y1_bar_A0U0(YAMU))

def get_Y_bar_AU(YAMU, y, a, u):
    try:
        Y_bar_AU = sum([YAMU[(y,a,m,u)] for m in [0,1]])/sum([YAMU[(y,a,m,u)] for y in [0,1] for m in [0,1]])
        return Y_bar_AU
    except ZeroDivisionError:
        print("zero divisor", y,a,u)

print("Y1_bar_A1U1: ", get_Y_bar_AU(YAMU, 1, 1, 1))
print("Y1_bar_A1U0: ", get_Y_bar_AU(YAMU, 1, 1, 0))

print("Y0_bar_A0U1: ", get_Y_bar_AU(YAMU, 0, 0, 1))
print("Y0_bar_A0U0: ", get_Y_bar_AU(YAMU, 0, 0, 0))

print("Y1_bar_A0U1: ", get_Y_bar_AU(YAMU, 1, 0, 1))
print("Y1_bar_A0U0: ", get_Y_bar_AU(YAMU, 1, 0, 0))
