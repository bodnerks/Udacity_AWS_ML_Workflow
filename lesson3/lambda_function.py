import HelloBlazePreprocessLambda
import json

def lambda_handler( event, context ):
    preprocess( event[ 's3-data-uri' ] )
    return { 
        'statusCode': 200,
        'body': json.dumps( 'Musical Instrument Reviews Pre-processed!' )
    }