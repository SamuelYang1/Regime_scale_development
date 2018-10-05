class Bend:
    def __init__(self):
        #读入数据规模
        with open("size.txt") as sz:
            p = sz.read().split(' ')
            self.m = int(p[0])
            self.n = int(p[1])
            self.r=int(p[2])

        #读入劳动力资源，交通成本和政权
        self.L = [[0 for i in range(self.n)] for i in range(self.m)]
        self.T = [[0 for i in range(self.n)] for i in range(self.m)]
        self.ID = [[0 for i in range(self.n)] for i in range(self.m)]
        with open('labor.txt')as lb, open('transportation.txt')as tr, open('regime.txt')as rg:
            for i in range(self.m):
                s_lb = lb.readline().split(' ')
                s_tr = tr.readline().split(' ')
                s_rg = rg.readline().split(' ')
                for j in range(self.n):
                    self.L[i][j] = float(s_lb[j])
                    self.T[i][j] = float(s_tr[j])
                    self.ID[i][j] = int(s_rg[j])

    def init_boder(self):
        # 初始化边缘带表
        self.Out_border = [[] for i in range(self.r)]
        self.In_border = [[] for i in range(self.r)]
        for i in range(self.m):
            for j in range(self.n):
                Is_in_border = False
                if i - 1 >= 0 and self.ID[i - 1][j] != self.ID[i][j]:
                    Is_in_border = True
                    if self.Out_border[self.ID[i - 1][j]].count((i, j)) == 0:
                        self.Out_border[self.ID[i - 1][j]].append((i, j))
                if j - 1 >= 0 and self.ID[i][j - 1] != self.ID[i][j]:
                    Is_in_border = True
                    if self.Out_border[self.ID[i][j - 1]].count((i, j)) == 0:
                        self.Out_border[self.ID[i][j - 1]].append((i, j))
                if i + 1 < self.m and self.ID[i + 1][j] != self.ID[i][j]:
                    Is_in_border = True
                    if self.Out_border[self.ID[i + 1][j]].count((i, j)) == 0:
                        self.Out_border[self.ID[i + 1][j]].append((i, j))
                if j + 1 < self.n and self.ID[i][j + 1] != self.ID[i][j]:
                    Is_in_border = True
                    if self.Out_border[self.ID[i][j + 1]].count((i, j)) == 0:
                        self.Out_border[self.ID[i][j + 1]].append((i, j))
                if Is_in_border:
                    self.In_border[self.ID[i][j]] = (i, j)
    def cal_mr(self):
        # 边际收益，一通乱搞，暂时不写
        self.marginal_revenue = [[[[0 for i in range(self.n)] for i in range(self.m)] for i in range(self.n)] for i in range(self.m)]
    def evolution(self):
        changed=True
        while changed:
            changed=False
            # 分配
            self.allocate = [[[0 for i in range(self.n)] for i in range(self.m)] for i in range(self.r)]
            for i in range(self.m):
                for j in range(self.n):
                    id = self.ID[i][j]
                    mx, my = 0
                    max_profit = 0.0
                    for k in self.In_border[id]:
                        (x, y) = k
                        if self.marginal_revenue[i, j, x, y] > max_profit:
                            max_profit = self.marginal_revenue[i, j, x, y]
                            mx = x
                            my = y
                    self.allocate[id][mx][my] += max_profit
                    mx, my = 0
                    max_profit = 0.0
                    for k in self.Out_border[id]:
                        (x, y) = k
                        if self.marginal_revenue[i, j, x, y] > max_profit:
                            max_profit = self.marginal_revenue[i, j, x, y]
                            mx = x
                            my = y
                    self.allocate[id][mx][my] += max_profit
            #演化
            changed=False
            for id in range(self.r):
                for k in self.Out_border[id]:
                    (x,y)=k
                    new_id=id
                    for i in range(self.r):
                        if self.allocate[i][x][y]>self.allocate[new_id][x][y]:
                            new_id=i
                            chanegd=True
                    self.ID[x][y]=new_id
            self.cal_mr()
