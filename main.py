from init import  Bend
bend=Bend()
bend.cal_mr()
'''bend.evolution()
for i in range(bend.m):
    for j in range(bend.n):
        print(bend.ID[i][j]," ",end="")
    print()
'''
bend.init_harassment()
bend.cal_harassment()
bend.harass()
bend.last_work()
for i in range(bend.r):
    for j in range(bend.r):
        print(bend.gain[i][j]," ",end="")
    print()