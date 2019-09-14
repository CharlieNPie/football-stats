from flask import Flask, render_template
import xg_test

app = Flask(__name__)

#data to be displayed on index
data = xg_test.get_xpts()

#index route
@app.route('/')
def index():
    return render_template('index.html', overachievers = data[0], underachievers = data[1])

if __name__ == "__main__":
    app.run(debug=True)