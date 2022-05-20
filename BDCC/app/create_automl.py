## This script filters the automl.csv file
from google.cloud import bigquery
from google.cloud import storage
import os

animals = ['Dolphin', 'Fox', 'Horse', 'Butterfly', 'Cat', 'Dog', 'Bee', 'Pig', 'Goose', 'Sea turtle']
PROJECT_ID = 'big-data-project1-347618'
BQ_CLIENT = bigquery.Client(project=PROJECT_ID)
BUCKET_NAME="project1-bigdata2"

print("Overwritting automl.csv")
f = open("automl.csv", "w")

storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)
gsurl="gs://project1-bigdata2/"


## for each animal get 100 imageIds
for animal in animals:
    print("Querying animal " + animal)
    results = BQ_CLIENT.query(
            '''
            SELECT imageId
            FROM  `big-data-project1-347618.dataset1.classes`
            JOIN  `big-data-project1-347618.dataset1.labels` USING(label)
            WHERE description = '{0}'
            ORDER BY Description ASC
        '''.format(animal)).result()
    print(animal + " has " + str(results.total_rows) + " results " )
    count = 0
    for row in results:

        imageId = row[0] ## get the imageId
        ## check if image is on bucket
        image_path = "images/"+imageId+".jpg"
        if not storage.Blob(bucket=bucket,name=image_path).exists(storage_client):
            print(image_path + " doesnt exist in storage ... continue")
            continue

        if count >= 100:
            break
        
        text = ""
        if count < 80:
            text +="TRAIN,"
        elif count >= 80 and count <90:
            text +="VALIDATION,"
        else:
            text +="TEST,"
        text+=gsurl+image_path+","+animal+"\n"
        f.write(text)
        count = count + 1

