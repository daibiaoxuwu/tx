import cv2
import numpy as np

picin = cv2.imread('2.png')
print(picin.shape)
print(picin[100][100])
print(picin[100][101])
print(picin[100][102])
loss=np.zeros(picin.shape)
summ=np.zeros(picin.shape[:2])
last=np.zeros(picin.shape[:2])

for i in range(picin.shape[0]-1):
    for j in range(picin.shape[1]):
        for r in range(3):
            diff=(picin[i+1][j][r]-picin[i][j][r])/3/255
            loss[i][j][0]+=abs(diff)
            loss[i][j][1]+=abs(diff)
            loss[i][j][2]+=abs(diff)

for i in range(picin.shape[0]-1):
    for j in range(picin.shape[1]):
        for r in range(3):
            if 


#cv2.imshow('pic',picin)
cv2.imshow('pic',loss)
cv2.waitKey()
