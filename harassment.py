class Down_Bend:
    def __int__(self):
        with open("size.txt") as sz:
            p = sz.read().split(' ')
            self.m = int(p[0])
            self.n = int(p[1])
            self.r=int(p[2])

        #读入劳动力资源，交通成本和政权
        self.M = [[0.0 for i in range(self.n)] for i in range(self.m)]
        self.X = [[0.0 for i in range(self.n)] for i in range(self.m)]
        self.ID = [[0 for i in range(self.n)] for i in range(self.m)]
        with open('labor.txt')as lb, open('transportation.txt')as tr, open('regime.txt')as rg:
            for i in range(self.m):
                s_lb = lb.readline().split('\t')
                s_tr = tr.readline().split('\t')
                s_rg = rg.readline().split('\t')
                for j in range(self.n):
                    self.M[i][j] = float(s_lb[j])
                    self.X[i][j] = float(s_tr[j])
                    self.ID[i][j] = int(s_rg[j])