from flask import Flask, request, render_template, json
from flask_cors import CORS
import sklearn
import pickle
import pandas as pd

app = Flask(__name__)
CORS(app)
model = pickle.load(open("creditscore_xgboost.pkl", "rb"))

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/api', methods = ['GET'])
def returnresult():
	return {'Test':'HelloWorld'}


@app.route("/api/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        response = json.loads(request.data)
        print('Request:', response)

        creditamount= int(response['creditAmount'])
        duration=int(response['duration'])
        purpose = response['purpose']
        print('Purpose:',purpose)
        disposible=int(response['disposible'])
        num_existing_credit = int(response['numExistCredit'])
        status_existing_credit = int(response['statusExistCredit'])
        credit_history= int(response['creditHistory'])
        isOtherPlans=response['isOtherPlans']
        isEmployed = response['isEmployed']   
        employ_len=int(response['employLength'])
        housing = int(response['housing'])
        num_child=int(response['numChild'])

        if (purpose=='electronics'):
            electronics = 1
            car_new=0
            car_used=0
            furniture_equipment=0
            business=0
            education=0
            repairs=0
            domestic_appliances=0
            retraining=0
            others=0
        elif (purpose=='car_new'):
            electronics = 0
            car_new=1
            car_used=0
            furniture_equipment=0
            business=0
            education=0
            repairs=0
            domestic_appliances=0
            retraining=0
            others=0
        elif (purpose=='car_used'):
            electronics = 0
            car_new=0
            car_used=1
            furniture_equipment=0
            business=0
            education=0
            repairs=0
            domestic_appliances=0
            retraining=0
            others=0
        elif (purpose=='furniture_equipment'):
            electronics = 0
            car_new=0
            car_used=0
            furniture_equipment=1
            business=0
            education=0
            repairs=0
            domestic_appliances=0
            retraining=0
            others=0
        elif (purpose=='business'):
            electronics = 0
            car_new=0
            car_used=0
            furniture_equipment=0
            business=1
            education=0
            repairs=0
            domestic_appliances=0
            retraining=0
            others=0
        elif (purpose=='education'):
            electronics = 0
            car_new=0
            car_used=0
            furniture_equipment=0
            business=0
            education=1
            repairs=0
            domestic_appliances=0
            retraining=0
            others=0
        elif (purpose=='repairs'):
            electronics = 0
            car_new=0
            car_used=0
            furniture_equipment=0
            business=0
            education=0
            repairs=1
            domestic_appliances=0
            retraining=0
            others=0
        elif (purpose=='domestic_appliances'):
            electronics = 0
            car_new=0
            car_used=0
            furniture_equipment=0
            business=0
            education=0
            repairs=0
            domestic_appliances=1
            retraining=0
            others=0
        elif (purpose=='retraining'):
            electronics = 0
            car_new=0
            car_used=0
            furniture_equipment=0
            business=0
            education=0
            repairs=0
            domestic_appliances=0
            retraining=1
            others=0
        else:
            electronics = 0
            car_new=0
            car_used=0
            furniture_equipment=0
            business=0
            education=0
            repairs=0
            domestic_appliances=0
            retraining=0
            others=1
     
        if (isOtherPlans=='yes'):
            yes =1
        else:
            yes=0

        if (isEmployed=='Employed'):
            yes=1
        else:
            yes=0
      
        prediction = model.predict([[ creditamount, duration, electronics, car_new, car_used, furniture_equipment, business, education, repairs, domestic_appliances, 
            retraining, others,disposible, num_existing_credit, status_existing_credit,
            credit_history, yes, yes, employ_len, housing, num_child
        ]])

        output=round(prediction[0],0)
        return{'predict' : "{}".format(output)}
        # if output>=620:
        #     eligibility_msg = "You are eligible for loan."
        # else:
        #     eligibility_msg = "You are not eligible for loan."
        # return{'predict' : "Your Credit Score is {}. {}".format(output, eligibility_msg)}
    #     return render_template('home.html', prediction_text="Your Credit Score is {}. {}".format(output, eligibility_msg))
    # else:
    #     return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
        