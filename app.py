import datetime
import pickle
import joblib
import pandas as pd

from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

# Load the model from the joblib file
model = joblib.load("./models/dt_model.pkl")

def preprocess_input(data):
    """
    Preprocesses the input JSON data before feeding it into the model.
    """
    # Convert Date key to a datetime object
    date_string = data['Date']
    date_obj = datetime.strptime(date_string, '%Y-%m-%d')

    # Create Year, Month, Day fields from the datetime object
    data['Year'] = date_obj.year
    data['Month'] = date_obj.month
    data['Day'] = date_obj.day

    # Convert State_Holiday string to int counterpart 
    state_holiday_map = {'0': 0, 'a': 1, 'b': 2, 'c': 3}
    data['StateHoliday'] = state_holiday_map.get(data['StateHoliday'], data['StateHoliday'])
    
    # Delete "Date" key
    del data["Date"]
    return data

@app.route('/health', methods=['GET'])
def health():
    return ("Welcome to Rossmann Sales API!")

@app.route("/predict", methods=["POST"])
def predict():
    # Get the input data as a JSON
    input_data = request.get_json()

    # Preprocess the input data
    input_preprocessed = preprocess_input(input_data)

    # Convert dictionary to dataframe
    input_dataframe = pd.DataFrame([input_preprocessed])

    # Make the prediction using the loaded model
    prediction = model.predict(input_dataframe)
    response = prediction.tolist()
    return jsonify({"sales": response[0]})

if __name__ == '__main__':
    app.run(port=5000, debug=True)