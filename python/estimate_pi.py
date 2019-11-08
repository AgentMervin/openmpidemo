import random as r
import math as m
import cv2
import sys
import os



img_path = '/Users/agentmervin/Downloads/data/222.tiff'


def load_image(img_path):
    img = cv2.imread(img_path,1)
    print(img.size)
    print(img.shape)
    img_shape = img.shape
    return img,img_shape

# Number of darts that land inside.
inside = 0
# Total number of darts to throw.
total = 100000

img, img_shape= load_image(img_path)
x_sum, y_sum = img_shape[0], img_shape[1]
sum=min(x_sum, y_sum)


for i in range(1,sum):
    for j in range(1,100):
        x1,y1,z1 = img[i][j]
        if (x1**2+y1**2+z1**2) < 2.0:
            print(i)
            inside += 1

target = (float(inside) / total) * 4
print(target)


