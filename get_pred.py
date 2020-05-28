import numpy as np
from fastai.text import *

learn = load_learner(" ------ ADD PATH TO FOLDER CONTAINING TextClassifier_EXP.pkl -----, Ex: SoftwareEngProject/models","TextClassifier_EXP.pkl")

review = 'ADD REVIEW HERE'

preds = learn.predict(review)

pred = preds[1].cpu().data.numpy()
probs = preds[2].cpu().data.numpy()
prob = probs[pred]

#preds - predicted outcome 0 or 1

#prob - probability of that outcome


