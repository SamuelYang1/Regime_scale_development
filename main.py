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
with open("hresult.txt","w+") as op:
    for i in range(bend.r):
        for j in range(bend.r):
            op.write(str(bend.gain[i][j])+'\t')
        op.write('\n')