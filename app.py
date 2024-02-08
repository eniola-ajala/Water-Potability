import pickle
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        input_data = {
            'ph': float(request.form.get('ph', 0)),
            'Hardness': int(request.form.get('Hardness', 0)),
            'Solids': int(request.form.get('Solids', 0)),
            'Chloramines': int(request.form.get('Chloramines', 0)),
            'Sulfate': int(request.form.get('Sulfate', 0)),
            'Conductivity': int(request.form.get('Conductivity', 0)),
            'Organic_carbon': int(request.form.get('Organic_carbon', 0)),
            'Trihalomethanes': int(request.form.get('Trihalomethanes', 0)),
            'Turbidity': int(request.form.get('Turbidity', 0)),
        }

        input_df = pd.DataFrame([input_data])
        prediction = model.predict(input_df)[0]

        # Convert the binary prediction to a human-readable message
        if prediction == 1:
            prediction_text = 'The water is potable for drinking.'
        else:
            prediction_text = 'The water is not potable for drinking.'

        return render_template('index.html', prediction_text=prediction_text)

   

        
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
