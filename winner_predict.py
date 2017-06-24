# -*- coding: utf-8 -*-　
# !flask/bin/python
from flask import Flask, request, jsonify
from flask import render_template
from flask_cors import CORS
from webob import Response
import os
import json
from sklearn import datasets, svm, metrics
import numpy as np
from sklearn.svm import SVC
from lunisolar import ChineseDate

classifier = SVC(kernel="linear", C=0.04)
app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')
CORS(app)


@app.route('/', methods=['GET'])
def indexInfo():
    return render_template('index.html')


def training_data():
    print "Start training...."
    lottery_input = []
    lottery_output = []
    f = open("lottery_numbers_Chinese", 'r')
    for line in f.readlines():
        number = [0] * 49
        numberInfo = map(int, line.split())
        month = numberInfo[0]
        day = numberInfo[1]

        '''
        input:[12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        output: 33
        '''
        lottery_input.append([month, day] + number)
        lottery_output.append(numberInfo[2])

        for i in range(2, 8, 1):
            number[numberInfo[i] - 1] = 1
            lottery_input.append([month, day] + number)
            lottery_output.append(numberInfo[i + 1])
    f.close

    n_samples = len(lottery_input)

    data = np.hstack(lottery_input)
    data = data.reshape((n_samples, -1))
    lottery_output = np.array(lottery_output)

    classifier.fit(data, lottery_output)
    print "Finish training...."
    # expected = lottery_output[n_samples / 2:]
    # predicted = classifier.predict(data[n_samples / 2:])
    #
    # error = []
    # for i in range(len(expected)):
    #     if(expected[i] != predicted[i]):
    #         error.append(i)
    # print "correct probability is ", (len(expected) - len(error)) / float(len(expected))


@app.route('/api/getnumber', methods=['POST'])
def lottry_predict():
    # Encryption the plaintext
    json_dict = request.get_json()
    year = int(json_dict['year'])
    month = int(json_dict['month'])
    day = int(json_dict['day'])
    moon_landing = ChineseDate.from_gregorian(year, month, day)
    number = [0] * 49
    user_output = []
    for i in range(7):
        user_input = [moon_landing.month, moon_landing.day] + number
        predicted = int(classifier.predict(user_input))
        user_output.append(predicted)
        number[predicted - 1] = 1

    # Ttansform the ciphertext from bytearray to string
    body = json.dumps(user_output)
    return Response(content_type='application/json', body=body)

if __name__ == "__main__":
    training_data()
    app.run(host='0.0.0.0', threaded=True)
