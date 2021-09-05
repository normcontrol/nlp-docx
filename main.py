from flask import Flask
from flask_restful import Resource, Api
from DataCollectionPreparation import DataCollectionPreparation
from DatasetStructure import DatasetStructure
from IntroductionParagraphsCorrelation import IntroductionParagraphsCorrelation
import json
from DepartmentsClassification import DepartmentsClassification
from StructureLabelsPrediction import StructureLabelsPrediction

app = Flask(__name__)
api = Api(app)
import numpy as np


class Nlp(Resource):
    def get(self, userId, documentDirectory, documentPath):
        list_with_data = []
        path = "C:\\core\\documents\\" + userId + "\\" + documentDirectory + "\\" +documentPath
        #path = '/Users/mac/Desktop/flask/Разработка автоматизированной системы защиты информации в системе медико-социальной экспертизы.docx'
        data_collection_preparation = DataCollectionPreparation(path)
        df_docs = data_collection_preparation.get_data()

        #  Есть ли введение и оглавление
        dataset_structure = DatasetStructure(df_docs)
        dataset_structure_res = dataset_structure.get_results()
        df_docs = dataset_structure_res.get("df")
        introduction = dataset_structure_res.get("introduction")
        contents = dataset_structure_res.get("contents")
        #print(dataset_structure_res)
        # print(df_docs)

        # Корреляция текста введению
        introduction_paragraphs_correlation = IntroductionParagraphsCorrelation(df_docs)
        corr_sections_and_intro = introduction_paragraphs_correlation.get_results()
        corr_sections_and_intro = corr_sections_and_intro.get("corr_sections_and_intro")
        #print(corr_sections_and_intro)

        # Предсказания департамента
        departments_classification = DepartmentsClassification(df_docs)
        departament = departments_classification.get_results()
        departament = departament.get("departament")
        #print(departments_classification.get_results())

        # Предсказание наличия целей и всего остального
        structure_labels_prediction = StructureLabelsPrediction(df_docs)
        structure_labels_prediction = structure_labels_prediction.get_results(df_docs)

        return json.dumps({'have_introduction': introduction,
                           'have_contents': contents,
                           'have_TZ': 'in_dev',
                           'have_conclusion': 'in_dev',
                           'cor_text_and_intro': str(corr_sections_and_intro.values[0]),
                           'is_direction': departament,
                           'labels_prediction': structure_labels_prediction
                           }, cls=NpEncoder)


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)
