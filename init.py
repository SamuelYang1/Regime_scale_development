#读入数据规模
with open("size.txt") as sz:
    p = sz.read().split(' ')
    m = int(p[0])
    n = int(p[1])
    r=int(p[2])

#读入劳动力资源，交通成本和政权
L = [[0 for i in range(n)] for i in range(m)]
T = [[0 for i in range(n)] for i in range(m)]
ID = [[0 for i in range(n)] for i in range(m)]
with open('labor.txt')as lb, open('transportation.txt')as tr, open('regime.txt')as rg:
    for i in range(m):
        s_lb = lb.readline().split(' ')
        s_tr = tr.readline().split(' ')
        s_rg = rg.readline().split(' ')
        for j in range(n):
            L[i][j] = float(s_lb[j])
            T[i][j] = float(s_tr[j])
            ID[i][j] = int(s_rg[j])

#初始化边缘带表
Out_border=[[] for i in range(r)]
In_border=[[] for i in range(r)]
for i in range(m):
    for j in range(n):
        Is_in_border=False
        if i-1>=0 and ID[i-1][j]!=ID[i][j]:
            Is_in_border=True
            if Out_border[ID[i-1][j]].count((i,j))==0:
                Out_border[ID[i-1][j]].append((i,j))
        if j - 1 >= 0 and ID[i][j-1] != ID[i][j]:
            Is_in_border = True
            if Out_border[ID[i][j-1]].count((i, j)) == 0:
                Out_border[ID[i][j-1]].append((i, j))
        if i+1<m and ID[i+1][j]!=ID[i][j]:
            Is_in_border=True
            if Out_border[ID[i+1][j]].count((i,j))==0:
                Out_border[ID[i+1][j]].append((i,j))
        if j+1<n and ID[i][j+1]!=ID[i][j]:
            Is_in_border=True
            if Out_border[ID[i][j+1]].count((i,j))==0:
                Out_border[ID[i][j+1]].append((i,j))
        if Is_in_border:
            In_border[ID[i][j]]=(i,j)

#联盟关系暂略
