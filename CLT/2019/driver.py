#!/bin/env python3
#
# memtier driver for Redis benchmark
#
# Iterate over connections, data sizes and pipeline length

import subprocess
import numpy as np
import pickle
import sys
from pathlib import PurePath

co = (25, 50, 100, 500)
da = (32, 256, 1024, 2048)
res = np.zeros((len(co), len(da)))
dim = (co, da)

if len(sys.argv) != 2:
    print('Usage: {} <architecture_name>'.format(PurePath(sys.argv[0]).name))
    sys.exit(-1)
else:
    arch = sys.argv[1]

cc = 0
for c in co:
    dc = 0
    for d in da:
        args ='memtier_benchmark -t 1 -c {} -d {} --test-time=60 --hide-histogram'.format(c, d)
        cp = subprocess.run(args + " | fgrep Totals | awk '{print $2}'", shell=True, encoding="UTF-8", stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        res [cc][dc] = round(float(cp.stdout.strip()))
        subprocess.run('redis-cli flushdb', encoding="UTF-8", shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        dc += 1
    cc += 1

pickle.dump(dim, open(arch+'_dim.p', 'wb'))
res.dump(arch+'_dat.npy')
