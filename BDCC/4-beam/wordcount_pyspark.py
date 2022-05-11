from pyspark import SparkContext, SparkConf
import argparse
import time

parser = argparse.ArgumentParser()

parser.add_argument(
    '--input-file',
    required=True,
    help='The file path for the input text to process.'
)

parser.add_argument(
    '--output-path',
    required=True,
    help='The path prefix for output files.'
)

args = parser.parse_args()

start_time = time.time()

# create Spark context with necessary configuration
sc = SparkContext('local', 'PySpark Word Count Exmaple')

# read data from text file and split each line into words
words = sc.textFile(args.input_file).flatMap(lambda line: line.split(' '))

# count the occurrence of each word
wordCounts = words.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)

# save the counts to output
wordCounts.saveAsTextFile(args.output_path)

elapsed_time = time.time() - start_time
print('Elapsed time: {:.3f} seconds'.format(elapsed_time))
