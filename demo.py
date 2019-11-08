#!usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import mpi4py.MPI as MPI
import numpy as np

#
#  Global variables for MPI
#

# instance for invoking MPI relatedfunctions
comm = MPI.COMM_WORLD
# the node rank in the whole community
comm_rank = comm.Get_rank()
# the size of the whole community, i.e.,the total number of working nodes in the MPI cluster
comm_size = comm.Get_size()

if __name__ == '__main__':
    if comm_rank == 0:
        sys.stderr.write("processor root starts reading data...\n")
        all_lines = sys.stdin.readlines()
    all_lines = comm.bcast(all_lines if comm_rank == 0 else None, root=0)
    num_lines = len(all_lines)
    local_lines_offset = np.linspace(0, num_lines, comm_size + 1).astype('int')
    local_lines = all_lines[local_lines_offset[comm_rank]:local_lines_offset[comm_rank + 1]]
    sys.stderr.write("%d/%d processor gets %d/%d data \n" % (comm_rank, comm_size, len(local_lines), num_lines))
    cnt = 0
    for line in local_lines:
        fields = line.strip().split('\t')
        cnt += 1
        if cnt % 100 == 0:
            sys.stderr.write("processor %d has processed %d/%d lines \n" % (comm_rank, cnt, len(local_lines)))
        output = line.strip() + ' process every line here'
        print output
