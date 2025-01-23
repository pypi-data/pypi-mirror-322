#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# MIT License

# Copyright (c) 2025 Anthony Pecquenard

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import numpy as np
import matplotlib.cm as cm

def Greyscale(N):
    return np.linspace(np.array([0, 0, 0]), np.array([255, 255, 255]), N).astype(int)

def Jet(N):
    return (cm.jet(np.linspace(0, 1, N))[:, :3] * 255).astype(int)

def Hot(N):
    return (cm.hot(np.linspace(0, 1, N))[:, :3] * 255).astype(int)

def Plasma(N):
    return (cm.plasma(np.linspace(0, 1, N))[:, :3] * 255).astype(int)

def Viridis(N):
    return (cm.viridis(np.linspace(0, 1, N))[:, :3] * 255).astype(int)

def Inferno(N):
    return (cm.inferno(np.linspace(0, 1, N))[:, :3] * 255).astype(int)

cs = {
    'Greyscale': Greyscale,
    'Jet': Jet,
    'Hot': Hot,
    'Plasma': Plasma,
    'Viridis': Viridis,
    'Inferno': Inferno}