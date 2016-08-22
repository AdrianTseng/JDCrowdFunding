import jieba

from .__init__ import path, USER_DICT, STOPWORDS


class Separator:

    def __init__(self, parallel=False):
        self.stopwords = open(STOPWORDS, 'r', encoding="utf-8").read().splitlines()
        extended = [each for each in ["", " ", "\t"] if each not in self.stopwords]
        for each in extended:
            self.stopwords.append(each)
        self.stopwords = tuple(self.stopwords)
        self.parallel = parallel

    def initialization(self):
        jieba.enable_parallel() if self.parallel else jieba.disable_parallel()
        if path.exists(USER_DICT):
            jieba.load_userdict(USER_DICT)

    def run(self, sentence):
        self.initialization()
        return [word for word in jieba.cut(sentence=sentence, cut_all=False) if word not in self.stopwords]

    def map(self, sentences):
        self.initialization()

        def process(sentence):
            return [word for word in jieba.cut(sentence) if word not in self.stopwords]

        return list(map(process, sentences))

    @staticmethod
    def extract(data, topics=5):
        from jieba import analyse
        analyse.set_stop_words(STOPWORDS)
        return analyse.extract_tags(data, topK=topics, withWeight=False)
