
class DatasetStructure(object):
    def __init__(self,df):
        # Наличие введения
        df['introduction'] = df['dict_sections_texts'].map(self.__get_introduction)
        self.have_introduction = len(df[df['introduction'] != 'NONE'])
        # Наличие содердания
        df['contents'] = df['dict_sections_texts'].map(self.__get_contents)
        self.have_contents = len(df[df['contents'] != 'NONE'])
        df['conclusion'] = df['dict_sections_texts'].map(self.__get_conclusion)
        df['TZ'] = df['dict_sections_texts'].map(self.__get_TZ)
        self.df = df

    def get_results(self):
        '''

        :return:
        '''
        return {"df": self.df, "introduction":self.have_introduction, "contents": self.have_contents}
    def __get_introduction(self, dict_sections_texts_clean):
        '''

        :param dict_sections_texts_clean:
        :return:
        '''
        try:
            return dict_sections_texts_clean['введение']
        except:
            return 'NONE'

    def __get_contents(self, dict_sections_texts_clean):
        '''

        :param dict_sections_texts_clean:
        :return:
        '''
        if 'оглавление' in dict_sections_texts_clean:
            return dict_sections_texts_clean['оглавление']
        elif 'содержание' in dict_sections_texts_clean:
            return dict_sections_texts_clean['содержание']
        else:
            return 'NONE'

    def __get_conclusion(self, dict_sections_texts_clean):
        if 'заключение' in dict_sections_texts_clean:
            return dict_sections_texts_clean['заключение']
        elif 'выводы' in dict_sections_texts_clean:
            return dict_sections_texts_clean['выводы']
        else:
            return 'NONE'

    def __get_TZ(self, dict_sections_texts_clean):
        for section, texts in dict_sections_texts_clean.items():
            if 'техническое задание' in section:
                return texts
        return 'NONE'

