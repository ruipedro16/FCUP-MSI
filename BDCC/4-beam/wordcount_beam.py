import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.options.pipeline_options import PipelineOptions
import argparse
import re
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

with beam.Pipeline() as pipeline:
    lines = (
        pipeline
        | 'Read lines from text file' >> beam.io.ReadFromText(args.input_file)
        | 'Extract words' >> beam.FlatMap(lambda x: re.findall(r'[A-Za-z\']+', x))
        | beam.combiners.Count.PerElement()
        | beam.MapTuple(lambda word, count: '%s: %s' % (word, count))
        | 'Write to output file' >> beam.io.WriteToText(args.output_path)
    )

elapsed_time = time.time() - start_time
print('Elapsed time: {:.3f} seconds'.format(elapsed_time))
