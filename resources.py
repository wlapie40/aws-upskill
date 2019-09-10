import logging as logger
from datetime import datetime, timedelta

import boto3
from flask import session
from flask_restful import reqparse

from serializers import serializer

# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('bucket_name', type=str, default=False, required=True)
parser.add_argument('file_name', type=str, default=False, required=False)
parser.add_argument('path', type=str, default=False, required=False)

# #get all instances
# instanceIDs=[]
# ec2 = boto3.resource('ec2')
# instances = ec2.instances.filter(
#     Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])


def _client(service, region_name='eu-west-1'):
    return boto3.client(service, region_name)


def _read_parameters_store(param_name, with_decryption=False): ## todo
    client = boto3.client('ssm', region_name='eu-west-1')
    return tuple(client.get_parameter(Name=param_name, WithDecryption=with_decryption)['Parameter']['Value'].split(','))


#Get weekly CPU usage function
def cloudwatch_metrics(InstanceId):
    client = boto3.client('cloudwatch')
    response = client.get_metric_statistics(
        Namespace='AWS/EC2', #check the AWS docs on the namespaces.
        MetricName='CPUUtilization',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': InstanceId
            },
        ],

        StartTime=datetime.now() - timedelta(days=7),
        EndTime=datetime.now(),
        Period=86400,
        Statistics=[
            'Average',
        ],
        Unit='Percent'
    )

    # for k, v in response.items():
    #     if k == 'Datapoints':
    #         for y in v:
    #             return "{0:.2f}".format(y['Average'])


    for k, v in response.items():
        if k == 'Datapoints':
            for y in v:
                print("{0:.2f}".format(y['Average']))

    return response.items()


def _get_s3_resource():
        return boto3.resource('s3')


def get_bucket():
    s3_resource = _get_s3_resource()
    if 'bucket' in session:
        bucket = session['bucket']
    return s3_resource.Bucket(bucket)


def get_region_name():
    session = _set_session()
    return session.region_name


def _set_session():
    return boto3.session.Session()


def get_buckets_list():
    client = boto3.client('s3')
    return client.list_buckets().get('Buckets')


def _list_s3_buckets():
    client = boto3.client('s3')
    response = client.list_buckets()
    if response['Buckets']:
        json_data = serializer(response, filter='Buckets')
        return json_data
    else:
        return {}


def _delete_s3_bucket_files(**kwargs):
    args = parser.parse_args() # {'bucket_name': 'pgs-s3', 'file_name': 'db-settings.txt', 'path': False}
    bucket_name = args['bucket_name']
    file_name = args['file_name']

    s3_resource = _get_s3_resource()

    my_bucket = s3_resource.Bucket(bucket_name)
    try:
        my_bucket.Object(file_name).delete()
    except Exception as e:
        logger(e)
    #
    return {"HTTPStatusCode": 200,
            'action': 'delete',
            'file_name': file_name,
            'bucket_name': bucket_name}


def _upload_s3_bucket_file(bucket_name=None, path=None, file_name=None):
    try:
        args = parser.parse_args()
        bucket_name = args['bucket_name']
        path = args['path']
        file_name = args['file_name']
    except Exception as e:
        logger(bucket_name)
        logger(path)
        logger(file_name)

    s3_resource = _get_s3_resource()
    try:
        s3_resource.Bucket(bucket_name).upload_file(f'{path}', file_name)
        return {"HTTPStatusCode": 200, 'action': 'upload', 'file_name': file_name, 'bucket_name': bucket_name,
                'path': path}
    except FileNotFoundError:
        return {"FileNotFoundError": f'{file_name} does not exists'}


def _download_s3_bucket_file():
    args = parser.parse_args()
    bucket_name = args['bucket_name']
    file_name = args['file_name']
    logger.debug('test 1')
    s3 = boto3.client('s3')
    try:
        s3.download_file(bucket_name, file_name, file_name)
        return {"HTTPStatusCode": 200, 'file_name': file_name, 'bucket_name': bucket_name}
    except:
        json_data = _list_s3_bucket_files()
        if bucket_name not in {el['Key'] for el in json_data.values()}:
            return {"HTTPStatusCode": 200,
                    'info': f'{file_name} does not exists in S3 bucket: {bucket_name}',
                    bucket_name: json_data}


def _list_s3_bucket_files(bucket_name=None):
    if not bucket_name: ##todo
        args = parser.parse_args()
        bucket_name = args['bucket_name']

    s3 = boto3.client('s3')
    bucket = s3.list_objects(Bucket=bucket_name)
    if bucket:
        json_data = serializer(bucket['Contents'])
        return json_data
    else:
        return bucket

