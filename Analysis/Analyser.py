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

    @staticmethod
    def translation(df, cluster_result):
        import pandas as pd
        from .Separator import Separator

        new_df = pd.concat([df, pd.DataFrame(data={
            'cluster_label': cluster_result.labels_
        })], axis=1)

        keyword = {}
        amount = {}
        for index in range(max(cluster_result.labels_) + 1):
            group = new_df.loc[new_df['cluster_label'] == index]
            keys = Separator.extract((','.join(group['project']).lower()), topics=6)
            keyword[index] = (' '.join(keys)).upper()
            amount[index] = group.shape[0]
        keys = [keyword[each] for each in cluster_result.labels_]
        amounts = [amount[each] for each in cluster_result.labels_]

        new_df = pd.concat([new_df, pd.DataFrame(data={
            'keywords': keys,
            'cluster_amount': amounts
        })], axis=1)

        return  new_df
