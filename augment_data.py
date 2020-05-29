import pandas as pd
import numpy as np
from tqdm import tqdm
from inltk.inltk import get_similar_sentences
import warnings
warnings.filterwarnings('ignore')

data = pd.read_csv('Final_dataset_3.0.csv')
data_augmented = pd.DataFrame(columns=data.columns)

for i in tqdm(range(data.shape[0]),position=0,leave=True):
    a = get_similar_sentences(data['Review'][i], 1, 'hi')
    inst_0 = data.iloc[i].copy()
    inst_0['Review'] = a[0]
    data_augmented = data_augmented.append(inst_0)

data_augmented.to_csv('Augmented_3.0.csv',index=False)
df_complete = pd.concat([data, data_augmented], axis=0)
df_complete = df_complete.sample(frac=1).reset_index(drop=True)
data_complete.to_csv('Dataset_3.0_Augmented.csv',index=False)
