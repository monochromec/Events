#!/usr/bin/env python3

import pickle
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

archs = ['s390', 'gcp', 'intel']

# Set up 3d bar chart with x # of connections and y as record length
# ARCH: architecture prefix as string
# Expects ARCH_dim.p and ARCH_dat.npy as pickled Pyton object files in current directory

def draw_chart(arch):
    dims = pickle.load(open(arch+'_dim.p', 'rb'))
    vals = pickle.load(open(arch+'_dat.npy', 'rb'))
    fig = plt.figure(figsize=(5, 5))
    ax = Axes3D(fig)
    # Set up grid
    lx = len(dims[0])
    ly = len(dims[1])
    xp = np.arange(lx)
    yp = np.arange(ly)
    xpos, ypos = np.meshgrid(xp+0.25, yp+0.25)
    xpos = xpos.flatten()
    ypos = ypos.flatten()
    zpos = np.zeros(lx*ly)
    dx = 0.5 * np.ones_like(lx*ly)
    dy = dx.copy()
    dz = vals.flatten()
    # Draw axis with labels
    cs = ['r', 'g', 'b', 'y'] * ly
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=cs)
    xnames = [str(i) for i in dims[0]]
    ynames = [str(i) for i in dims[1]]
    ticksx = np.arange(0.5, lx)
    ticksy = np.arange(0.5, ly)
    # Evenly space tick labels
    plt.xticks(ticksx, xnames)
    plt.yticks(ticksy, ynames)
    ax.set_xlabel('# of connections')
    ax.set_ylabel('record length in bytes')
    ax.set_zlabel('Operations/sec')
    return fig

for arch in archs:
    fig = draw_chart(arch)
    fig.savefig(arch+'.svg')
