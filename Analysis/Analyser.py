from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer


class Analyser:

    def __init__(self, cluster_numbers=20):
        self.vectorizer = CountVectorizer()
        self.transformer = TfidfTransformer()
        self.cluster_numbers = cluster_numbers

    def tf_idf(self, sentences):
        ori = sentences
        if len(sentences) > 0 and type(sentences[0]) is not str:
            ori = [" ".join(each) for each in sentences]

        return self.transformer.fit_transform(self.vectorizer.fit_transform(ori))

    def feature(self):
        return self.vectorizer.get_feature_names()

    def cluster(self, tf_idf):
        from scipy.sparse import csr_matrix
        matrix = csr_matrix(tf_idf.toarray())
        cluster = KMeans(n_clusters=self.cluster_numbers)
        cluster.fit(matrix)
        return cluster
