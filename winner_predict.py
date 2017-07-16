# -*- coding: utf-8 -*-　
from sklearn import datasets, svm, metrics
import numpy as np
from sklearn.svm import SVC
from lunisolar import ChineseDate
import random


def training_data():
    print "Start training...."
    classifier = SVC(kernel="linear", C=0.04)

    lottery_input = []
    lottery_output = []
    f = open("lottery_data/lottery_numbers_Chinese", 'r')
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
    return classifier
