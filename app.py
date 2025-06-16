import pickle
from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    redirect,
    url_for,
    session,
    escape,
)
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

# Loading the trained regression model and scaler
regmodel = pickle.load(open("regmodel.pkl", "rb"))
scaler = pickle.load(open("scaling.pkl", "rb"))

# Mean total_bedrooms from training set (you should adjust this to match your data!)
MEAN_TOTAL_BEDROOMS = 537.87  # Example; you should put your actual mean here


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/predict_api", methods=["POST"])
def predict_api():
    data = request.json["data"]
    print("Received data :", data)

    values = list(data.values())  # this should match the trained features
    if len(values) == 7:
        # If total_bedrooms is missing, insert mean at the appropriate index
        values.insert(3, MEAN_TOTAL_BEDROOMS)

    new_data = scaler.transform([values])  # 2D array expected
    output = regmodel.predict(new_data)
    return jsonify({"prediction": output[0]})


MEAN_TOTAL_BEDROOMS = 1.09667  # for example; use your actual mean here


@app.route("/predict", methods=["POST"])
def predict():
    """For form submission from home.html"""
    data = [float(x) for x in request.form.values()]
    if len(data) == 7:
        # If total_bedrooms is missing, insert the mean at the 4th position
        data.insert(3, MEAN_TOTAL_BEDROOMS)

    final_input = scaler.transform([data])  # Now it's 8 features
    output = regmodel.predict(final_input)[0]

    return render_template(
        "home.html", prediction_text=f"The House Price Prediction is {output}"
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
