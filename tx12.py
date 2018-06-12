import cv2
import numpy as np

picin = cv2.imread('1.jpg')
print(picin.shape)
print(picin[100][100])
print(picin[100][101])
print(picin[100][102])
loss=np.zeros(picin.shape[:2])
summ=np.ones(picin.shape[:2])*10000
last=np.zeros(picin.shape[:2],dtype='int32')

for step in range(picin.shape[0]):
    for i in range(picin.shape[0]):
        for j in range(picin.shape[1]-1-step):
            for r in range(3):
                diff=(picin[i][j+1][r]-picin[i][j][r])/3/255
                loss[i][j]+=abs(diff)

    for i in range(picin.shape[0]-1):
        for j in range(1,picin.shape[1]-1-step):
            for r in range(-1,2):
                if loss[i][j+r]<summ[i+1][j]:
                    summ[i+1][j]=loss[i][j+r]
                    last[i+1][j]=r
            summ[i+1][j]+=loss[i+1][j]
    minsum=1
    for j in range(1,picin.shape[1]-1-step):
        if summ[picin.shape[0]-1][j]<minsum:
            minsum=summ[picin.shape[0]-1][j]
            minpos=j

    for i in range(picin.shape[0]-1,-1,-1):
        for j in range(minpos,picin.shape[1]-1-step):
            for r in range(3):
                picin[i][j][r]=picin[i][j+1][r]
            
        for r in range(3):
            picin[i][picin.shape[1]-1-step][r]=0

        minpos+=last[i][minpos]
    cv2.imwrite('1'+str(step)+'.jpg',picin)
    print(step)


    
    

#cv2.imshow('pic',picin)
cv2.imshow('pic',picin)
cv2.waitKey()
