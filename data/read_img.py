import cv2
import sys
import os

img_path = '/Users/agentmervin/Downloads/GF1_0522/222.tiff'
img = cv2.imread(img_path,1)
print('不进行转化读取')
cv2.namedWindow("Image")
cv2.imshow("Image", img)
cv2.waitKey (0)
cv2.imwrite('/Users/agentmervin/Downloads/GF1_0522/222.png', img)
#print(img.dtype)
#print(img.shape)
