#!/usr/bin/env python3

import argparse
from Analysis.Separator import Separator
from Analysis.Analyser import Analyser

parse = argparse.ArgumentParser()
parse.add_argument("-f", "--fetch", action="store_true", help="fetch spider result from server.")
parse.add_argument("-o", "--output", type=str, help="save data to csv file where you are expected.")
parse.add_argument("-i", "--input", type=str, help="load data from csv file where you are specified.")


if __name__ == "__main__":
    args = parse.parse_args()
    frame = None

    if args.input is not None:
        import pandas as pd
        try:
            import os

            if os.path.exists(args.input):
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
            print("Save data frame to file: %s", args.output)
            frame.to_csv(args.output, sep=",", na_rep="NA", encoding="GB18030")

        separator = Separator()
        words = separator.map(frame['project'])

        analyser = Analyser(cluster_numbers=20)
        tf_idf = analyser.tf_idf(words)
        feature_names = analyser.feature()

        cluster = analyser.cluster(tf_idf)

        [print(each) for each in cluster.cluster_centers_]

        print("\n\n\ncluster labels amount: %d" % len(cluster.labels_))

