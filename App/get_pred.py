import numpy as np
from fastai.text import *

learn = load_learner("","TextClassifier_EXP.pkl")

def PredictionModel(review):
    # review = 'ADD REVIEW HERE'

    preds = learn.predict(review)

    pred = preds[1].cpu().data.numpy()
    probs = preds[2].cpu().data.numpy()
    prob = probs[pred]
    output = []
    output.append(pred)
    output.append(prob)
    return output

    #preds - predicted outcome 0 or 1

    #prob - probability of that outcome


