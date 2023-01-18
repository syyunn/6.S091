def get_cond_prob(AB:dict, B:dict, a:int, b:int): 
    # P(A=a|B=b) = P(A=a,B=b)/P(B=bs)
    return AB[(a,b)]/B[b]
    
U = {0: 0.5, 1: 0.5}
UA = {(0,0): 1/2, (0,1):0, (1,0): 3/8, (1,1): 1/8}
AU = {(0,0): 1/2, (0,1): 3/8, (1,0): 0, (1,1): 1/8}

def marginalize(AB: dict, A:dict):
    B = {0: AB[(0,0)] + AB[(1,0)], 1: AB[(0,1)] + AB[(1,1)]}
    return B

A = marginalize(UA, U)
print(A)
# A = {0: 7/8, 1: 1/8}

AM = {(0,0): 1/2*7/8, (0,1): 1/2*7/8, (1,0): 2/5*1/8, (1,1): 3/5*1/8}
MA = {(0,0): 1/2*7/8, (0,1): 2/5*1/8, (1,0): 1/2*7/8, (1,1): 3/5*1/8}
M = marginalize(AM, A)
print(M)

def get_MAU(U, AU, MA):
    # P(M,A,U)= P(M|A)P(A|U)P(U)
    MAU = {}
    for u in [0,1]:
        for a in [0,1]:
            for m in [0,1]:
                MAU[(m,a,u)] = get_cond_prob(MA, A, m, a)*get_cond_prob(AU, U, a, u)*U[u]
    return MAU
MAU = get_MAU(U, AU, MA)
print("MAU: ", MAU, sum(MAU.values()))

def get_MU(MAU):
    MU = {}
    for u in [0,1]:
        for m in [0,1]:
            MU[(m,u)] = sum([MAU[(m,a,u)] for a in [0,1]])
    return MU
MU = get_MU(MAU)
print(MU)

YMU = {(0,0,0):1 * MU[(0,0)], (1,0,0):0* MU[(0,0)],
       (0,0,1):3/4* MU[(0,1)], (1,0,1):1/4* MU[(0,1)],
       (0,1,0):1/2 * MU[(1,0)], (1,1,0):1/2* MU[(1,0)],
       (0,1,1):1/4 * MU[(1,1)], (1,1,1):3/4* MU[(1,1)]}

print("YMU: ", YMU, sum(YMU.values()))

def marginalize_YMU(YMU):
    Y = {}
    for y in [0,1]:
        Y[y] = sum([YMU[(y, m, u)] for m, u in [(0,0), (0,1), (1,0), (1,1)]])
    return Y

Y = marginalize_YMU(YMU)
print("Y: ", Y, sum(Y.values()))

def get_Y_BAR_MU(YMU, MU):
    Y_BAR_MU = {}
    for y in [0,1]:
        for m in [0,1]:
            for u in [0,1]:
                Y_BAR_MU[(y,m,u)] = YMU[(y,m,u)]/MU[(m,u)]
    return Y_BAR_MU

Y_BAR_MU=get_Y_BAR_MU(YMU, MU)
print("Y_BAR_MU: ", Y_BAR_MU, sum(Y_BAR_MU.values()))

def get_YMAU(YMU, MU, MA, AU, A):
    # P(Y,M,A,U)= P(Y|M,U)P(M|A)P(A|U)P(U)
    YMAU = {}
    for y in [0,1]:
        for m in [0,1]:
            for a in [0,1]:
                for u in [0,1]:
                    YMAU[(y,m,a,u)] = Y_BAR_MU[(y,m,u)]*get_cond_prob(MA, A, m, a)*get_cond_prob(AU, U, a, u)*U[u]
    return YMAU

YMAU = get_YMAU(YMU, MU, MA, AU, A)
print("YMAU: ", YMAU, sum(YMAU.values()))

# P(Y=1|M=0, A=0) = sum_U(P(Y=1|M=0, A=0)))
def get_Y1_M0A0(YMAU):
    return sum([YMAU[(1,0,0,u)] for u in [0,1]])

print("Y1_M0A0: ", get_Y1_M0A0(YMAU))

# P(Y=1|M=0, A=1) = sum_U(P(Y=1|M=0, A=1)))
def get_Y1_M0A1(YMAU):
    return sum([YMAU[(1,0,1,u)] for u in [0,1]])

print("Y1_M0A1: ", get_Y1_M0A1(YMAU))

# Below for (d)
YMU = {(0, 0, 0): 


def get_Y1_bar_doA1(YMAU):
    return sum([YMAU[(1,m,1,u)] for m, u in [(0,0), (0,1), (1,0), (1,1)]])/sum([YMAU[(y,m,1,u)] for y in [0,1] for m in [0,1] for u in [0,1]])

def get_Y0_bar_doA1(YMAU):
    return sum([YMAU[(0,m,1,u)] for m, u in [(0,0), (0,1), (1,0), (1,1)]])/sum([YMAU[(y,m,1,u)] for y in [0,1] for m in [0,1] for u in [0,1]])

print("Y1_bar_doA1: ", get_Y1_bar_doA1(YMAU))
print("Y0_bar_doA1: ", get_Y0_bar_doA1(YMAU))

def get_Y1_bar_doA0(YMAU):
    return sum([YMAU[(1,m,0,u)] for m, u in [(0,0), (0,1), (1,0), (1,1)]])/sum([YMAU[(y,m,0,u)] for y in [0,1] for m in [0,1] for u in [0,1]])

def get_Y0_bar_doA0(YMAU):
    return sum([YMAU[(0,m,0,u)] for m, u in [(0,0), (0,1), (1,0), (1,1)]])/sum([YMAU[(y,m,0,u)] for y in [0,1] for m in [0,1] for u in [0,1]])

print("Y1_bar_doA0: ", get_Y1_bar_doA0(YMAU))
print("Y0_bar_doA0: ", get_Y0_bar_doA0(YMAU))

# Below for (e)
def get_YAU(YMAU):
    YAU = {}
    for y in [0,1]:
        for a in [0,1]:
            for u in [0,1]:
                YAU[(y,a,u)] = sum([YMAU[(y,m,a,u)] for m in [0,1]])
    return YAU

YAU = get_YAU(YMAU)
print("YAU: ", YAU, sum(YAU.values()))

def get_Y_bar_AU(YAU, AU, y, a, u):
    if AU[(a,u)] != 0:
        return YAU[(y,a,u)]/AU[(a,u)]
    else:
        return 0

print("Y1_bar_A1U1: ", get_Y_bar_AU(YAU, AU, 1, 1, 1))
print("Y0_bar_A1U1: ", get_Y_bar_AU(YAU, AU, 0, 1, 1))

print("Y1_bar_A1U0: ", get_Y_bar_AU(YAU, AU, 1, 1, 0))
print("Y0_bar_A1U0: ", get_Y_bar_AU(YAU, AU, 0, 1, 0))

print("Y1_bar_A0U1: ", get_Y_bar_AU(YAU, AU, 1, 0, 1))
print("Y0_bar_A0U1: ", get_Y_bar_AU(YAU, AU, 0, 0, 1))

print("Y1_bar_A0U0: ", get_Y_bar_AU(YAU, AU, 1, 0, 0))
print("Y0_bar_A0U0: ", get_Y_bar_AU(YAU, AU, 0, 0, 0))

print("Y1_bar_doA1: ", get_Y_bar_AU(YAU, AU, 1, 1, 1)*1/2 + get_Y_bar_AU(YAU, AU, 1, 1, 0)*1/2)
print("Y1_bar_doA0: ", get_Y_bar_AU(YAU, AU, 1, 0, 1)*1/2 + get_Y_bar_AU(YAU, AU, 1, 0, 0)*1/2)