from MyInfo.standartRouteHandler import *
from MyInfo.textProcesser import *


class Model:
    algorithm = None
    def __init__(self,algorithm):
        self.algorithm = algorithm

    def fit(self, X, Y):
        return self.algorithm.fit(X,Y)


    def predict(self, X):
        return self.algorithm.predict(X)

    def check(self, X, Y, checkQuery):
        predicted = []
        len_base = len(Y)
        TP = 0
        FP = 0

        for i in X:
            predicted.append(self.algorithm.predict(i))

        for i in range(len(Y)):
            if checkQuery(Y[i],predicted[i]):
                TP += 1
            else:
                FP += 1

        FN = len_base - TP
        TN = len_base - FN

        Precision = TP / (TP + FP + 1)
        Recall = TP / (TP + FN + 1)
        FMeasure = 2 * (Precision * Recall) / (Precision + Recall + 1)

        return {'Precision': Precision, 'Recall': Recall, 'Fmeasure': FMeasure}

    def combine(self, result):
        print('')