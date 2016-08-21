#!/usr/bin/env python3

import argparse
import pandas as pd
from os import path
from Analysis.Analyser import Analyser
from Analysis.Separator import Separator

parse = argparse.ArgumentParser()
parse.add_argument("-f", "--fetch", action="store_true", help="fetch spider result from server.")
parse.add_argument("-o", "--output", type=str, help="save data to csv file where you are expected.")
parse.add_argument("-i", "--input", type=str, help="load data from csv file where you are specified.")
parse.add_argument("-p", "--parallel", action="store_true", help="active parallel mode for better performance")
parse.add_argument("-n", "--cluster_numbers", type=int, default=10, help="K-Means cluster centers, default 20")


if __name__ == "__main__":
    args = parse.parse_args()
    frame = None

    if args.input is not None:
        import pandas as pd
        try:
            if path.exists(args.input):
                frame = pd.read_csv(args.input, sep=',', na_values="NA", encoding="GB18030")
            else:
                print("cannot find the input file: %s" % args.input)
                exit(-1)
        except SystemExit:
            frame = None

    elif args.fetch:
        from DataGraber.Graber import Graber
        fetcher = Graber()
        frame = fetcher.grab()

    if frame is not None:
        if args.output is not None and args.input is None:
            print("Save data frame to file: %s" % args.output)
            frame.to_csv(args.output, sep=",", na_rep="NA", encoding="GB18030")

        separator = Separator(parallel=args.parallel)
        words = separator.map(frame['project'])

        analyser = Analyser(cluster_numbers=args.cluster_numbers)
        tf_idf = analyser.tf_idf(words)
        feature_names = analyser.feature()

        cluster = analyser.cluster(tf_idf)

        frame = pd.concat([frame, pd.DataFrame(data={
            'cluster': cluster.labels_
        })], axis=1)

        keyword = {}
        for index in range(max(cluster.labels_) + 1):
            group = frame.loc[frame['cluster'] == index]
            keys = separator.extract((','.join(group['project']).lower()), topics=5)
            keyword[index] = ' '.join(keys)
        keys = [keyword[each] for each in cluster.labels_]

        frame = pd.concat([frame, pd.DataFrame(data={
            'keyword': keys
        })], axis=1)
        
        if args.output is not None or args.input is not None:
            output_text = path.splitext(args.output if args.output is not None else args.input)
            rst_file = "%s_clustered%s" % (output_text[0], output_text[1])
            print("Save clustered data frame to file: %s" % rst_file)
            frame.to_csv(rst_file, sep=",", na_rep="NA", encoding="GB18030")
