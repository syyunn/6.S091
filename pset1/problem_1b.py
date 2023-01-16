class Bernoulli:
    def __init__(self, p=0.5):
        self.p = p

    def __call__(self, x):
        if x == 0:
            return 1 - self.p
        elif x == 1:
            return self.p
        else:
            return None


class CondProb:
    def __init__(self, A=[0,1], B=[0,1], C=None, f=lambda x: x/4):
        self.A = A
        self.B = B
        self.C = C
        if C:
            self.C = C
        self.f = f
        self.CondProb = {}
        for a in A:
            for b in B:
                if C:
                    for c in C:
                        ber = Bernoulli(f(b, c))
                        self.CondProb[(a,b,c)] = ber(a)
                else:
                    ber = Bernoulli(f(b))
                    self.CondProb[(a,b)] = ber(a)

    def __call__(self, a, b, c=None):
        if self.C:
            return self.CondProb[(a,b,c)]
        else:
            return self.CondProb[(a,b)]

if __name__ == "__main__":
    # f = Bernoulli(0.7)
    # print(f(0))

    prob_A_bar_U = CondProb(A=[0,1], B=[0,1], f=lambda x: x/4)
    print(prob_A_bar_U(1,1))

    prob_M_bar_A = CondProb(A=[0,1], B=[0,1], f=lambda x: 0.5 + 0.1*x)
    print(prob_M_bar_A(1,1))

    prob_Y_bar_M_U = CondProb(A=[0,1], B=[0,1], C=[0,1], f=lambda x, y: 0.5*x + 0.25*y)
    print(prob_Y_bar_M_U(1,0,0))
    print(prob_Y_bar_M_U(1,0,1))
