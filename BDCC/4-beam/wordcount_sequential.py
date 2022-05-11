import re
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

words_dict = {}

with open(args.input_file, 'r') as f:
    lines = f.readlines()

for line in lines:
    words = line.split()
    for word in words:
        if re.match(r'[a-zA-Z]+$', word):
            try:
                words_dict[word] += 1
            except KeyError:
                words_dict[word] = 1

with open(args.output_path, 'w') as f:
    for (k, v) in words_dict.items():
        f.write(f'{k}:{v}\n')

elapsed_time = time.time() - start_time
print('Elapsed time: {:.3f} seconds'.format(elapsed_time))
