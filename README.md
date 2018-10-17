# Regime_scale_development
一只弯曲而已\
init.py变量解释：\
War_border[id]=[(x,y)] 政权id的战争带坐标\
War=[(x,y)] 所有战争带坐标\
Move[x][y]=[(p,q,l)] (x,y)分配方案，(p,q)为被分配栅格，l为劳力\
K[id][x][y]=float 栅格(x,y)所分配的id国的总劳力\
Dis[x][y]=float (x,y)被分配的劳力的最大值与次大值之差\
Advantage[x][y]=int (x,y)优势政权id\
moved[id][x][y]=[(i,j)] id所有分配劳力到(x,y)的栅格\
War_re[x][y]=[id] 交战带(x,y)的相关交战国\
Disadvantage[id]=[(x,y)] 劣势表\
cmp_advantage 比较优势表


