import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

df_train = pd.read_csv('data/train_3.0_Augmented.csv')

df_valid = pd.read_csv('data/val_3.0.csv')

for df in [df_train, df_valid]:
    if len(df) == len(df_train):
        print('In Training Set:')
    else:
        print('In Valid Set:')
    print('Positive Sentiment', (df['Sentiment'] == 1).sum())
    print('Negative Sentiment', (df['Sentiment'] == 0).sum())
    print('\n\n\n')

df_train_temp = pd.DataFrame()
for i in range(df_train.shape[0]):
    review = df_train.iloc[i].copy()
    if(review['Sentiment']==1):
      review['Sentiment']='positive'
    else:
      review['Sentiment']='negative'
    df_train_temp = df_train_temp.append(review)
df_train = df_train_temp.copy()

df_valid_temp = pd.DataFrame()
for i in range(df_valid.shape[0]):
    review = df_valid.iloc[i].copy()
    if(review['Sentiment']==1):
      review['Sentiment']='positive'
    else:
      review['Sentiment']='negative'
    df_valid_temp = df_valid_temp.append(review)
df_valid = df_valid_temp.copy()

"""# ULMFIT"""

from fastai.text import *

path = Path('data')

data_lm = TextLMDataBunch.from_df(path=path, train_df=df_train, valid_df=df_valid, text_cols='Review', label_cols='Sentiment')

data_clas = TextClasDataBunch.from_df(path=path, train_df=df_train, valid_df=df_valid, text_cols='Review', label_cols='Sentiment', vocab=data_lm.train_ds.vocab)

data_clas.show_batch(2)

data_lm.show_batch(2)

data_lm.save('data_lm.pkl')
#data_lm.vocab.itos[:3]

learn = language_model_learner(data_lm, AWD_LSTM, pretrained="third_hi_lm.pth", drop_mult=0.5)

learn.lr_find()
# learn.recorder.plot()

learn.freeze()

# fitting head
learn.fit_one_cycle(1, 1e-01,moms=(0.8, 0.7))

"""### Now fine-tuning after unfreezing the whole network"""

learn.unfreeze()
learn.lr_find()
# learn.recorder.plot()

# fitting after unfreezing the whole learn. Therefore, its the final fine-tuning
learn.fit_one_cycle(8, 1e-03, moms=(0.8, 0.7))

learn.export("models/LangaugeModel_EXP.pkl")

learn.save_encoder('LangaugeModel')

"""### Now moving on to the text-classifier"""

learn = text_classifier_learner(data_clas, AWD_LSTM, drop_mult=0.5)
# Loading the encoder 
learn.load_encoder('LangaugeModel')


learn.freeze()
learn.lr_find()
# learn.recorder.plot()

# fitting the head
learn.fit_one_cycle(1, 5e-02, moms=(0.8, 0.7))

"""### Now, we will fine-tune the whole classifier using 'gradual unfreezing' technique"""

learn.freeze_to(-2)
learn.fit_one_cycle(1, 1e-03, moms=(0.8, 0.7))

learn.freeze_to(-3)
learn.fit_one_cycle(1, 5e-03, moms=(0.8, 0.7))

learn.unfreeze()
learn.fit_one_cycle(8, 5e-04, moms=(0.8, 0.7))

learn.export("models/TextClassifier_EXP.pkl")


"""# Visualization"""

# learn = load_learner("models","TextClassifier_EXP.pkl")

from fastai.tabular import *
from fastai.vision import *

preds,y,losses = learn.get_preds(with_loss=True)

inp = ClassificationInterpretation(learn,preds,y,losses)

cm = inp.plot_confusion_matrix()

"""### To save the confusion matrix image"""

# from PIL import Image
# j = Image.fromarray(cm)
# j.save('confusion_matrix.jpeg')
