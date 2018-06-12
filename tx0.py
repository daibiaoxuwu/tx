import cv2
import numpy as np

picin = cv2.imread('1.jpg')
print(picin.shape)
print(picin[100][100])
print(picin[100][101])
print(picin[100][102])
loss=np.zeros(picin.shape,dtype='ubyte')
summ=np.zeros(picin.shape[:2],dtype='int32')
last=np.zeros(picin.shape[:2],dtype='int32')

for i in range(picin.shape[0]-1):
    for j in range(picin.shape[1]-1):
        diff=0
        '''
        for r in range(3):
            diff+=abs(picin[i+1][j][r]-picin[i][j][r])/6/255
            '''
#        for r in range(3):
#            diff+=int(abs(int(picin[i][j+1][r])-int(picin[i][j][r])))
#        for r in range(3):
#            diff+=int(abs(int(picin[i+1][j][r])-int(picin[i][j][r])))
        #diff=abs(picin[i+1][j][0]+picin[i+1][j][1]+picin[i+1][j][2]-picin[i][j][0]-picin[i][j][1]-picin[i][j][2])/3/255
        #diff=abs(picin[i+1][j][0]+picin[i+1][j][1]+picin[i+1][j][2]-picin[i][j][0]-picin[i][j][1]-picin[i][j][2])/3/255
        diff=abs(int(picin[i][j+1][0])+int(picin[i][j+1][1])+int(picin[i][j+1][2])-int(picin[i][j][0])-int(picin[i][j][1])-int(picin[i][j][2]))
        #diff=abs(int(picin[i+1][j][0])+int(picin[i+1][j][1])+int(picin[i+1][j][2])-int(picin[i][j][0])-int(picin[i][j][1])-int(picin[i][j][2]))
        loss[i][j][0]+=(diff)
        loss[i][j][1]+=(diff)
        loss[i][j][2]+=(diff)

'''
for i in range(picin.shape[0]-1):
    for j in range(picin.shape[1]):
        for r in range(3):
'''         


#cv2.imshow('pic',picin)
cv2.imshow('pic',loss)
cv2.waitKey()
