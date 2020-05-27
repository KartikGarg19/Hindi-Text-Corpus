from flask import Flask, render_template, request, redirect, url_for
from forms import MovieInputForm
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


@app.route('/prediction2', methods=['GET','POST'])
def prediction2():
    form = MovieInputForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('prediction2.html', title='Predict', form=form)
        else:
            movie_name = form.moviename.data
            predicted_rating = 2.5
            return render_template('result.html', movie_name=movie_name, rating=predicted_rating)
    elif request.method == 'GET':
        return render_template('prediction2.html', title='Predict', form=form)

@app.route("/review")
def review():
    return render_template('review.html')

app.run(debug=True)