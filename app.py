import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
# import Food_Recommendation_System_Baseline.ipynb
from food_recommendation_system_baseline import foodrecommendation


app = Flask(__name__)
model = pickle.load(open('modelpickel1.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    # int_features = [x for x in request.for m.values()]
    # print(int_features)
    final_features = request.form['meal']
    print("the input is" + str(final_features))
    prediction = model.give_rec(final_features)
    p = prediction.tolist()
    print(p)
    print("end")

    # output = prediction

    # return render_template('index.html', prediction_text='Employee Salary should be $ {}'.format(output)) .prediction[:5]
    return render_template('index.html', prediction_text='Recommended meals are: ' + "\n".join(p[:5])+ "\n") #+ str(p[:5])

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.give_rec(data)

    output = prediction
    return jsonify(output)
    # return ("Success")

if __name__ == "__main__":
    app.run(debug=True)