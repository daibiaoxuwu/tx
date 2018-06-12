import cv2
import numpy as np

picin = cv2.imread('2.png')
print(picin.shape)
print(picin[100][100])
print(picin[100][101])
print(picin[100][102])
loss=np.zeros(picin.shape[:2])
summ=np.ones(picin.shape[:2])*10000
last=np.zeros(picin.shape[:2],dtype='int32')

for i in range(picin.shape[0]-1):
    for j in range(1,picin.shape[1]):
        for r in range(3):
            diff=(picin[i+1][j][r]-picin[i][j][r])/3/255
            loss[i][j]+=abs(diff)

for i in range(picin.shape[0]-1):
    for j in range(1,picin.shape[1]-1):
        for r in range(-1,2):
            if loss[i][j+r]<summ[i+1][j]:
                summ[i+1][j]=loss[i][j+r]
                last[i+1][j]=r
        summ[i+1][j]+=loss[i+1][j]
minsum=1
for j in range(1,picin.shape[1]-1):
    if summ[picin.shape[0]-1][j]<minsum:
        minsum=summ[picin.shape[0]-1][j]
        minpos=j

minpos=300
for i in range(picin.shape[0]-1,-1,-1):
    for r in range(3):
        print(i,minpos,r)
        picin[i][minpos][r]=255
    minpos+=last[i][minpos]


    
    

#cv2.imshow('pic',picin)
cv2.imshow('pic',picin)
cv2.waitKey()
