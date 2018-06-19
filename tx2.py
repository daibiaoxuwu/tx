import cv2
import numpy as np
import sys

picin = cv2.imread('1.jpg')
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



def main():
    lenth=picin.shape[0]
    width=picin.shape[1]
    for i in range(lenth-1):
        for j in range(width-1):#loss的最后一行最后一列为0
            loss[i][j]=diff(picin,i,j)
    print(1)

    for i in range(picin.shape[0]-1):   #修正最后一列
        loss[i][picin.shape[1]-1]=loss[i][picin.shape[1]-2]
    print(2)


    summ=np.zeros(picin.shape[:2])
    last=np.ones(picin.shape[:2],dtype='int32') #debug,其实可以不初始化
    stack=np.zeros(picin.shape[0],dtype='int32')

#第一遍全初始化summ
    for j in range(picin.shape[1]):    #范围:全
        summ[0][j]=loss[0][j]
    for i in range(picin.shape[0]-1):               #范围:i+1顶到头 最后一行是有summ和last的 第一行没有
        for j in range(picin.shape[1]):    #范围:全
            summ[i+1][j]=summ[i][max(j-1,0)]
            last[i+1][j]=max(j-1,0)
            for r in range(j,min(j+2,picin.shape[1]-1)):
                if summ[i][r]<summ[i+1][j]:       #取三个的最小值
                    summ[i+1][j]=summ[i][r]
                    last[i+1][j]=r                #存放上面一排的位置
            summ[i+1][j]+=loss[i+1][j]


    print('ready')
#    for step in range(picin.shape[0]-10):
    for step in range(10):
        regen=np.zeros(picin.shape[:2],dtype='int32') #debug,其实可以一维...?

#找最小值
        minsum=10000000000
        for j in range(1,picin.shape[1]-1-step):        #因为第一列和最后一列没有,范围缩小,缩小掉黑边
            if summ[picin.shape[0]-1][j]<minsum:
                minsum=summ[picin.shape[0]-1][j]
                oldm=j


#显示图片
        minpos=oldm

        for i in range(picin.shape[0]-1,-1,-1):         #范围:全
            for r in range(3):
                picin[i][minpos][r]=0                   #画一条黑线

            loss[i][minpos]=10000                       #loss提上去(下面尝试让他没有用)
            stack[i]=minpos                             #记录路径: 也就是说stack和i等大,并且相当于全沿黑线.按正顺序.
            minpos=last[i][minpos]


        cv2.imshow('1',picin)
        cv2.waitKey(1)
        cv2.imwrite('1'+str(step)+'.jpg',picin)

#更新summ
        def nsumm(summ,loss,i,down,up,left,right,regen):
            oldsum = summ[i+1][down]                        #记录summ
            down=max(stack[i]+down,0)
            up=min(stack[i]+up,summ.shape[1])
            if summ[i+1][down] > summ[i][up]:               #直接最小
                summ[i+1][down] = summ[i][up]               #变得更小了.标注.
                regen[i+1][down]=-1                         


            elif summ[i+1][down] == summ[i][stack[i]]:      #三选一,一般会变得更大,也可能不变
                left=max(stack[i]+left,0)                   
                right=min(stack[i]+right,summ.shape[1])

                summ[i+1][down] = summ[i][left]
                last[i+1][down] = left
                for j in range(left+1,right+1):
                    if summ[i+1][down] > summ[i][j]:
                        summ[i+1][down] = summ[i][j]
                        last[i+1][down] = j
                summ[i+1][down] += loss[i+1][down]
            if not summ[i+1][down] == oldsum:
                regen[i+1][down]=1
            else:
                regen[i+1][down]=0



        for i in range(picin.shape[0]-1):               #范围:正向,最后一个数没有
            if stack[i+1]==stack[i]:
                nsumm(summ,loss,i,-1,1,-2,1,regen)
                nsumm(summ,loss,i,1,-1,-1,2,regen)
            elif stack[i+1]==stack[i]+1:
                nsumm(summ,loss,i,-1,1,-2,1,regen)
                nsumm(summ,loss,i,0,2,-1,2,regen)
            else:
                nsumm(summ,loss,i,0,-2,-2,1,regen)
                nsumm(summ,loss,i,1,-1,-1,2,regen)

            #更新下面的:变得更大更小了 的情况 针对i+2
            if i!=picin.shape[0]-2:
                for j in range(picin.shape[1]):
                    if regen[i+1][j]==1:       #变大了.
                        for r in range(max(0,j-1),min(picin.shape[1],j+2)):
                            if stack[i+2]!=r and summ[i+2][r]-loss[i+2][r]==summ[i+1][j]:     #等于它 必须更新
                                olds=summ[i+2][r]
                                minv=min(summ[i+1][max(0,r-1) : min(picin.shape[1],r+2)])
                                summ[i+2][r]=loss[i+2][r]+minv
                                last[i+2][r]=np.argmax(summ[i+1])
                                if(olds!=summ[i+2][r]):         #传递
                                    regen[i+2][r]=1
                    elif regen[i+1][j]==-1:      #变小了
                        for r in range(max(0,j-1),min(picin.shape[1],j+2)):
                            if stack[i+2]!=r and summ[i+2][r]-loss[i+2][r] > summ[i+1][j]:     #小于它才更新
                                summ[i+2][r]=loss[i+2][r]+summ[i+1][j]
                                last[i+2][r]=j
                                regen[i+2][r]=-1





        


        print(step)


        
        

#cv2.imshow('pic',picin)
#    cv2.imshow('pic',picin)
#    cv2.waitKey()

main()
