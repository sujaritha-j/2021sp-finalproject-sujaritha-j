import json

import pandas as pd
import boto3
import io

from word_embedding.cosineutil import get_cosine_distance
from word_embedding.embedding import WordEmbedding


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    if 'searchText' in event['queryStringParameters']:
        s3_output_path = 's3://finalproject-spring-2021/output/'
        search_text = event['queryStringParameters']['searchText']
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('finalproject-spring-2021')
        data_files_in_s3 = bucket.objects.filter(Prefix="output/")
        distance_list = []
        list_of_dataframes = []
        cols = ['Uniq Id', 'Product Name', 'Selling Price', 'Image', 'About Product']
        try:
            for obj in data_files_in_s3:
                key = obj.key
                body = obj.get()['Body'].read()
                temp = pd.read_csv(io.BytesIO(body), encoding='utf8')
                list_of_dataframes.append(temp)

            product_data_frame = pd.concat(list_of_dataframes)

            # convert search text to vector
            word_embedding = WordEmbedding.from_files('words.txt', 'vectors.npy.gz')
            search_vector = word_embedding.embed_document(search_text)
            # get distance
            for index, row in product_data_frame.iterrows():
                distance = get_cosine_distance(search_vector, row['vectorized_value'])
                distance_list.append({
                    'unique_id': row['Uniq Id'],
                    'product_name': row['Product Name'],
                    'selling_price': row['Selling Price'],
                    'image': row['Image'],
                    'about_product': row['About Product'],
                    'distance': distance
                })
            # get closer top 10 list
            distance_df = pd.DataFrame(distance_list).sort_values(by='distance', ascending=True, na_position='last')
            data_to_api = distance_df.head(10)

        except Exception as e:
            # Send some context about this error to Lambda Logs
            print(e)
            raise e

        search_list = {}
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            "body": json.dumps({
                "status": "success",
                "product_list": data_to_api.to_json(orient='index')
            })
        }

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        "body": json.dumps({
            "status": "No search text"
        })
    }
