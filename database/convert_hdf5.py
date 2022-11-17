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
hf = h5py.File('hsi.h5', 'w')

hf.create_dataset('Set_1_lower_10_icg_spim', data=spim)
hf.create_dataset('Set_1_lower_10_icg_rgb', data=rgb)
hf.create_dataset('Set_1_lower_10_icg_masks', data=np.array(list(masks.values())).astype(int))


tiff_path = "/Users/yusukemikami/Repos/IDP_2022_Project/data/Set 1, lower 2, icg.tiff"
spim, wavelengths, rgb, metadata = read_stiff(tiff_path)

mask_path = "/Users/yusukemikami/Repos/IDP_2022_Project/data/Set 1, lower 2, icg, mask.tiff"
masks = read_mtiff(mask_path)


hf.create_dataset('Set_1_lower_2_icg_spim', data=spim)
hf.create_dataset('Set_1_lower_2_icg_rgb', data=rgb)
hf.create_dataset('Set_1_lower_2_icg_masks', data=np.array(list(masks.values())).astype(int))


# test hdf5
infh = h5py.File('hsi.h5', 'r')

Set_1_lower_2_icg_spim = infh['Set_1_lower_2_icg_spim']

print(Set_1_lower_2_icg_spim.shape)

Set_1_lower_2_icg_spim = infh['Set_1_lower_2_icg_rgb']

print(Set_1_lower_2_icg_spim.shape)

Set_1_lower_2_icg_spim = infh['Set_1_lower_2_icg_masks']

print(Set_1_lower_2_icg_spim.shape)