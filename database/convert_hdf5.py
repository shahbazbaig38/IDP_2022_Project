# read tiff file
from spectral_tiffs import read_stiff, read_mtiff
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import h5py

'''
    Convert original spim file into spim, wavelengths, rgb, metadata in hdf5
'''


# read tiff and mask tiff file 
tiff_path = "/Users/yusukemikami/Repos/IDP_2022_Project/data/Set 1, lower 10, icg.tiff"
spim, wavelengths, rgb, metadata = read_stiff(tiff_path)

mask_path = "/Users/yusukemikami/Repos/IDP_2022_Project/data/Set 1, lower 10, icg, mask.tiff"
masks = read_mtiff(mask_path)

# create dataset
hf = h5py.File('hdf5_files/Set_1_lower_10_icg.h5', 'w')

hf.create_dataset('spim', data=spim)
hf.create_dataset('rgb', data=rgb)
hf.create_dataset('mask', data=np.array(list(masks.values())).astype(int))


tiff_path = "/Users/yusukemikami/Repos/IDP_2022_Project/data/Set 1, lower 2, icg.tiff"
spim, wavelengths, rgb, metadata = read_stiff(tiff_path)

mask_path = "/Users/yusukemikami/Repos/IDP_2022_Project/data/Set 1, lower 2, icg, mask.tiff"
masks = read_mtiff(mask_path)

hf = h5py.File('hdf5_files/Set_1_lower_2_icg.h5', 'w')

hf.create_dataset('spim', data=spim)
hf.create_dataset('rgb', data=rgb)
hf.create_dataset('mask', data=np.array(list(masks.values())).astype(int))


# test hdf5
infh = h5py.File('hdf5_files/Set_1_lower_2_icg.h5', 'r')

Set_1_lower_2_icg = infh['spim']

print(Set_1_lower_2_icg.shape)

Set_1_lower_2_icg = infh['rgb']

print(Set_1_lower_2_icg.shape)

Set_1_lower_2_icg = infh['mask']

print(Set_1_lower_2_icg.shape)