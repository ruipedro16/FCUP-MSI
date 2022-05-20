# Imports
from google.cloud import storage
from google.cloud import bigquery
from google.cloud import vision
import tfmodel
import os
import logging
import flask
import warnings
import io


warnings.filterwarnings("ignore", category=FutureWarning)


# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

PROJECT = os.environ.get('GOOGLE_CLOUD_PROJECT')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'big-data-project1-347618-be6d8ed4bd0b.json'

logging.info('Google Cloud project is {}'.format(PROJECT))

# Initialisation
logging.info('Initialising app')
app = flask.Flask(__name__)

logging.info('Initialising BigQuery client')
BQ_CLIENT = bigquery.Client()

BUCKET_NAME = "project1-bigdata2.appspot.com"
logging.info('Initialising access to storage bucket {}'.format(BUCKET_NAME))
APP_BUCKET = storage.Client().bucket(BUCKET_NAME)
APP_BUCKET = storage.Client().bucket("project1-bigdata2")
logging.info('Initialising TensorFlow classifier')
TF_CLASSIFIER = tfmodel.Model(
    app.root_path + "/static/tflite/model.tflite",
    app.root_path + "/static/tflite/dict.txt"
)
logging.info('Initialisation complete')

# End-point implementation


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/classes')
def classes():
    results = BQ_CLIENT.query(
        '''
        Select Description, COUNT(*) AS NumImages
        FROM `big-data-project1-347618.dataset1.labels`
        JOIN `big-data-project1-347618.dataset1.classes` USING(label)
        GROUP BY Description
        ORDER BY Description
    ''').result()
    logging.info('classes: results={}'.format(results.total_rows))
    data = dict(results=results)
    return flask.render_template('classes.html', data=data)


@app.route('/relations')
def relations():
    results = BQ_CLIENT.query(
        '''
        SELECT Relation, COUNT(*) As NumImages
        FROM `big-data-project1-347618.dataset1.relations`
        GROUP BY Relation
        ORDER BY Relation ASC
    ''').result()

    logging.info('classes: results={}'.format(results.total_rows))
    data = dict(results=results)
    return flask.render_template('relations.html', data=data)


@app.route('/image_info')
def image_info():
    image_id = flask.request.args.get('image_id')

    results_classes = BQ_CLIENT.query(
        '''
        SELECT Description
        FROM `big-data-project1-347618.dataset1.labels`
        JOIN `big-data-project1-347618.dataset1.classes` USING(label)
        WHERE ImageId = '{0}'
        ORDER BY Description ASC
    '''.format(image_id)
    ).result()

    results_relations = BQ_CLIENT.query(
        '''
        SELECT C1.Description as Class1, R.Relation, C2.Description as Class2
        FROM `big-data-project1-347618.dataset1.relations` R
        JOIN `big-data-project1-347618.dataset1.classes` C1 ON (R.label1=C1.label)
        JOIN `big-data-project1-347618.dataset1.classes` C2 ON (R.label2=C2.label)
        WHERE R.ImageId = '{0}'
    '''.format(image_id)
    ).result()

    data = dict(description=image_id,
                classes=results_classes,
                relations=results_relations
                )
    logging.info('image_info: image_id={}, classes={}, relations={}'.format(
        image_id, results_classes.total_rows, results_relations.total_rows))
    return flask.render_template('image_id.html', data=data)


@app.route('/image_search')
def image_search():
    description = flask.request.args.get('description')
    image_limit = flask.request.args.get('image_limit', default=10, type=int)
    results = BQ_CLIENT.query(
        '''
        SELECT ImageId
        FROM `big-data-project1-347618.dataset1.labels`
        JOIN `big-data-project1-347618.dataset1.classes` USING(label)
        WHERE Description = '{0}'
        ORDER BY ImageId
        LIMIT {1}
    '''.format(description, image_limit)
    ).result()
    logging.info('image_search: description={} limit={}, results={}'
                 .format(description, image_limit, results.total_rows))
    data = dict(description=description,
                image_limit=image_limit,
                results=results)
    return flask.render_template('image_search.html', data=data)


@app.route('/relation_search')
def relation_search():
    class1 = flask.request.args.get('class1', default='%')
    relation = flask.request.args.get('relation', default='%')
    class2 = flask.request.args.get('class2', default='%')
    image_limit = flask.request.args.get('image_limit', default=10, type=int)

    results = BQ_CLIENT.query(
        '''
        SELECT R.ImageId, C1.Description as Class1, R.Relation, C2.Description as Class2
        FROM `big-data-project1-347618.dataset1.relations` R
        JOIN `big-data-project1-347618.dataset1.classes` C1 ON (R.label1=C1.label)
        JOIN `big-data-project1-347618.dataset1.classes` C2 ON (R.label2=C2.label)
        WHERE R.Relation LIKE '{0}'
        AND C1.Description LIKE '{1}'
        AND C2.Description LIKE '{2}'
        ORDER BY R.ImageId
        LIMIT {3}
    '''.format(relation, class1, class2, image_limit)
    ).result()

    logging.info('relation_search: limit={}, results={}'
                 .format(image_limit, results.total_rows))
    data = dict(class1=class1,
                class2=class2,
                relation=relation,
                image_limit=image_limit,
                results=results)
    return flask.render_template('relation_search.html', data=data)


@app.route('/image_search_multiple')
def image_search_multiple():
    descriptions = flask.request.args.get('descriptions').split(',')
    image_limit = flask.request.args.get('image_limit', default=10, type=int)

    results = BQ_CLIENT.query(
        '''
        SELECT ImageId, ARRAY_AGG(Description), COUNT(Description)
        FROM big-data-project1-347618.dataset1.labels
        JOIN big-data-project1-347618.dataset1.classes USING(label)
        WHERE Description IN UNNEST({0})
        GROUP BY ImageId
        ORDER BY Count(Description) DESC, ImageId
        LIMIT {1}
    '''.format(descriptions, image_limit)
    ).result()

    logging.info(
        'image_search_multiple: descriptions={} image_limit={} results={}'.format(
            descriptions, image_limit, results.total_rows)
    )
    data = dict(descriptions=descriptions,
                image_limit=image_limit,
                results=results)
    return flask.render_template(
        'image_search_multiple.html',
        data=data,
        descriptions=descriptions,
        image_limit=image_limit,
        total=results.total_rows,
        description_len=len(descriptions)
    )


@app.route('/image_classify_classes')
def image_classify_classes():
    with open(app.root_path + "/static/tflite/dict.txt", 'r') as f:
        data = dict(results=sorted(list(f)))
        return flask.render_template('image_classify_classes.html', data=data)


@app.route('/image_classify', methods=['POST'])
def image_classify():
    files = flask.request.files.getlist('files')
    min_confidence = flask.request.form.get(
        'min_confidence', default=0.25, type=float)
    results = []
    if len(files) > 1 or files[0].filename != '':
        for file in files:
            classifications = TF_CLASSIFIER.classify(file, min_confidence)
            blob = storage.Blob(file.filename, APP_BUCKET)
            blob.upload_from_file(file, blob, content_type=file.mimetype)
            logging.info('image_classify: filename={} blob={} classifications={}'
                         .format(file.filename, blob.name, classifications))
            results.append(dict(bucket=APP_BUCKET,
                                filename=file.filename,
                                classifications=classifications))

    data = dict(bucket_name=APP_BUCKET.name,
                min_confidence=min_confidence,
                results=results)
    return flask.render_template('image_classify.html', data=data)



@app.route('/cloud_vision', methods=['POST'])
def cloud_vision():
    files = flask.request.files.getlist('files')
    min_confidence = 1

    results = []
    if len(files) > 1 or files[0].filename != '':
        for file in files:
            blob = storage.Blob(file.filename, APP_BUCKET)
            blob.upload_from_file(file, blob, content_type=file.mimetype)
            
            client = vision.ImageAnnotatorClient()
            image = vision.Image()
            image.source.image_uri = 'https://storage.googleapis.com/' + APP_BUCKET.name + '/' + file.filename
            
            response = client.label_detection(image=image)

            if response.error.message:
                raise Exception('{}\nFor more info on error messages, check: https://cloud.google.com/apis/design/errors'.format(response.error.message))

            classifications = response.label_annotations
            scores = list(map(lambda x: x.score, classifications))
            
            if min(scores) < min_confidence:
                min_confidence = min(scores)

            logging.info('cloud_vision: filename={} blob={} classifications={}, scores={}'
                         .format(file.filename, blob.name, classifications, scores))
            results.append(dict(bucket=APP_BUCKET,
                                filename=file.filename,
                                classifications=classifications))
   

    data = dict(bucket_name=APP_BUCKET.name,
                min_confidence='{:.5f}'.format(min_confidence),
                results=results)
    return flask.render_template('cloud_vision.html', data=data)


if __name__ == '__main__':
    # When invoked as a program.
    logging.info('Starting app')
    app.run(host='0.0.0.0', port=8080, debug=True)
