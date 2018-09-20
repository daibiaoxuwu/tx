import cv2
import numpy as np

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
    for i in range(picin.shape[0]-1):
        for j in range(picin.shape[1]-1):#loss的最后一行最后一列为0
            loss[i][j]=diff(picin,i,j)

    for i in range(picin.shape[0]):   #修正最后一列
        loss[i][picin.shape[1]-1]=10000
        loss[i][0]=10000
    for i in range(picin.shape[1]):   #修正最后一列
        loss[picin.shape[0]-1][i]=10000
        loss[0][i]=10000

    picin=np.concatenate(picin,np.zeros([100,picin.shape[1],3])

    for step in range(picin.shape[0]-10):
        summ=np.ones(picin.shape[:2])*10000               #重新初始化sum
        last=np.ones(picin.shape[:2],dtype='int32')*1000000

        for j in range(picin.shape[1]-step):    #范围:全
            summ[0][j]=loss[0][j]
        for i in range(picin.shape[0]-1):               #范围:i+1顶到头 最后一行是有summ和last的 第一行没有
            for j in range(picin.shape[1]-step):    #范围:全
                for r in range(max(j-1,0),min(j+2,picin.shape[1]-1-step)):
                    if summ[i][r]<summ[i+1][j]:       #取三个的最小值
                        summ[i+1][j]=summ[i][r]
                        last[i+1][j]=r                #存放上面一排的位置
                summ[i+1][j]+=loss[i+1][j]
                

        '''
            maxs=max(summ[i+1][:picin.shape[1]-step])
            print('max',maxs,max(loss[i+1]),i)
            for j in range(picin.shape[1]-step):
                for r in range(3):
                    if summ[i+1][j]<10:
                        disp[i+1][j][r]=0
                    else:
                        disp[i+1][j][r]=1
                    disp[i+1][j][r]=summ[i+1][j]/maxs
        cv2.imwrite('1g.jpg',disp)
        cv2.waitKey()
                        '''

                    
                    
        minsum=10000000000
        for j in range(1,picin.shape[1]-1-step):        #因为第一列和最后一列没有,范围缩小,缩小掉黑边
            if summ[picin.shape[0]-1][j]<minsum:
                minsum=summ[picin.shape[0]-1][j]
                oldm=j

        minpos=oldm

#显示图片
        for i in range(picin.shape[0]-1,-1,-1):
            print('mp33',i,minpos)
            for r in range(3):
                picin[i][minpos][r]=0
            minpos=last[i][minpos]
        cv2.imshow('1',picin)
        cv2.waitKey(1)


        minpos=oldm
        for i in range(picin.shape[0]-1,-1,-1):             #从最底下一直到最上面
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
#    loss2=loss[:]#debug
        #更新loss
        for i in range(picin.shape[0]-2,-1,-1):             #i不能从头到尾了因为计算loss i最后一行没有
            for j in range(minpos-1,minpos):                #j其实是一个数
                loss[i][j]=diff(picin,i,j)
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

    printf("added my feature");
    printf("this is a bug");
    cv2.waitKey()

main()
