## Copies images from example bucket to ours , warning this takes a while
import os
from google.cloud import bigquery
from google.cloud import storage


BQ_CLIENT = bigquery.Client()


animals = ['Dolphin', 'Fox', 'Horse', 'Butterfly', 'Cat', 'Dog', 'Bee', 'Pig', 'Goose', 'Sea turtle']


source_bucket_name = "bdcc_open_images_dataset"
destination_bucket_name = "project1-bigdata2"

storage_client = storage.Client()

source_bucket = storage_client.bucket(source_bucket_name)
destination_bucket = storage_client.bucket(destination_bucket_name)

## for each animal queries the image names
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
    print("Inserting images in other bucket")
    count = 0
    for row in results:
        if count > 100:
            print("Arrived to 100 , going to other animal")
            break
        imageId = row[0]
        ## Copies from one bucket to another
        #print(imageId)
        #os.system("gsutil cp gs://bdcc_open_images_dataset/images/"+imageId+".jpg gs://project1-openimages/images/"+imageId+".jpg")
        image_path = "images/"+imageId+".jpg"
        source_blob = source_bucket.blob(image_path)
        blob_copy = source_bucket.copy_blob(source_blob,destination_bucket,image_path)
        print(
                "Blob {} in bucket {} copied to blob {} in bucket {}.".format(
                    source_blob.name,
                    source_bucket.name,
                    blob_copy.name,
                    destination_bucket.name,
                )
            )
        count+=1



#PROJECT = os.environ.get('GOOGLE_CLOUD_PROJECT')
#BQ_CLIENT = bigquery.Client()

#BUCKET_NAME = "project1-openimages"
#print('Initialising access to storage bucket')
#APP_BUCKET = storage.Client().bucket(BUCKET_NAME)




