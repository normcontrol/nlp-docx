import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

class DepartmentsClassification(object):
    def __init__(self,df):
        loaded_model = pickle.load(open('models/departameny_model.sav', 'rb'))
        yhat = loaded_model.predict(df['main_preproc_text'])
        encoder = LabelEncoder()
        encoder.classes_ = np.load('models/le_department.npy', allow_pickle=True)
        self.departament = encoder.inverse_transform(yhat)

    def get_results(self):
        '''
        Возвращает датафрейм и степеь корреляции текста с введением
        :return:
        '''
        return {"departament": self.departament[0]}

