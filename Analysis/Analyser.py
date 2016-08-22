from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from matplotlib import pyplot as plt
import pandas as pd


plt.style.use('ggplot')


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
        from .Separator import Separator
        from .__init__ import CLUSTER_IMAGE

        colors = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99',
                  '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a']

        new_df = pd.concat([df, pd.DataFrame(data={
            'cluster_label': cluster_result.labels_
        })], axis=1)

        def extract_keywords_and_amount(label, topics = 6):
            group = new_df.loc[new_df['cluster_label'] == label]
            keys = Separator.extract(','.join(group['project']).lower(), topics=topics)
            return ((' '.join(keys)).upper(), group.shape[0])

        labels = list(range(max(cluster_result.labels_) + 1))
        [keywords, amounts] = [list(each) for each in zip(*[extract_keywords_and_amount(label)
                                                            for label in labels])]

        rst = pd.DataFrame(data=amounts, index=keywords, columns=['聚类占比'])

        ax = rst.plot.pie(y='聚类占比', figsize=(10, 10), title="商品关键词",
                          labels=None, autopct='%.1f', colors=colors)
        ax.legend(loc='best')
        plt.savefig("%s.png" % CLUSTER_IMAGE, format="png", dpi=720)
        plt.savefig("%s.pdf" % CLUSTER_IMAGE, format="pdf")
        plt.show()

        return rst
