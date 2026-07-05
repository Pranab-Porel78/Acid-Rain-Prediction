from flask import Flask

from flask import Flask, render_template


from routes.sensor import sensor_bp

from routes.pollution import pollution_bp

from routes.prediction import prediction_bp

app = Flask(__name__)

app.register_blueprint(sensor_bp, url_prefix="/api")
app.register_blueprint(
    pollution_bp,
    url_prefix="/api"
)
app.register_blueprint(
    prediction_bp,
    url_prefix="/api"
)


@app.route("/")
def dashboard():

    return render_template("dashboard.html")

@app.route("/sensor")
def sensor():
    return render_template("sensor.html")


@app.route("/pollution")
def pollution():
    return render_template("pollution.html")


@app.route("/prediction")
def prediction():
    return render_template("prediction.html")


@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":

    app.run(
    host="0.0.0.0",
    port=5000,
    debug=True
)