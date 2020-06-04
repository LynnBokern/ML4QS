# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 13:21:20 2020

@author: lynnb
"""


import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt


import math
import copy
from scipy.stats import norm
from sklearn.decomposition import PCA
import re


from util.VisualizeDataset import VisualizeDataset


DATA_PATH = Path('./intermediate_datafiles/')


dataset = pd.read_csv(Path(DATA_PATH / 'chapter4_result.csv'), index_col=0)

frequencies = []
values = []
for col in dataset.columns:
    val = re.findall(r'freq_\d+\.\d+_Hz', col)
    if len(val) > 0:
        frequency = float((val[0])[5:len(val)-4])
        frequencies.append(frequency)
        values.append(dataset.loc[dataset.index, col])
        
unique_frequencies = list(set(frequencies))

data_unique_frequencies = pd.Series([pd.DataFrame(index=dataset.index) for _ in range(len(unique_frequencies))], index=unique_frequencies) #mogeljk nog meer verschillende maken
        


for col in dataset.columns:
    val = re.findall(r'freq_\d+\.\d+_Hz', col)
    if len(val) > 0:
        frequency = float((val[0])[5:len(val)-4])
        data_unique_frequencies[frequency][col] = dataset[col]
        
     
for df_name in data_unique_frequencies.index:
    df = data_unique_frequencies[df_name]
    #VisualizeDataset2 = VisualizeDataset()

    #VisualizeDataset2.plot_dataset(df, df.columns)

    for col in df:
        print(col)
        plt.plot(df.index, df[col])
    plt.show()
    


