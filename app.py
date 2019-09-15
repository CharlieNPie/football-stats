from flask import Flask, render_template
import xg_test

app = Flask(__name__)

#data to be displayed on pages
form_data = xg_test.get_xpts()
score_data = xg_test.get_xgoals()

#index route
@app.route('/')
def index():
    return render_template('index.html', pts_outliers=form_data, goals_outliers=score_data)

@app.route('/players')
def players():
    return render_template('players.html')

if __name__ == "__main__":
    app.run(debug=True)