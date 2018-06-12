import cv2
import numpy as np

picin = cv2.imread('1.jpg')
picori=picin.copy()
print(picin.shape)
print(picin[100][100])
print(picin[100][101])
print(picin[100][102])
loss=np.zeros(picin.shape[:2])
disp=np.zeros(picin.shape)


def diff(picin,i,j):
    '''
        for r in range(3):
            diff+=int(abs(int(picin[i][j+1][r])-int(picin[i][j][r])))
        for r in range(3):
            diff+=int(abs(int(picin[i+1][j][r])-int(picin[i][j][r])))
    '''
    did=abs(int(picin[i][j+1][0])+int(picin[i][j+1][1])+int(picin[i][j+1][2])-int(picin[i][j][0])-int(picin[i][j][1])-int(picin[i][j][2]))
    return did



for i in range(picin.shape[0]-1):
    for j in range(picin.shape[1]-1):#loss的最后一行最后一列为0
        loss[i][j]=diff(picin,i,j)

for i in range(picin.shape[0]-1):   #修正最后一列
    loss[i][picin.shape[1]-1]=loss[i][picin.shape[1]-2]


summ=np.zeros(picin.shape[:2])
last=np.ones(picin.shape[:2],dtype='int32') #debug,其实可以不初始化

for step in range(picin.shape[0]-10):
    for j in range(picin.shape[1]-step):    #范围:全
        summ[0][j]=loss[0][j]
    for i in range(picin.shape[0]-1):               #范围:i+1顶到头 最后一行是有summ和last的 第一行没有
        for j in range(picin.shape[1]-step):    #范围:全
            summ[i+1][j]=summ[i][max(j-1,0)]
            last[i+1][j]=max(j-1,0)
            for r in range(j,min(j+2,picin.shape[1]-1-step)):
                if summ[i][r]<summ[i+1][j]:       #取三个的最小值
                    summ[i+1][j]=summ[i][r]
                    last[i+1][j]=r                #存放上面一排的位置
            summ[i+1][j]+=loss[i+1][j]
            

    minsum=10000000000
    for j in range(1,picin.shape[1]-1-step):        #因为第一列和最后一列没有,范围缩小,缩小掉黑边
        if summ[picin.shape[0]-1][j]<minsum:
            minsum=summ[picin.shape[0]-1][j]
            oldm=j


#显示图片
    minpos=oldm
    for i in range(picin.shape[0]-1,-1,-1):
        if(step==1):
            for r in range(3):
                picin[i][minpos][r]=0
        else:
            picin[i][minpos][0]=0
            picin[i][minpos][1]=255
            picin[i][minpos][2]=0

        loss[i][minpos]=10000
        minpos=last[i][minpos]
    cv2.imshow('1',picin)
    cv2.waitKey(1)


    minpos=oldm
    '''
    for i in range(picin.shape[0]-1,-1,-1):             #从最底下一直到最上面
        for j in range(minpos,picin.shape[1]-1-step):   #一行的像素左移
            for r in range(3):
                picin[i][j][r]=picin[i][j+1][r]
            loss[i][j]=loss[i][j+1]                    #loss左移
        for r in range(3):
            picin[i][picin.shape[1]-1-step][r]=0        #最左边抹黑
        minpos=last[i][minpos]                         #更新minpos
#        print('mp2:',minpos)
'''
#    input()
    minpos=oldm
#    loss2=loss[:]#debug
    #更新loss
    '''
    for i in range(picin.shape[0]-2,-1,-1):             #i不能从头到尾了因为计算loss i最后一行没有
        for j in range(minpos-1,minpos):                #j其实是一个数
            loss[i][j]=diff(picin,i,j)
        minpos=last[i][minpos]                         #更新minpos
#        print('mp:',minpos)
        '''

    cv2.imwrite('1'+str(step)+'.jpg',picin)



    minpos=oldm
    if(step==1):
        for i in range(picin.shape[0]-1,-1,-1):
            for r in range(3):
                picori[i][minpos][r]=0
            loss[i][minpos]=10000
            minpos=last[i][minpos]
        cv2.imwrite('1a'+str(step)+'.jpg',picori)
        print('fiin')
        input()







    print(step)


    
    

#cv2.imshow('pic',picin)
cv2.imshow('pic',picin)
cv2.waitKey()
