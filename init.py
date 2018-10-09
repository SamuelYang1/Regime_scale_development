import math
import networkx as nx
class Bend:
    def __init__(self):
        #读入数据规模
        with open("size.txt") as sz:
            p = sz.read().split(' ')
            self.m = int(p[0])
            self.n = int(p[1])
            self.r=int(p[2])

        #读入劳动力资源，交通成本和政权
        self.L = [[0.0 for i in range(self.n)] for i in range(self.m)]
        self.T = [[0.0 for i in range(self.n)] for i in range(self.m)]
        self.ID = [[0 for i in range(self.n)] for i in range(self.m)]
        with open('labor.txt')as lb, open('transportation.txt')as tr, open('regime.txt')as rg:
            for i in range(self.m):
                s_lb = lb.readline().split('\t')
                s_tr = tr.readline().split('\t')
                s_rg = rg.readline().split('\t')
                for j in range(self.n):
                    self.L[i][j] = float(s_lb[j])
                    self.T[i][j] = float(s_tr[j])
                    self.ID[i][j] = int(s_rg[j])
        self.init_boder()
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
                    self.In_border[self.ID[i][j]].append ((i, j))
    def cal_mr(self):
        # 边际收益
        sq2=math.sqrt(2)
        self.path_length = [[[[0.0 for i in range(self.n)] for i in range(self.m)] for i in range(self.n)] for i in range(self.m)]
        Tr = [[0.0 for i in range(self.n)] for i in range(self.m)]
        for i in range(self.m):
            for j in range(self.n):
                Tr[i][j]=-math.log(self.T[i][j])
        G = nx.Graph()
        for i in range(self.m):
            for j in range(self.n):
                if i-1>=0:
                    G.add_edge((i,j),(i-1,j),weight=(Tr[i][j]+Tr[i-1][j])/2)
                if j-1>=0:
                    G.add_edge((i,j),(i,j-1),weight=(Tr[i][j]+Tr[i][j-1])/2)
                    if i-1>=0:
                        G.add_edge((i, j), (i - 1, j-1), weight=(Tr[i][j] + Tr[i - 1][j-1]) / 2*sq2)
                    if i+1<self.m:
                        G.add_edge((i, j), (i + 1, j - 1), weight=(Tr[i][j] + Tr[i + 1][j - 1]) / 2 * sq2)
        print("cal_mr start")
        p=dict(nx.shortest_path_length(G,weight="weight"))
        for i in range(self.m):
            for j in range(self.n):
                a=(i,j)
                for x in range(self.m):
                    for y in range(self.n):
                        b=(x,y)
                        self.path_length[i][j][x][y]=math.exp(-p[a][b]+Tr[i][j]/2)
        print("cal_mr end")
    def evolution(self):
        changed=True
        num=0
        while changed:
            num+=1
            print("第",num,"轮演化")
            s="output/result"+str(num)+".txt"
            with open(s,"w+") as op:
                for i in range(self.m):
                    for j in range(self.n):
                        op.write(str(self.ID[i][j])+'\t')
                    op.write('\n')
            # 分配
            self.allocate = [[[0.0 for i in range(self.n)] for i in range(self.m)] for i in range(self.r)]
            for i in range(self.m):
                for j in range(self.n):
                    id = self.ID[i][j]
                    max_profit = 0.0
                    mx=0
                    my=0
                    for k in self.In_border[id]:
                        (x, y) = k
                        if self.path_length[i][j][x][y]*self.L[x][y] > max_profit:
                            max_profit = self.path_length[i][j][x][y]*self.L[x][y]
                            mx = x
                            my = y
                    self.allocate[id][mx][my] += self.path_length[i][j][mx][my]*self.L[i][j]
                    max_profit = 0.0
                    for k in self.Out_border[id]:
                        (x, y) = k
                        if self.path_length[i][j][x][y]*self.L[x][y] > max_profit:
                            max_profit = self.path_length[i][j][x][y]*self.L[x][y]
                            mx = x
                            my = y
                    self.allocate[id][mx][my] += self.path_length[i][j][mx][my]*self.L[i][j]
            #演化
            changed=False
            for id in range(self.r):
                for k in self.Out_border[id]:
                    (x,y)=k
                    new_id=self.ID[x][y]
                    for i in range(self.r):
                        if self.allocate[i][x][y]>self.allocate[new_id][x][y]:
                            new_id=i
                            changed=True
                    self.ID[x][y]=new_id
            self.init_boder()