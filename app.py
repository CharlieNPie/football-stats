from flask import Flask, render_template
import stats_backend

app = Flask(__name__)

#data to be displayed on pages
form_data = stats_backend.get_xpts()
score_data = stats_backend.get_xgoals()
goals_against_data = stats_backend.get_xgoals_against()

#basic list of team names for drop-down
team_names = stats_backend.get_team_data()[0]
print(team_names)

#index route
@app.route('/')
def index():
    return render_template(
        'index.html', 
        pts_outliers=form_data, 
        goals_outliers=score_data, 
        conceded_outliers=goals_against_data
        )

@app.route('/players')
def players():
    return render_template('players.html')

@app.route('/teams')
def teams():
    return render_template('teams.html')

@app.route('/tactics')
def tactics():
    return render_template('players.html')

if __name__ == "__main__":
    app.run(debug=True)