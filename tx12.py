import cv2
import numpy as np

picin = cv2.imread('1.jpg')
print(picin.shape)
print(picin[100][100])
print(picin[100][101])
print(picin[100][102])
loss=np.zeros(picin.shape[:2])

for i in range(picin.shape[0]):
    for j in range(picin.shape[1]-1):
        for r in range(3):
            loss[i][j]+=abs(int(picin[i][j+1][r])-int(picin[i][j][r]))/3/255        #每个loss是0到1的

for step in range(picin.shape[0]-10):
    summ=np.ones(picin.shape[:2])*10000                 #重新初始化sum
    last=np.zeros(picin.shape[:2],dtype='int32')

    for i in range(picin.shape[0]-1):
        for j in range(1,picin.shape[1]-1-step):
            for r in range(-1,2):
                if loss[i][j+r]<summ[i+1][j]:       #取三个的最小值
                    summ[i+1][j]=loss[i][j+r]
                    last[i+1][j]=j+r                #存放上面一排的位置
            summ[i+1][j]+=loss[i+1][j]
    minsum=10000
    for j in range(1,picin.shape[1]-1-step):
        if summ[picin.shape[0]-1][j]<minsum:
            minsum=summ[picin.shape[0]-1][j]
            oldm=j

    minpos=oldm

#显示图片
    for i in range(picin.shape[0]-1,-1,-1):
        for r in range(3):
            picin[i][minpos][r]=0
        minpos=last[i][minpos]
    cv2.imshow('1',picin)
    cv2.waitKey(1)


    minpos=oldm
    for i in range(picin.shape[0]-1,-1,-1):
        for j in range(minpos,picin.shape[1]-1-step):   #一行的像素左移
            for r in range(3):
                picin[i][j][r]=picin[i][j+1][r]
            loss[i][j]=loss[i][j+1]                    #loss左移
        for r in range(3):
            picin[i][picin.shape[1]-1-step][r]=0        #最左边抹黑
        minpos=last[i][minpos]                         #更新minpos
#        print('mp2:',minpos)

#    input()
    minpos=oldm
    loss2=loss[:]#debug

    for i in range(picin.shape[0]-1,-1,-1):
        for j in range(minpos-1,minpos):
            loss[i][j]=0
            for r in range(3):
                loss[i][j]+=abs(int(picin[i][j+1][r])-int(picin[i][j][r]))/3/255  #重新计算loss 
        minpos=last[i][minpos]                         #更新minpos
#        print('mp:',minpos)

    '''
    for i in range(picin.shape[0]):#debug
        for j in range(picin.shape[1]-2-step):
            temp=0
            for r in range(3):
                temp+=abs(int(picin[i][j+1][r])-int(picin[i][j][r]))/3/255        #debug
            if not temp==loss[i][j]:
                print(temp,loss[i][j],i,j)
                raise Exception
'''
    cv2.imwrite('1'+str(step)+'.jpg',picin)
    print(step)


    
    

#cv2.imshow('pic',picin)
cv2.imshow('pic',picin)
cv2.waitKey()
