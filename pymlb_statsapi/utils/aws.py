# """
# created by nikos at 7/20/21
# """
# import boto3
# import os
#
# from botocore.exceptions import ClientError
#
# from .log import LogMixin
#
# AWS_REGION = os.environ.get('MLB_STATSAPI__REGION', 'us-west-2')
# S3_DATA_BUCKET = os.environ.get("MLB_STATSAPI__S3_DATA_BUCKET", f"mlb-statsapi-etl-{AWS_REGION}-data")
# ENV = os.environ.get('MLB_STATSAPI__ENV', f'mlb-statsapi-{AWS_REGION}')
#
#
# class Singleton(type):
#     _instances = {}
#
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#         return cls._instances[cls]
#
#
# class AWSClient(LogMixin):
#
#     def __init__(self, region_name=AWS_REGION, *args, **kwargs):
#         self._client = boto3.client(self.__class__.__name__.lower(), *args, region_name=region_name, **kwargs)
#
#
# def check_response(func):
#     """method annotation to check the HTTPStatusCode for boto3 calls"""
#     def checker(self: AWSClient, *args, **kwargs):
#         self.log.info(f"{func.__name__} {args=} {kwargs=}")
#         res = func(self, *args, **kwargs)
#         assert res['ResponseMetadata']['HTTPStatusCode'] // 100 == 2, f"{func.__name__} failed: {str(res)}"
#         return res
#     return checker
#
#
# # noinspection PyPep8Naming
# class S3(AWSClient):
#
#     def exists(self, bucket, key: str) -> bool:
#         try:
#             self.head_object(Bucket=bucket, Key=key)
#             return True
#         except ClientError as e:
#             if e.response["ResponseMetadata"]["HTTPStatusCode"] != 404:
#                 raise e
#         return False
#
#     @check_response
#     def get_object(self, Bucket, Key):
#         return self._client.get_object(Bucket=Bucket, Key=Key)
#
#     @check_response
#     def head_object(self, Bucket, Key):
#         return self._client.head_object(Bucket=Bucket, Key=Key)
#
#     @check_response
#     def list_objects_v2(self, Bucket, Prefix):
#         return self._client.list_objects_v2(Bucket=Bucket, Prefix=Prefix)
#
#     @check_response
#     def put_object(self, Body, Bucket, Key):
#         return self._client.put_object(Body=Body, Bucket=Bucket, Key=Key)
#
#     # NO check_response: does not provide the HTTPStatusCode!!!
#     def upload_file(self, Bucket, Key, Filename):
#         self.log.info(f"upload_file {Bucket=} {Key=} {Filename=}")
#         return self._client.upload_file(Bucket=Bucket, Key=Key, Filename=Filename)
#
#     # NO check_response: does not provide the HTTPStatusCode!!!
#     def download_file(self, Bucket, Key, Filename):
#         self.log.info(f"download_file {Bucket=} {Key=} {Filename=}")
#         res = self._client.download_file(Bucket=Bucket, Key=Key, Filename=Filename)
#         assert os.path.isfile(Filename), f"download_file failed: {str(res)}"
#         return res
#
#
# # noinspection PyPep8Naming
# class SNS(AWSClient):
#
#     @check_response
#     def publish(self, TopicArn, Subject, Message, MessageAttributes):
#         return self._client.publish(
#             TopicArn=TopicArn, Subject=Subject, Message=Message, MessageAttributes=MessageAttributes
#         )
#
#
# # noinspection PyPep8Naming
# class StepFunctions(AWSClient):
#
#     @check_response
#     def describe_execution(self, executionArn):
#         return self._client.describe_execution(executionArn=executionArn)
#
#     @check_response
#     def get_execution_history(self, executionArn):
#         return self._client.get_execution_history(executionArn=executionArn)
#
#     @check_response
#     def start_execution(self, stateMachineArn, name, input):
#         return self._client.start_execution(stateMachineArn=stateMachineArn, name=name, input=input)
#
#     @check_response
#     def send_task_success(self, taskToken, output):
#         return self._client.send_task_success(taskToken=taskToken, output=output)
#
#     @check_response
#     def send_task_failure(self, taskToken, error, cause):
#         return self._client.send_task_failure(taskToken=taskToken, error=error, cause=cause)
#
#     @check_response
#     def stop_execution(self, executionArn):
#         return self._client.stop_execution(executionArn=executionArn)
#
#
# # noinspection PyPep8Naming
# class SQS(AWSClient):
#
#     @check_response
#     def delete_message(self, QueueUrl, ReceiptHandle: str):
#         return self._client.delete_message(QueueUrl=QueueUrl, ReceiptHandle=ReceiptHandle)
#
#     @check_response
#     def receive_message(self, *args, **kwargs):
#         return self._client.receive_message(*args, QueueUrl=kwargs.pop("QueueUrl"), **kwargs)
#
#
# # noinspection PyPep8Naming
# class STS(AWSClient):
#
#     @check_response
#     def assume_role(self, *args, **kwargs):
#         return self._client.assume_role(*args, **kwargs)
#
#     @check_response
#     def get_caller_identity(self, *args, **kwargs):
#         return self._client.get_caller_identity(*args, **kwargs)
