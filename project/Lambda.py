# First Lambda function -- serialize image data

import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""

    # Get the s3 address from the Step Function event input
    key = event[ "key" ] ## TODO: fill in
    bucket = event[ "bucket" ] ## TODO: fill in

    # Download the data from s3 to /tmp/image.png
    ## TODO: fill in
    ### reference: https://aws.plainenglish.io/how-to-copy-a-file-using-aws-lambda-a64eb9d0c902
    s3.download_file( bucket, key, '/tmp/image.png' )

    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        "statusCode": 200,
        "body": {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }




# Second Lambda function -- invoke inference endpoint

import json
import boto3
import base64
# import sagemaker  ### PITA to get sagemaker uploaded in package.zip

rt_sagemaker = boto3.client( "runtime.sagemaker" )

ENDPOINT = 'image-classification-2022-07-05-00-19-43-157'

def lambda_handler(event, context):
    # Decode the image data
    image = base64.b64decode( event[ "body" ][ "image_data" ] )
    
    # instantiate predictor
    response = rt_sagemaker.invoke_endpoint( EndpointName = ENDPOINT, ContentType = "image/png", Body = image )
    
    inference = json.loads( response[ "Body" ].read() )
    print( inference )
    event[ "inferences" ] = inference
    
    return {
        "statusCode": 200,
        "body": {
            "image_data": event[ "body" ][ "image_data" ],
            "s3_bucket": event[ "body" ][ "s3_bucket" ],
            "s3_key": event[ "body" ][ "s3_key" ],
            "inferences": inference
        }
    }




# Third Lambda function -- filter inferences by threshold

import json

THRESHOLD = .90

def lambda_handler(event, context):

    # Grab the inferences from the event
    ## TODO: fill in
    inferences = event[ "body" ][ "inferences" ]


    # Check if any values in our inferences are above THRESHOLD
    ## TODO: fill in
    meets_threshold = ( inferences[ 0 ]  >= THRESHOLD ) or ( inferences[ 1 ] >= THRESHOLD )

    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if meets_threshold:
        pass
    else:
        raise Exception( "THRESHOLD_CONFIDENCE_NOT_MET" )

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }