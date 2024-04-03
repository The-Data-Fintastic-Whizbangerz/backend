from flask import Flask, request, render_template, json
from flask_cors import CORS
import sklearn
import pickle
import pandas as pd

app = Flask(__name__)
CORS(app)
model = pickle.load(open("CreditScorePrediction1.pkl", "rb"))

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/api', methods = ['GET'])
def returnresult():
	return {'Test':'HelloWorld'}


@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        response = json.loads(request.data)
        print('Request:', response)

        purpose = response['purpose']
        print('Purpose:',purpose)
        
        if (purpose=='radio_television'):
            radio_television = 1
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
            radio_television = 0
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
            radio_television = 0
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
            radio_television = 0
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
            radio_television = 0
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
            radio_television = 0
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
            radio_television = 0
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
            radio_television = 0
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
            radio_television = 0
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
            radio_television = 0
            car_new=0
            car_used=0
            furniture_equipment=0
            business=0
            education=0
            repairs=0
            domestic_appliances=0
            retraining=0
            others=1
        
        occupation = int(response['occupation'])       
        employ_len=int(response['employLength'])
        guarntor = response['guarantor']
        if (guarntor == 'co_applicant'):
            co_applicant = 1
            guarantor =0
            none = 0
        elif (guarntor == 'guarantor'):
            co_applicant = 0
            guarantor =1
            none = 0
        else:
            co_applicant = 0
            guarantor =0
            none = 1
        house = response['house']
        if (house=='own'):
            own = 1
            rent=0
            for_free=0 
        elif (house=='rent'):
            own = 0
            rent=1
            for_free=0 
        else:
            own = 0
            rent=0
            for_free=1

        res_len = response['residentLength']
        if (res_len == 'one_year_or_less'):
            one_year_or_less = 1
            two_years =0
            three_years =0
            More_than_4_years =0
        elif (res_len == 'two_years'):
            one_year_or_less = 0
            two_years =1
            three_years =0
            More_than_4_years =0
        elif (res_len == 'three_years'):
            one_year_or_less = 0
            two_years =0
            three_years =1
            More_than_4_years =0
        else:
            one_year_or_less = 0
            two_years =0
            three_years =0
            More_than_4_years =1
        
        agegp=int(response['ageGroup'])
        sex=response['sex']
        if (sex=='female'):
            female =1
            male=0
        else:
            female=0
            male=1
        
        num_child= int(response['numChild'])
        
        prediction = model.predict([[
           radio_television, car_new, car_used, furniture_equipment, business, education, repairs, domestic_appliances, 
           retraining, others,occupation,employ_len,
           co_applicant,  guarantor, none,
            own, rent,  for_free,
           one_year_or_less, two_years, three_years,More_than_4_years, 
           agegp,
           female, male, num_child 
        ]])

        output=round(prediction[0],0)
        if output>=620:
            eligibility_msg = "You are eligible for loan."
        else:
            eligibility_msg = "You are not eligible for loan."
        return{'predict' : "Your Credit Score is {}. {}".format(output, eligibility_msg)}
    #     return render_template('home.html', prediction_text="Your Credit Score is {}. {}".format(output, eligibility_msg))
    # else:
    #     return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
        