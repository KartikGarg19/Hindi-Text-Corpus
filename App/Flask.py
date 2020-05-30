from flask import Flask, render_template, request, redirect, url_for
from forms import MovieInputForm, SearchForm
from movieSearch import AajTak
# import sys
# sys.path.append('..')
# import get_pred
# from get_pred import PredictionModel
app= Flask(__name__)

app.config['SECRET_KEY'] = '60cc08dd39658ff2bf4a9e3e45ec8b8f'


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/about")

def about():
    return render_template('About.html')

@app.route("/contact")

def contact():
    return render_template('meet the team.html')


@app.route("/analysis")
def analysis():
    return render_template('analysis.html')


@app.route('/prediction', methods=['GET','POST'])
def prediction2():
    form = MovieInputForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('prediction.html', title='Predict', form=form)
        else:
            movie_name = form.moviename.data
            # output = PredictionModel(form.moviereview)
            # pred = output[0]
            # prob = output[1]
            pred = 1
            prob = 0.92
            if(pred == 1):
                sentiment = "Positive"
            else:
                sentiment = "Negative"
            return render_template('result.html', movie_name=movie_name, sentiment=sentiment, prob=prob)
    elif request.method == 'GET':
        return render_template('prediction.html', title='Predict', form=form)

@app.route('/search', methods=['GET','POST'])
def search():
    form = SearchForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('search.html', title='search', form=form)
        else:
            movie_name = form.moviename.data
            info = AajTak(movie_name)
            return render_template('search2.html', title='search2', info=info, form=form)
    elif request.method == 'GET':
        return render_template('search.html', title='Predict', form=form)


app.run(debug=True)