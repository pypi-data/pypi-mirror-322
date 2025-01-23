
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .main import *

df=pd.read_csv("mechanical_database.csv")
print(df.describe(include='all'))
print(df.columns)
data=dataset_clean(df)
percentage=data.percentage()
data.clean_dataset_percentage(percentage)
print('\nDataset limpio:')
print(data.df)
