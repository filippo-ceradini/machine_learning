from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
import numpy as np
app = Flask(__name__)

@app.route('/',methods=['get','post'])
def normal():
    if request.method == 'GET':
        return render_template('index.html', result="waiting for you after you have entered the data! Enter all fields!")
    else:
        try:
            model = load_model('willCancel.h5')
            lead_time = int(float(request.form['lead_time']))
            arrival_year = int(float(request.form['arrival_date_year']))
            arrival_week = int(float(request.form['arrival_date_week_number']))
            arrival_day = int(float(request.form['arrival_date_day_of_month']))
            weekend_nights = int(float(request.form['stays_in_weekend_nights']))
            week_nights = int(float(request.form['stays_in_week_nights']))
            adults = int(float(request.form['adults']))
            children = int(float(request.form['children']))
            babies = int(float(request.form['babies']))

            inputs = []
            inputs.append(lead_time)
            inputs.append(arrival_year)
            inputs.append(arrival_week)
            inputs.append(arrival_day)
            inputs.append(weekend_nights)
            inputs.append(week_nights)
            inputs.append(adults)
            inputs.append(children)
            inputs.append(babies)

            inputs.extend(list(map(int, request.form.get('arrival_date_month').split(','))))
            inputs.extend(list(map(int, request.form.get('meal').split(','))))
            inputs.extend(list(map(int, request.form.get('arrival_country').split(','))))

            # Make prediction
            newBookingArr = np.array([inputs])
            prediction = model.predict(newBookingArr)[0][0]
            # Render prediction result
            return render_template('index.html', result='probability booking will be canceled is ' + str(round(float(prediction)*100)) +"%")
        except Exception as e:
            return render_template('index.html', result='Error: ' + str(e))

if __name__ == '__main__':
    app.run()
