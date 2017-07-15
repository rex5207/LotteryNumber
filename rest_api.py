# -*- coding: utf-8 -*-　
# !flask/bin/python
from flask import Flask, request, jsonify
from flask import render_template
from flask_cors import CORS
from webob import Response
import os
import json
from lunisolar import ChineseDate
import random
import winner_predict

classifier = None
app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')
CORS(app)


@app.route('/', methods=['GET'])
def indexInfo():
    return render_template('index.html')
    

@app.route('/api/getnumber', methods=['POST'])
def lottry_predict():
    # Encryption the plaintext
    json_dict = request.get_json()
    year = int(json_dict['year'])
    month = int(json_dict['month']) + 1
    day = int(json_dict['day'])
    moon_landing = ChineseDate.from_gregorian(year, month, day)
    number = [0] * 49
    user_output = []
    for i in range(7):
        user_input = [moon_landing.month, moon_landing.day] + number
        predicted = int(classifier.predict(user_input))
        while predicted in user_output:
            predicted = random.randint(1, 49)
        user_output.append(predicted)
        number[predicted - 1] = 1

    # Ttansform the ciphertext from bytearray to string
    body = json.dumps(user_output)
    return Response(content_type='application/json', body=body)


if __name__ == "__main__":
    classifier = winner_predict.training_data()
    app.run(host='0.0.0.0', threaded=True, port=8000)
