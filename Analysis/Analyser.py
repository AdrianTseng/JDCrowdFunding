from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer


class Analyser:

    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.transformer = TfidfTransformer()

    def tf_idf(self, sentences):
        ori = sentences
        if len(sentences) > 0 and type(sentences[0]) is str:
            ori = [" ".join(each) for each in sentences]

        return self.transformer.fit_transform(self.vectorizer.fit_transform(ori))

    def feature(self):
        return self.vectorizer.get_feature_names()
