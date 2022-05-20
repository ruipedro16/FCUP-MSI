## Population script
## This script uses the .csv given to populate the big guery tables
#from google.colab import auth
import google.cloud.bigquery as bq
import vega_datasets as vd
import pandas as pd
import time



PROJECT_ID = 'big-data-project1-347618'


## This function loads the csv values to the bigquery table
def load_table(dataframe, table_name):
    ## Load the tables
    table = bq.Table(table_name)
    print('Loading data into ' + table_name)
    load_job = client.load_table_from_dataframe(dataframe, table)

    while load_job.running():
        print('waiting for the load job to complete')
        time.sleep(1)

    if load_job.errors == None:
        print('Load complete!')
    else:
        print(load_job.errors)


## MAIN

## Authenticating in gcloud
##print("Authenticating ...")
##auth.authenticate_user()
##gcloud config set project {PROJECT_ID}

## Create the BigQuery client
client = bq.Client(project=PROJECT_ID)

## Create the dataset 'dataset1'
print("Creating dataset dataset1")
#dataset = client.create_dataset('dataset1', exists_ok=True)

## Reading csv files
print("Reading classes.csv")
classes = pd.read_csv("../classes.csv")
image_labels = pd.read_csv("../image-labels.csv")
relations = pd.read_csv("../relations.csv")

## Creating tables

table_classes = PROJECT_ID + '.dataset1.classes'
print('Creating table ' + table_classes)
# Delete the table in case of running this for the second time
client.delete_table(table_classes, not_found_ok=True)
table = bq.Table(table_classes)
table.schema = (
        bq.SchemaField('label',      'STRING'),
        bq.SchemaField('description',      'STRING'),

)
client.create_table(table)


table_labels = PROJECT_ID + '.dataset1.labels'
print('Creating table ' + table_labels)
# Delete the table in case of running this for the second time
client.delete_table(table_labels, not_found_ok=True)
table = bq.Table(table_labels)
table.schema = (
        bq.SchemaField('imageId',      'STRING'),
        bq.SchemaField('label',      'STRING')
)
client.create_table(table)


table_relations = PROJECT_ID + '.dataset1.relations'
# Delete the table in case of running this for the second time
client.delete_table(table_relations, not_found_ok=True)
print('Creating table ' + table_relations)
table = bq.Table(table_relations)
table.schema = (
        bq.SchemaField('imageId',      'STRING'),
        bq.SchemaField('label1',      'STRING'),
        bq.SchemaField('relation',      'STRING'),
        bq.SchemaField('label2',     'STRING')
)
#client.create_table(table)

## Load classes table
load_table(classes,table_classes)

## Load labels table
load_table(image_labels,table_labels)

## Load relations table
load_table(relations,table_relations)

print("Populating done!")



