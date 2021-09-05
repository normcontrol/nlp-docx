import joblib
import logging
import json


class StructureLabelsPrediction(object):
    def __init__(self, df):
        logging.basicConfig(level=logging.DEBUG, filename='log.log', format='%(asctime)s %(levelname)s:%(message)s')
        logging.debug("StructureLabelsPrediction is running")
        page_names = ['наличие целей', 'наличие задач', 'наличие во введение цели и задач',
                      'соответствие темы работы направлению', 'соответствие введения заданной теме',
                      'наличие актуальности во введении',
                      'наличие обоснования актуальности во введении']
        lst_page_names = ['page0', 'page1', 'page2', 'page3', 'page4', 'page5', 'page6']

        self.dict_page_names = {k: v for k, v in zip(lst_page_names, page_names)}

    def get_results(self, df):
        '''

        :param df:
        :return:
        '''
        logging.debug("StructureLabelsPrediction.get_results is run")
        main_preproc_text = df['main_preproc_text']
        introduction = df['main_preproc_text']
        dict_results = joblib.load('models/dict_results.jbl')
        result = {}
        for k in dict_results:
            model = dict_results[k].get('model_best')
            result[k] = {
                'predicted_main_preproc_text': model.predict(main_preproc_text)[0],
                'predicted_introduction': model.predict(introduction)[0],
            }
        return result
