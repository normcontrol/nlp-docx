from nltk.corpus import stopwords
import string
import numpy as np
import re
import pymorphy2

morph = pymorphy2.MorphAnalyzer(lang='ru')
import spacy

nlp = spacy.load("en_core_web_sm")
from ast import literal_eval


class IntroductionParagraphsCorrelation(object):
    russian_stopwords = stopwords.words("russian")
    russian_stopwords = set(russian_stopwords + ['который', 'таблица', 'рисунок',
                                                 'тот', 'также', 'этот', 'это',
                                                 'такой', 'каждый', 'другой'])

    def __init__(self, df):
        self.df = df
        print("IntroductionParagraphsCorrelation is running")

        df['si_corr_info'] = df['dict_sections_texts'].map(self.__get_info_corr_sections_and_intro)
        df['corr_sections_and_intro'] = df['si_corr_info'].apply(lambda x: x[0])
        # кореляция 'corr_sections_and_intro']
        self.df = df

    def get_results(self):
        '''
        Возвращает датафрейм и степеь корреляции текста с введением
        :return:
        '''
        return {"df": self.df, "corr_sections_and_intro": self.df["corr_sections_and_intro"]}

    def __get_info_corr_sections_and_intro(self, paper_dict):

        if 'введение' not in paper_dict:
            return 0, {}
        intro_preproc = self.__sentence_preproc(paper_dict['введение'])

        dict_intro_parag_corr = {}
        for parag_name in paper_dict.keys():
            if 'введение' in parag_name:
                continue
            parag_text = paper_dict[parag_name]
            if len(parag_text) < 30:
                continue

            parag_preproc = self.__sentence_preproc(parag_text)

            doc_intro = nlp(intro_preproc)
            doc_parag = nlp(parag_preproc)
            corr = doc_parag.similarity(doc_intro)
            dict_intro_parag_corr[parag_name] = corr

        avg_corr_sections_and_intro = np.mean(list(dict_intro_parag_corr.values()))
        return avg_corr_sections_and_intro, dict_intro_parag_corr

    def __sentence_preproc(self, sentence):
        sentence = ''.join([ch for ch in sentence if ch not in string.punctuation])
        sentence = re.sub(r'[^а-яА-Я]', ' ', sentence).strip().replace('  ', '')
        sentence = sentence.split()

        sentence_new = [morph.parse(word)[0].normal_form for word in sentence if word not in self.russian_stopwords and
                        str(morph.parse(word)[0].tag) != 'UNKN']

        sentence_new = ' '.join(sentence_new)

        return sentence_new
