from flask import Flask, request, jsonify, render_template, Response
import pickle
import numpy as np
import pandas as pd
import io
import json


app=Flask(__name__)

#model=open("creditdata.pkl","rb")
model_f = None
with open('creditdata.pkl', 'rb') as f:
    model_f = pickle.load(f)

#print(model_f)
@app.errorhandler(404)
def not_found_error(error):
    return "This page was not found.", 404

# Example of a custom error handler for 500 - Internal Server Error
@app.errorhandler(500)
def internal_error(error):
    return "An internal error occurred. Please try again later.", 500

@app.route('/')
def index():
    return render_template('index.html')

print("Hello")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        print("hello")
        #data = request.data  # Assuming the raw bytes are sent directly

        # Use BytesIO to simulate a file-like object from bytes
        model_file = io.BytesIO(model_f)

        # Load the model from the byte stream
        model = pickle.load(model_file)
        #get input data from form
        data=request.form
        # extract data from form and convert it into a dataframe
        print(data)
        
        age=float(data['age'])
        prev_defaults=int(data['prev_defaults'])
        #occupation_type=int(data['occupation_type'])
        #yearly_income=data['net_yearly_income']
        
        job_roles=['net_yearly_income','total_family_members', 'credit_limit',
       'credit_limit_used(%)', 'credit_score', 
       'default_in_last_6months', 'occupation_type_Accountants',
       'occupation_type_Cleaning staff', 'occupation_type_Cooking staff',
       'occupation_type_Core staff', 'occupation_type_Drivers',
       'occupation_type_HR staff', 'occupation_type_High skill tech staff',
       'occupation_type_IT staff', 'occupation_type_Laborers',
       'occupation_type_Low-skill Laborers', 'occupation_type_Managers',
       'occupation_type_Medicine staff',
       'occupation_type_Private service staff',
       'occupation_type_Realty agents', 'occupation_type_Sales staff',
       'occupation_type_Secretaries', 'occupation_type_Security staff',
       'occupation_type_Unknown', 'occupation_type_Waiters/barmen staff']

       
       
        job_selected = data['occupation_type']
        if job_selected not in job_roles:
            return jsonify({'error': 'Invalid job role'})
        job_data = [True if job == job_selected else False for job in job_roles]
        
        # Combine all inputs into a single array
        input_data = [age,prev_defaults] + job_data
        # Convert to numpy array
        input_array = np.array([input_data]).reshape(1, -1)
       
        # Predict salary
        prediction = model.predict(input_array)[0]
   
        prediction=int(prediction)
        print(prediction)
        if prediction==0:
            return jsonify({'predicted_CreditDefaulter': 'No'})
        else:
            return jsonify({'predicted_CreditDefaulter': 'Yes'})
        

        print("hello")
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)