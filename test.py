from scipy import spatial
resultarray=[[],[],[],[]]
array=[[581,48],[225,48],[215,416],[570,401]]
imgsize=[[0,0],[720,0],[0,480],[720,480]]
tree=spatial.KDTree(array)
for x in range(0,4):
    _,result=tree.query(imgsize[x])
    resultarray[x]=array[result]


