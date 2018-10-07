from init import  Bend
bend=Bend()
bend.cal_mr()
bend.evolution()
for i in range(bend.m):
    for j in range(bend.n):
        print(bend.ID[i][j]," ",end="")
    print()
