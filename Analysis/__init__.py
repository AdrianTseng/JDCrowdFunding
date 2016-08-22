import os.path as path

USER_DICT = path.join(path.split(path.realpath(__file__))[0], path.pardir, "user_dict.txt")
STOPWORDS = path.join(path.dirname(USER_DICT), "stopwords.txt")
CLUSTER_IMAGE = path.join(path.dirname(USER_DICT), "R_Home", "Results", "Cluster")