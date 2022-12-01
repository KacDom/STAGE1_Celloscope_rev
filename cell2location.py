import sys
IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    !pip install --quiet scvi-colab
    from scvi_colab import install
    install()
    !pip install --quiet git+https://github.com/BayraktarLab/cell2location#egg=cell2location[tutorials]
import scanpy as sc
import anndata
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import cell2location
import scvi
from matplotlib import rcParams
import zipfile
import shutil

os.chdir("/content")
zip_file = 'dense.zip'
with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    zip_ref.extractall()
main_dir = "/content/" + zip_file.split(".")[0]
os.chdir("/content/" + zip_file.split(".")[0])
dirs_list = sorted([f for f in os.listdir() if '.' not in f])

for setup in dirs_list:
  print(setup, "\n")
  os.chdir(main_dir + '/' + setup)
  inf_aver = pd.read_csv("TRUE_lambda.csv", index_col=0)
  C_gs = sc.AnnData(pd.read_csv("C_gs.csv", index_col=0).transpose())
   
  cell2location.models.Cell2location.setup_anndata(adata=C_gs)
  mod = cell2location.models.Cell2location(C_gs, cell_state_df=inf_aver) 

  mod.train(max_epochs=30000, 
          # train using full data (batch_size=None)
          batch_size=None, 
          # use all data points in training because 
          # we need to estimate cell abundance at all locations
          train_size=1,
          use_gpu=False)
  # In this section, we export the estimated cell abundance (summary of the posterior distribution).
  adata_vis = mod.export_posterior(
      C_gs, sample_kwargs={'num_samples': 1000, 'batch_size': mod.adata.n_obs, 'use_gpu': False})
  adata_vis.obsm['means_cell_abundance_w_sf'].div(adata_vis.obsm['means_cell_abundance_w_sf'].sum(axis=1), axis=0).to_csv(setup+".csv")

os.chdir("/content")
shutil.make_archive(zip_file.split('.')[0], 'zip', zip_file.split('.')[0])