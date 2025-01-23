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

## --------------------------------------------------------------------------------- ##
# Manage the data from a STEM_EDX acquisition, apply PCA and NMF decomposition.
## --------------------------------------------------------------------------------- ##

import numpy as np
import hyperspy.api as hs


class Decomposition:
    def __init__(self, data, method='svd', n_components=3, normalize_poissonian_noise=True):
        """Initializes the Decomposition class

        Parameters
        ----------
        data : numpy array
            The data to be decomposed
        method : str, optional
            Decomposition method, by default 'svd'
        n_components : int, optional
            Number of components, by default 3
        """

        if method == 'svd':
            self.name = 'PCA'
        elif method == 'nmf':
            self.name = 'NMF'

        self.key = f'{self.name}_{method}_{n_components}_{normalize_poissonian_noise}'
        self.data = data
        self.data.change_dtype('float')
        self.method = method
        self.n_components = n_components
        self.selected_component = 0

        if method == 'svd':
            try:
                self.n_components = 'Undefined'
                # Hyperspy decomposition
                self.data.decomposition(normalize_poissonian_noise=normalize_poissonian_noise, print_info=False)
                self.success = True
            except Exception:
                self.success = False

        elif method == 'nmf':
            try:
                # Hyperspy decomposition
                self.data.decomposition(
                    algorithm='NMF',
                    output_dimension=n_components,
                    normalize_poissonian_noise=normalize_poissonian_noise,
                    max_iter=5000,
                    print_info=False
                )
                self.success = True
            except Exception:
                self.success = False

        if self.success:
            self.factors = self.data.get_decomposition_factors()
            self.loadings = self.data.get_decomposition_loadings()
            if method == 'svd':
                self.elbow_method = self.data.estimate_elbow_position()

    def next_component(self):
        self.selected_component += 1


class STEM_EDX_DATA:
    def __init__(self, path, data=None, name='STEM_EDX_Object', signal_type='EDS_TEM', rebin_energy=1):
        """Initializes the STEM_EDX_DATA class

        Parameters
        ----------
        path : str
            The path to the data file if data is not provided.
        data : hyperspy object, optional
            Already loaded data from Hyperspy, by default None
        signal_type : str, optional
            Signal type for loadings parameters, by default 'EDS_TEM'
        rebin_energy : int, optional
            Rebin energy factor, by default 1
        """

        # Load the data
        if data is not None:
            self.data = data
        else:
            self.data = hs.load(path, signal_type=signal_type, rebin_energy=rebin_energy)

        self.data_copy = self.data.deepcopy()
        self.metadata = self.data.metadata
        self.file = path
        self.name = name
        self.signal_type = signal_type

        # Get axes informations from the datas.
        try:
            self.Scales = (
                self.data.axes_manager[0].scale,
                self.data.axes_manager[1].scale,
                self.data.axes_manager[2].scale
            )
            self.Energy_offset = self.data.axes_manager[2].offset
        except Exception:
            self.Scales = (1, 1, 1)
            self.Energy_offset = 0

        self.data = np.array(self.data)
        self.size = self.data.shape
        self.key = f"{self.name}_{self.signal_type}_{self.size}"
        self.sub_items = {}

    def rebin(self, factor=(2, 2, 1)):
        """Rebin the data

        Parameters
        ----------
        factor : tuple, optional
            Rebin (x, y, Energy) axes, by default (2, 2, 1)
        """

        self.data = self.data.rebin(factor)

    def apply_PCA(self):
        """
        Apply Principal Component Analysis (PCA) to the data.
        This method applies PCA using Singular Value Decomposition (SVD) with a 
        specified number of components and an option to normalise Poissonian 
        noise. If the decomposition has already been applied, it will not be 
        re-applied.

        Returns
        -------
        str
            'Success' if PCA was successfully applied, 'Failed' otherwise.
        """

        name = 'PCA'
        method = 'svd'
        n_components = 3
        normalize_poissonian_noise = True

        PCA_key = f'{name}_{method}_{n_components}_{normalize_poissonian_noise}'

        # Check if the decomposition has already been applied
        for item in self.sub_items:
            if item == PCA_key:
                return

        self.PCA = Decomposition(self.data_copy)

        if self.PCA.success:
            self.sub_items[PCA_key] = self.PCA
            return 'Success'
        else:
            return 'Failed'

    def apply_NMF(self):
        """
        Apply Non-negative Matrix Factorisation (NMF) to the data.
        This method applies NMF to the data stored in the instance. It checks if 
        the NMF has already been applied with the same parameters and skips the 
        computation if so. If the NMF is successful, it stores the result in 
        `self.sub_items`.

        Returns
        -------
        str
            'Success' if NMF is applied successfully, 'Failed' otherwise.
        """

        name = 'NMF'
        method = 'nmf'
        n_components = 3
        normalize_poissonian_noise = True

        NMF_key = f'{name}_{method}_{n_components}_{normalize_poissonian_noise}'

        # Check if the decomposition has already been applied
        for item in self.sub_items:
            if item == NMF_key:
                return

        self.NMF = Decomposition(self.data_copy, method='nmf')

        if self.NMF.success:
            self.sub_items[NMF_key] = self.NMF
            return 'Success'
        else:
            return 'Failed'