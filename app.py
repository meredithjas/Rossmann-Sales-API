import datetime
import os
import pickle
import joblib
import pandas as pd

from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

# Load the model from the pickle file
model = joblib.load("./models/rf_model.pkl")


def preprocess_input(input_data):
    """
    Splits Date to Year, Month, Day.
    Converting State Holiday to int counterpart.
    Deletes Open and Date fields.
    """
    # Convert Date key to a datetime object
    date_string = input_data["Date"]
    date_obj = datetime.strptime(date_string, "%Y-%m-%d")

    # Create Year, Month, Day fields from the datetime object
    input_data["Year"] = date_obj.year
    input_data["Month"] = date_obj.month
    input_data["Day"] = date_obj.day

    # Convert State_Holiday string to int counterpart
    state_holiday_map = {"0": 0, "a": 1, "b": 2, "c": 3}
    input_data["StateHoliday"] = state_holiday_map.get(
        input_data["StateHoliday"], input_data["StateHoliday"]
    )

    # Delete "Date" key
    del input_data["Date"]

    # Delete "Open" key
    del input_data["Open"]

    return input_data


# Health Check endpoint
@app.route("/health", methods=["GET"])
def health():
    return "Welcome to Rossmann Sales API!!"


# Predict endpoint
@app.route("/predict", methods=["POST"])
def predict():
    # Get the input data as a JSON
    input_data = request.get_json()

    # Check if store is Open
    if input_data["Open"] != 1:
        return {
            "status": 400,
            "error": "ERROR: Store should be open.",
        }

    # Check if State Holiday is valid
    if not (input_data["StateHoliday"] in ["a", "b", "c", "0"]):
        if input_data["StateHoliday"] != 0:
            return {
                "status": 400,
                "error": "ERROR: State Holiday unknown.",
            }

    # Preprocess the input data
    input_preprocessed = preprocess_input(input_data)

    # Convert dictionary to dataframe
    input_dataframe = pd.DataFrame([input_preprocessed])

    # Make the prediction using the loaded model
    try:
        prediction = model.predict(input_dataframe)
        response = prediction.tolist()
        return jsonify({"sales": response[0]})

    except Exception as err:
        raise Exception("ERROR:", err)


if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)
    app.run(debug=False, host="0.0.0.0", port=port)
