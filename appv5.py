from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("creditscore_xgboost.pkl", "rb"))

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        creditamount= int(request.form['Credit_amount_group'])
        duration=int(request.form['duration_group'])
        purpose = request.form['Purpose']
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
        disposible=int(request.form['disposible_income_group'])
        num_existing_credit = int(request.form['number_of_existing_credits_at_this_bank'])
        status_exstng_acnt = int(request.form['status_of_existing_checking_account'])
        credit_history= int(request.form['credit_history'])
        other_installment_plans=request.form['other_installment_plans']
        if (other_installment_plans=='yes'):
            yes =1
        else:
            yes=0
        occupation_new=request.form['occupation_new']
        if (occupation_new=='Employed'):
            yes=1
        else:
            yes=0
        employ_len=int(request.form['employment_length'])
        housing = int(request.form['housing'])
        num_depend= int(request.form['number_of_dependents'])
        prediction = model.predict([[ creditamount, duration, electronics, car_new, car_used, furniture_equipment, business, education, repairs, domestic_appliances, 
           retraining, others,disposible, num_existing_credit, status_exstng_acnt,
    credit_history, yes, yes, employ_len, housing, num_depend
        ]])

        output=round(prediction[0],0)
        eligibility_rate = round(((output/900)*100),0)
        
        return render_template('home.html', prediction_text="Your Credit Score is {}. You are {} % likely to be accepted for your loan application".format(output, eligibility_rate))
    else:
        return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
        