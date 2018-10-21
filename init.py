import math
import networkx as nx
def cm(a):
    ((x, y), id, (x1, y1), (x2, y2), tmp1)=a
    return tmp1
def cm3(a):
    (x,y, tmp1) = a
    return tmp1
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
    def init_war_border(self):#交战带确定
        # 分配
        allocate = [[[0.0 for i in range(self.n)] for i in range(self.m)] for i in range(self.r)]
        for i in range(self.m):
            for j in range(self.n):
                id = self.ID[i][j]
                max_profit = 0.0
                mx = 0
                my = 0
                for (x,y) in self.In_border[id]:
                    if self.path_length[i][j][x][y] * self.L[x][y] > max_profit:
                        max_profit = self.path_length[i][j][x][y] * self.L[x][y]
                        mx = x
                        my = y
                allocate[id][mx][my] += self.path_length[i][j][mx][my] * self.L[i][j]
                max_profit = 0.0
                for (x,y) in self.Out_border[id]:
                    if self.path_length[i][j][x][y] * self.L[x][y] > max_profit:
                        max_profit = self.path_length[i][j][x][y] * self.L[x][y]
                        mx = x
                        my = y
                allocate[id][mx][my] += self.path_length[i][j][mx][my] * self.L[i][j]
        # 交战带确定
        self.War_border = [[] for i in range(self.r)]
        self.War = []
        self.War_re=[[[] for i in range(self.n)]for i in range(self.m)]
        for id in range(self.r):
            for (x,y) in self.Out_border[id]:
                b_id = self.ID[x][y]
                if allocate[id][x][y] > allocate[b_id][x][y]:
                    if self.War_border[id].count((x, y)) == 0:
                        self.War_border[id].append((x, y))
                    if self.War_border[b_id].count((x, y)) == 0:
                        self.War_border[b_id].append((x, y))
                    if self.War_re[x][y].count(id)==0:
                        self.War_re[x][y].append(id)
                    if self.War_re[x][y].count(b_id) == 0:
                        self.War_re[x][y].append(b_id)
                    if self.War.count((x, y)) == 0:
                        self.War.append((x, y))
    def init_allocate(self):
        self.moved = [[[[] for i in range(self.n)] for i in range(self.m)] for i in range(self.r)]
        self.K = [[[0.0 for i in range(self.n)] for i in range(self.m)] for i in range(self.r)]
        for i in range(self.m):
            for j in range(self.n):
                id = self.ID[i][j]
                for (x,y,l) in self.move[i][j]:
                    self.K[id][x][y]+=l*self.path_length[i][j][x][y]
                    self.moved[id][x][y].append((i,j))
        self.Dis=[[0.0 for i in range(self.n)] for i in range(self.m)]
        self.Advantage=[[0 for i in range(self.n)] for i in range(self.m)]
        self.Disadvantage=[[]for i in range(self.r)]
        for (x,y) in self.War:
            max1=0
            max2=0
            for id in self.War_re[x][y]:
                if max1<self.K[id][x][y]:
                    max2=max1
                    max1=self.K[id][x][y]
                    self.Advantage[x][y]=id
                elif max2<self.K[id][x][y]:
                    max2=self.K[id][x][y]
            self.Dis[x][y]=max1-max2
            for id in self.War_re[x][y]:
                if id!=self.Advantage[x][y]:
                    self.Disadvantage[id].append((x,y))
    def init_cmp_advantage(self):
        self.cmp_advantage=[]
        for (x,y) in self.War:
            id=self.Advantage[x][y]
            minn=1e9+0.1
            added = ((0, 0), 0, (0, 0), (0, 0), 0.0)
            for (x1,y1) in self.moved[id][x][y]:
                if self.L[x1][y1]>0:
                    for (x2,y2) in self.Disadvantage[id]:
                        tmp=self.path_length[x1][y1][x][y]*self.L[x][y]-self.path_length[x1][y1][x2][y2]*self.L[x2][y2]
                        #到底这玩意要不要大于0
                        if tmp<minn and tmp>0:
                            minn=tmp
                            added=((x,y),id,(x1,y1),(x2,y2),tmp)
            if minn!=1e9+0.1:
                self.cmp_advantage.append(added)
        self.cmp_advantage.sort(key=cm)
    def pure(self,x,y):
        i=0
        while i<len(self.move[x][y])-1:
            (xi,yi,tmpi)=self.move[x][y][i]
            j=i+1
            while j<len(self.move[x][y]):
                (xj,yj,tmpj)=self.move[x][y][j]
                if xi==xj and yi==yj:
                    tmpi+=tmpj
                    self.move[x][y].pop(j)
                else:
                    j+=1
            self.move[x][y][i]=(xi,yi,tmpi)
            i+=1
    def change(self):
        Out_Disadvantage=[[]for i in range(self.r)]
        In_Disadvantage=[[]for i in range(self.r)]
        changed1=True
        done=False
        num=0
        while changed1:
            changed1=False
            num+=1
            if len(self.cmp_advantage)>0:
                print("第",num,"次分配，优势表长：",len(self.cmp_advantage),"，第一个值：",self.cmp_advantage[0])
            for ((x,y),id,(x1,y1),(x2,y2),tmp) in self.cmp_advantage:
                if (self.Dis[x][y]<0.02):
                    continue
                elif len(self.Disadvantage[id])>0:
                    ind=-1
                    lap=0.0
                    for i in range(len(self.move[x1][y1])):
                        (xx,yy,lap)=self.move[x1][y1][i]
                        if xx==x and yy==y:
                            ind=i
                            break
                    if lap*self.path_length[x1][y1][x][y]<self.Dis[x][y]-0.01:
                        self.move[x1][y1].pop(ind)
                        self.move[x1][y1].append((x2, y2, lap))
                    else:
                        for ip in range(len(self.alloc_order[x1][y1])):
                            (p,q,wwww)=self.alloc_order[x1][y1][ip]
                            if p==x and q==y:
                                (p, q, wwww) = self.alloc_order[x1][y1][ip+1]
                                self.move[x1][y1].pop(ind)
                                self.move[x1][y1].append((x,y,(self.Dis[x][y]-0.01)/self.path_length[x1][y1][x][y]))
                                self.move[x1][y1].append((p, q, lap-(self.Dis[x][y] - 0.01) / self.path_length[x1][y1][x][y]))
                                break
                    self.pure(x1,y1)
                    self.init_allocate()
                    self.init_cmp_advantage()
                    changed1=True
                    break
            if (not done) and (not changed1):
                for i in range(self.r):
                    for (x,y) in self.Disadvantage[i]:
                        if i!=self.ID[x][y]:
                            Out_Disadvantage[i].append((x,y))
                        else:
                            In_Disadvantage[i].append((x,y))
                for x in range(self.m):
                    for y in range(self.n):
                        i=self.ID[x][y]
                        if len(In_Disadvantage[i])>0 and len(Out_Disadvantage[i])>0:
                            #先找(x,y)的边际效益最优的栅格
                            mx=-1
                            my=-1
                            max_profit=0.0
                            for (xx,yy) in self.War:
                                if self.War_re[xx][yy].count(i)>0 and Out_Disadvantage[i].count((xx,yy))==0:
                                    tmp=self.path_length[x][y][xx][yy]*self.L[xx][yy]
                                    if tmp>max_profit:
                                        max_profit=tmp
                                        mx=xx
                                        my=yy
                            #再删除(x,y)分配表move中的劣势栅格
                            ind=0
                            sum=0.0
                            while ind<len(self.move[x][y]):
                                (xx,yy,ll)=self.move[x][y][ind]
                                if Out_Disadvantage[i].count((xx,yy))>0:
                                    sum+=ll
                                    self.move[x][y].pop(ind)
                                ind+=1
                            self.move[x][y].append((mx,my,sum))
                            self.pure(x,y)
                self.init_allocate()
                self.init_cmp_advantage()
                done=True
                changed1=True
        changed1=False
        for (x,y) in self.War:
            if self.ID[x][y]!=self.Advantage[x][y]:
                self.ID[x][y]=self.Advantage[x][y]
                changed1=True
        return changed1
    def evolution(self):
        changed=True
        num=0
        while changed:
            self.init_boder()
            print("第",num,"轮演化")
            num += 1
            s="output/result"+str(num)+".txt"
            with open(s,"w+") as op:
                for i in range(self.m):
                    for j in range(self.n):
                        op.write(str(self.ID[i][j])+'\t')
                    op.write('\n')
            self.init_war_border()
            #生成分配次序表
            self.alloc_order=[[[] for i in range(self.n)] for i in range(self.m)]
            for i in range(self.m):
                for j in range(self.n):
                    id = self.ID[i][j]
                    for (x,y) in self.War_border[id]:
                        self.alloc_order[i][j].append((x,y,self.path_length[i][j][x][y]*self.L[x][y]))
                    self.alloc_order[i][j].sort(key=cm3,reverse=True)
            #初始分配
            self.move=[[[] for i in range(self.n)] for i in range(self.m)]
            for i in range(self.m):
                for j in range(self.n):
                    max_profit = 0.0
                    mx = -1
                    my = 0
                    for (x, y, profit) in self.alloc_order[i][j]:
                        if profit > max_profit:
                            mx = x
                            my = y
                            max_profit = profit
                    if mx!=-1:
                        self.move[i][j].append((mx,my,self.L[i][j]))
            self.init_allocate()
            self.init_cmp_advantage()
            print ("start")
            changed=self.change()
    ####
    def pure2(self,x,y):
        i=0
        while i<len(self.harassment_send[x][y])-1:
            (xi,yi,tmpi)=self.harassment_send[x][y][i]
            j=i+1
            while j<len(self.harassment_send[x][y]):
                (xj,yj,tmpj)=self.harassment_send[x][y][j]
                if xi==xj and yi==yj:
                    tmpi+=tmpj
                    self.harassment_send[x][y].pop(j)
                else:
                    j+=1
            self.harassment_send[x][y][i]=(xi,yi,tmpi)
            i+=1
    def init_harassment(self):
        self.M = [[0.0 for i in range(self.n)] for i in range(self.m)]
        self.X = [[0.0 for i in range(self.n)] for i in range(self.m)]
        with open('army.txt')as ar:
            for i in range(self.m):
                s_ar = ar.readline().split('\t')
                for j in range(self.n):
                    self.M[i][j] = float(s_ar[j])
                    self.X[i][j] = self.L[i][j]-self.M[i][j]
    def cal_harassment(self):
        self.harassment=[[[]for i in range(self.n)]for i in range(self.m)]
        self.P=[[[[0.0 for i in range(self.n)] for i in range(self.m)] for i in range(self.n)] for i in range(self.m)]
        self.cell=[[]for i in range(self.r)]
        for ai in range(self.m):
            for aj in range(self.n):
                id=self.ID[ai][aj]
                self.cell[id].append((ai,aj))
                for bi in range(self.m):
                    for bj in range(self.n):
                        if self.ID[ai][aj]!=self.ID[bi][bj] and self.L[bi][bj]!=0:
                            if self.M[bi][bj]!=0:
                                tmp=self.path_length[ai][aj][bi][bj]*self.X[bi][bj]/self.M[bi][bj]
                            else:
                                tmp=1e9
                            self.P[ai][aj][bi][bj]=tmp
                            self.harassment[ai][aj].append((bi,bj,tmp))
                self.harassment[ai][aj].sort(key=cm3,reverse=True)
    def init_harassment_rec(self):
        self.harassment_rec = [[[] for i in range(self.n)] for i in range(self.m)]
        for x in range(self.m):
            for y in range(self.n):
                for (a,b,c) in self.harassment_send[x][y]:
                    if a!=-1 and b!=-1:
                        self.harassment_rec[a][b].append((x,y,c))
    def harass(self):
        self.harassment_send=[[[]for i in range(self.n)]for i in range(self.m)]
        for i in range(self.m):
            for j in range(self.n):
                self.harassment_send[i][j].append((-1,-1,self.M[i][j]))
        for id in range(self.r):
            print("id=",id)
            for (x,y) in self.cell[id]:
                i=0
                sum=0.0
                while i<len(self.harassment_send[x][y]):
                    (xx,yy,zz)=self.harassment_send[x][y][i]
                    if xx==-1 and yy==-1:
                        self.harassment_send[x][y].pop(i)
                        sum+=zz
                    else:
                        i+=1
                (bx,by,bz)=self.harassment[x][y][0]
                self.harassment_send[x][y].append((bx,by,sum))
            self.init_harassment_rec()
            ck=False
            while not ck:
                #4.2
                self.diff = [[[] for i in range(self.n)] for i in range(self.m)]
                for bx in range(self.m):
                    for by in range(self.n):
                        for (ax,ay,az) in self.harassment_rec[bx][by]:
                            self.diff[bx][by].append((ax,ay,self.P[ax][ay][bx][by]))
                        self.diff[bx][by].sort(key=cm3,reverse=True)
                #4.3
                for bx in range(self.m):
                    for by in range(self.n):
                        if self.ID[x][y]!=self.ID[bx][by]:
                            summ = 0.0
                            for (ax,ay,az) in self.harassment_rec[bx][by]:
                                summ+=az*self.path_length[ax][ay][bx][by]
                            if summ<=self.M[bx][by]:
                                continue
                            else:
                                temp=self.M[bx][by]
                                (a1x,a1y,a1z)=self.diff[bx][by][0]
                                (a2x,a2y,a2z)=self.diff[bx][by][1]
                                num=-1
                                for (xx,yy,zz) in self.harassment_rec[bx][by]:
                                    if xx==a1x and yy==a1y:
                                        temp-=zz*self.path_length[a1x][a1y][bx][by]
                                        num=0
                                        break
                                step=-1.0
                                for (xx,yy,zz) in self.harassment_rec[bx][by]:
                                    if xx==a2x and yy==a2y:
                                        step=zz
                                        break
                                while temp>1e-6:
                                    temp-=step*self.path_length[a2x][a2y][bx][by]
                                    num=1
                                if temp<-1e-6:
                                    (ax,ay,az)=self.diff[bx][by][num]
                                    for ind in range(len(self.harassment_send[ax][ay])):
                                        (xx, yy, zz)=self.harassment_send[ax][ay][ind]
                                        if xx==bx and yy==by:
                                            zz+=temp/self.path_length[ax][ay][bx][by]
                                            self.harassment_send[ax][ay][ind]=(xx,yy,zz)
                                            (xx, yy, zz)=self.harassment[ax][ay][0]
                                            if xx==bx and yy==by:
                                                self.harassment[ax][ay].pop(0)
                                            self.harassment_send[ax][ay].append((-1,-1,-temp/self.path_length[ax][ay][bx][by]))
                                            self.pure2(ax,ay)
                                            break
                                else:
                                    num+=1
                                    while num<len(self.diff[bx][by]):
                                        (ax, ay, az) = self.diff[bx][by][num]
                                        (xx, yy, zz) = self.harassment[ax][ay][0]
                                        if xx == bx and yy == by:
                                            self.harassment[ax][ay].pop(0)
                                        for ind in range(len(self.harassment_send[ax][ay])):
                                            (xx, yy, zz) = self.harassment_send[ax][ay][ind]
                                            if xx == bx and yy == by:
                                                self.harassment_send[ax][ay].pop(ind)
                                                self.harassment_send[ax][ay].append((-1, -1,zz))
                                                self.pure2(ax,ay)
                                                break
                                        num+=1
                                self.init_harassment_rec()
                #4.10
                ck=True
                for bx in range(self.m):
                    for by in range(self.n):
                        sum=0.0
                        for (xx,yy,zz) in self.harassment_rec[bx][by]:
                            sum+=zz
                        if sum>self.M[bx][by]:
                            ck=False
                            break
                    if not ck:
                        break
    def last_work(self):
        self.gain=[[0.0 for i in range(self.r)]for i in range(self.r)]
        for i in range(self.m):
            for j in range(self.n):
                ida=self.ID[i][j]
                for (x,y,z) in self.harassment_send[i][j]:
                    idb=self.ID[x][y]
                    tmp=z/self.M[x][y]*self.path_length[i][j][x][y]*self.X[x][y]
                    self.gain[ida][idb]+=tmp
                    self.gain[idb][ida]-=tmp
