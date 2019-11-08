
"""
Demonstrates the usage of mpi I/O methods and mpi calculation example: Estimate PI.

Run this with 4 processes like:
$ mpiexec -n 4 python demo_3.py
"""

import cv2
import time
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# image path. Edit it as your will
img_path = '/Users/agentmervin/Downloads/data/222.tiff'
filename = 'save_np_1.txt'
buffer=[]
###read the image
def load_image(img_path):
    img = cv2.imread(img_path,1)
    #print(img.size)
    #print(img.shape)
    img_shape = img.shape
    return img,img_shape



img, img_shape= load_image(img_path)
x_sum, y_sum = img_shape[0], img_shape[1]
#determine the iteration num.
sum=min(x_sum, y_sum)
#print(sum)



def calculate_part(sum, img):
    # Number of darts that land inside.
    buffer=[]
    #calculation task
    inside = 0
    start_num = rank*(sum//size)
    end_num = (rank+1)*(sum//size)
    # Iterate for the number of darts.\

    for i in range(start_num,end_num):
        for j in range(1,sum):
            x1,y1,z1 = img[i][j]
            if (x1**2+y1**2+z1**2) < 2.0:
                #print(i)
                buffer.append(i)
                inside += 1

    return inside, buffer




N=sum*sum
t0=time.time()
value, buffer = calculate_part(sum, img)
result = 0.0
count = 0



fh = MPI.File.Open(comm, filename, amode= MPI.MODE_CREATE | MPI.MODE_WRONLY)
# set individual file pointer of each process
# here we use the default file view, so offset is in bytes
buf1=np.asarray(buffer,dtype='i')
offset = len(buf1) * MPI.INT.Get_size()

if rank == 0:
    count += value
    #calculate final target.
    for i in range(1,size):
        value = comm.recv(source=i, tag=0)
        count += value
    result = 4 * (count / N)
    t1=time.time()
    print('target is : ',result)
    print('time cost is', t1 - t0, 's')

else:
    comm.send(value, dest=0, tag=0)


fh.Seek(rank*offset, whence=MPI.SEEK_SET)
fh.Write(buf1)

# close the file
fh.Close()
