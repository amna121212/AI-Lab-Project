from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load saved model, preprocessor, and label encoder
model = joblib.load("model.pkl")
preprocessor = joblib.load("preprocessor.pkl")
le_target = joblib.load("le_target.pkl")

# Columns used in training
numeric_features = ['Age', 'Years at Company', 'Monthly Income', 'Number of Promotions',
                    'Distance from Home', 'Number of Dependents', 'Company Tenure']

categorical_features = ['Job Role', 'Work-Life Balance', 'Job Satisfaction',
                        'Performance Rating', 'Overtime', 'Education Level', 'Marital Status',
                        'Job Level', 'Company Size', 'Remote Work', 'Leadership Opportunities',
                        'Innovation Opportunities', 'Company Reputation', 'Employee Recognition']

model_columns = numeric_features + categorical_features

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        df = pd.DataFrame([data])

        # Ensure all columns exist
        for col in model_columns:
            if col not in df.columns:
                df[col] = ''  # add empty string for missing columns

        df = df[model_columns]  # reorder columns
        X_transformed = preprocessor.transform(df)
        prediction = model.predict(X_transformed)
        prediction_label = le_target.inverse_transform(prediction)[0]

        return jsonify({'prediction': prediction_label})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)


